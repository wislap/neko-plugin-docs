# 实时监听 (Watchers)

`BusListWatcher` 提供 Bus 数据的实时订阅和增量更新能力。

## 概述

Watcher 监听 Bus 数据变化，当新数据到达或数据被删除时，触发回调：

```{mermaid}
sequenceDiagram
    participant W as Watcher
    participant MP as Message Plane
    participant CB as Callback

    W->>MP: 订阅 topic
    loop 数据变化
        MP->>W: 推送增量 delta
        W->>W: 本地应用增量
        W->>CB: 触发回调 (BusListDelta)
    end
```

## 推荐用法

优先通过 `BusList.watch()` 创建 watcher，而不是手动实例化 `BusListWatcher`。

```python
messages = (
    self.ctx.bus.messages
    .get(max_count=100)
    .filter(priority_min=5)
    .sort(by="timestamp", reverse=True)
    .limit(50)
)

watcher = messages.watch(debounce_ms=100.0)

@watcher.subscribe(on=("add", "change"))
def on_delta(delta: BusListDelta):
    print(f"Added: {len(delta.added)}, Removed: {len(delta.removed)}")
    print(f"Current total: {len(delta.current)}")

watcher.start()

# ... 退出时停止
watcher.stop()
```

`on` 支持规则：

- `"add"`：新增记录
- `"del"`：删除记录
- `"change"`：集合内容发生变化（综合事件）

## BusListDelta

增量变化数据：

```python
@dataclass(frozen=True)
class BusListDelta(Generic[TRecord]):
    kind: str                          # Bus 类型
    added: Tuple[TRecord, ...]         # 新增的记录
    removed: Tuple[DedupeKey, ...]     # 删除的去重 key
    current: BusList[TRecord]          # 变化后的完整列表
```

## 使用约束

- Watcher 依赖可重放 plan，列表应由 `get()/filter()/where_*/sort(by=...)/limit()` 等结构化操作构建。
- `where(predicate)`、`sort(key=callable)` 这类不可重放步骤会导致 watcher 创建失败。
- 当前可稳定推断和监听的 bus 为：`messages` / `events` / `lifecycle`。

## 防抖

`debounce_ms` 参数控制回调触发频率，避免高频更新时的性能问题：

- `0`：每次变化立即触发
- `100`：100ms 内的变化合并为一次回调
- `500`：适合 UI 刷新场景

## 典型用例

- 实时消息列表（聊天界面）
- 事件监控仪表盘
- 插件状态实时显示
