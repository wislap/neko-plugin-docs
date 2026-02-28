# Run 状态机

每个 Run 有明确的状态转换规则，由 `_ALLOWED_TRANSITIONS` 定义。

## 状态

| 状态 | 说明 |
|------|------|
| `queued` | 已创建，等待执行 |
| `running` | 正在执行 |
| `succeeded` | 执行成功 |
| `failed` | 执行失败 |
| `canceled` | 被取消 |
| `timeout` | 执行超时 |
| `cancel_requested` | 取消请求已发出，等待插件响应 |

## 状态转换图

```{mermaid}
stateDiagram-v2
    [*] --> queued
    queued --> running
    queued --> canceled

    running --> succeeded
    running --> failed
    running --> timeout
    running --> cancel_requested

    cancel_requested --> canceled
    cancel_requested --> succeeded
    cancel_requested --> failed
```

## 转换规则

```python
_ALLOWED_TRANSITIONS = {
    "queued":           frozenset(("running", "canceled")),
    "running":          frozenset(("succeeded", "failed", "timeout", "cancel_requested")),
    "cancel_requested": frozenset(("canceled", "succeeded", "failed")),
    # 终态不允许转换
    "succeeded":        frozenset(),
    "failed":           frozenset(),
    "canceled":         frozenset(),
    "timeout":          frozenset(),
}
```

### InvalidRunTransition

非法状态转换会抛出异常：

```python
class InvalidRunTransition(RuntimeError):
    def __init__(self, current: str, target: str):
        self.current = current
        self.target = target
```

## RunRecord

```python
class RunRecord(BaseModel):
    # 身份
    run_id: str
    plugin_id: str
    entry_id: str
    status: RunStatus
    created_at: float
    updated_at: float

    # 关联
    task_id: Optional[str] = None
    trace_id: Optional[str] = None
    idempotency_key: Optional[str] = None

    # 生命周期时间戳
    started_at: Optional[float] = None
    finished_at: Optional[float] = None

    # 进度
    progress: Optional[float] = None      # 0.0 - 1.0
    stage: Optional[str] = None
    message: Optional[str] = None
    step: Optional[int] = None
    step_total: Optional[int] = None
    eta_seconds: Optional[float] = None
    metrics: Dict[str, Any] = {}

    # 取消
    cancel_requested: bool = False
    cancel_reason: Optional[str] = None
    cancel_requested_at: Optional[float] = None

    # 结果
    error: Optional[RunError] = None
    result_refs: List[str] = []
```

## 终态

终态集合：`succeeded`, `failed`, `canceled`, `timeout`

进入终态后：
1. `finished_at` 时间戳被设置
2. 不允许再进行状态转换
3. ExportStore 可以安全清理（根据驱逐策略）
