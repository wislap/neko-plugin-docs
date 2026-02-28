# 事件 (Events)

事件记录插件入口点的调用轨迹。

## EventRecord

```python
@dataclass(frozen=True, slots=True)
class EventRecord(BusRecord):
    event_id: Optional[str] = None
    entry_id: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `event_id` | 事件唯一 ID（来自 `trace_id`） |
| `entry_id` | 触发的入口点 ID |
| `args` | 调用参数 |

## EventClient

通过 `self.ctx.bus.events` 访问。

```python
# 获取最近事件
events = self.ctx.bus.events.get(max_count=50)

# 按插件过滤
events = self.ctx.bus.events.get(plugin_id="my_plugin", max_count=20)

# 异步
events = await self.ctx.bus.events.get_async(max_count=50)
```

## 典型用例

- 监控某个入口的调用频率
- 审计日志
- 调试调用链
