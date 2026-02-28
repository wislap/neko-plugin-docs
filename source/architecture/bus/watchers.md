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

## BusListWatcher

```python
watcher = BusListWatcher(
    lst=messages,           # 初始 BusList
    ctx=replay_context,     # 回放上下文
    bus="messages",         # Bus 类型
    debounce_ms=100.0,      # 防抖间隔
)
```

### 注册回调

```python
def on_change(delta: BusListDelta):
    print(f"Added: {len(delta.added)}, Removed: {len(delta.removed)}")
    print(f"Current total: {len(delta.current)}")

watcher.on_change(on_change)
```

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

## 增量更新机制

Watcher 使用增量更新而非全量刷新：

1. **订阅**：通过 Message Plane 订阅 topic
2. **增量推送**：只传输变化的数据（added/removed）
3. **本地应用**：在本地 BusList 上应用增量
4. **回调触发**：通知注册的回调函数

### 防抖

`debounce_ms` 参数控制回调触发频率，避免高频更新时的性能问题：

- `0` — 每次变化立即触发
- `100` — 100ms 内的变化合并为一次回调
- `500` — 适合 UI 显示场景

## 典型用例

- 实时消息列表（聊天界面）
- 事件监控仪表盘
- 插件状态实时显示
