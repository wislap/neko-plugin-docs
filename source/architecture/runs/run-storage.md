# 存储协议

Run 系统通过 Protocol 定义存储接口，支持可替换的后端实现。

## RunStore Protocol

```python
class RunStore(Protocol):
    def create(self, rec: RunRecord) -> None: ...
    def get(self, run_id: str) -> Optional[RunRecord]: ...
    def update(self, run_id: str, **patch: Any) -> Optional[RunRecord]: ...
    def commit_terminal(
        self,
        run_id: str,
        *,
        status: RunStatus,
        error: Optional[RunError],
        result_refs: List[str],
    ) -> Optional[RunRecord]: ...
```

### 方法说明

| 方法 | 说明 |
|------|------|
| `create` | 创建新的 RunRecord |
| `get` | 按 run_id 查询 |
| `update` | 部分更新字段 |
| `commit_terminal` | 提交终态（原子操作） |

## ExportStore Protocol

```python
class ExportStore(Protocol):
    def append(self, item: ExportItem) -> None: ...
    def list_for_run(
        self, *, run_id: str, after: Optional[str],
        limit: int, category: Optional[ExportCategory] = None,
    ) -> Tuple[List[ExportItem], Optional[str]]: ...
    def remove_for_run(self, run_id: str) -> None: ...
```

### 方法说明

| 方法 | 说明 |
|------|------|
| `append` | 追加 ExportItem |
| `list_for_run` | 分页列出某 Run 的 exports |
| `remove_for_run` | 清理某 Run 的所有 exports |

## 内存实现

默认提供 `InMemoryExportStore`：

- 线程安全（`threading.Lock`）
- 按 `run_id` 分组存储
- 支持分页游标
- 支持 category 过滤
- `remove_for_run()` 防止内存泄漏

## 驱逐策略

当已完成的 Run 超过 `RUN_STORE_MAX_COMPLETED` 时，按 FIFO 驱逐：

1. 从 RunStore 移除最旧的已完成 Run
2. 从 ExportStore 清理对应的 exports
3. 清理 throttle map 等内部状态
