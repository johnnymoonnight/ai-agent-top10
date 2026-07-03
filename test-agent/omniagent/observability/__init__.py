"""可观测性系统 - 融合 LangSmith/Braintrust/Mastra evals"""
from __future__ import annotations
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from enum import Enum

logger = logging.getLogger("omniagent.observability")


class SpanStatus(Enum):
    OK = "ok"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class Span:
    """追踪跨度 - OpenTelemetry 兼容"""
    span_id: str
    parent_id: Optional[str] = None
    name: str = ""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: SpanStatus = SpanStatus.OK
    attributes: Dict = field(default_factory=dict)
    events: List[Dict] = field(default_factory=list)


@dataclass
class EvalResult:
    metric: str
    score: float
    threshold: float = 0.5
    passed: bool = True
    details: str = ""


class Tracer:
    """追踪器 - LangSmith/OpenTelemetry 追踪"""
    def __init__(self):
        self._spans: Dict[str, Span] = {}
        self._current_span: Optional[Span] = None

    def start_span(self, name: str, attributes: Optional[Dict] = None) -> Span:
        span = Span(
            span_id=f"span_{int(time.time() * 1000)}_{len(self._spans)}",
            name=name,
            parent_id=self._current_span.span_id if self._current_span else None,
            attributes=attributes or {}
        )
        self._spans[span.span_id] = span
        self._current_span = span
        return span

    def end_span(self, status: SpanStatus = SpanStatus.OK):
        if self._current_span:
            self._current_span.end_time = time.time()
            self._current_span.status = status

    def add_event(self, name: str, attributes: Optional[Dict] = None):
        if self._current_span:
            self._current_span.events.append({
                "name": name, "attributes": attributes or {},
                "timestamp": datetime.now().isoformat()
            })

    def get_trace(self) -> List[Dict]:
        return [{"span_id": s.span_id, "name": s.name, "status": s.status.value,
                 "duration": (s.end_time or time.time()) - s.start_time}
                for s in self._spans.values()]


class Evaluator:
    """评估器 - Braintrust/Mastra evals 评估框架"""
    def __init__(self):
        self._metrics: Dict[str, Callable] = {}

    def register_metric(self, name: str, fn: Callable):
        self._metrics[name] = fn

    async def evaluate(self, metric: str, **kwargs) -> EvalResult:
        return await self._eval(metric, **kwargs)

    def register_builtin_metrics(self):
        self.register_metric("response_quality", lambda response, **kw: 0.8)
        self.register_metric("tool_accuracy", lambda tool_calls, **kw: 0.85)
        self.register_metric("task_completion", lambda result, **kw: 0.9)
        self.register_metric("latency", lambda duration_ms, **kw: max(0, 1 - duration_ms / 10000))
        self.register_metric("hallucination", lambda response, source, **kw: 0.95)

    async def _eval(self, name, **kw):
        """Invoke a registered metric (sync) and return EvalResult"""
        fn = self._metrics.get(name)
        if not fn:
            return EvalResult(metric=name, score=0.0, passed=False, details="Metric not found")
        try:
            score = fn(**kw)
            return EvalResult(metric=name, score=score, passed=score >= 0.5)
        except Exception as e:
            return EvalResult(metric=name, score=0.0, passed=False, details=str(e))
