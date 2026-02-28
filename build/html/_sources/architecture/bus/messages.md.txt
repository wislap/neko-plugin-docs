# 消息 (Messages)

消息是插件间传递数据的主要方式。

## MessageRecord

```python
@dataclass(frozen=True, slots=True)
class MessageRecord(BusRecord):
    message_id: Optional[str] = None
    message_type: Optional[str] = None    # "text" | "url" | "binary" | "binary_url"
    description: Optional[str] = None
```

### 创建方式

- `MessageRecord.from_raw(raw_dict)` — 从原始 payload 创建
- `MessageRecord.from_index(index, payload)` — 从 Message Plane 索引快速创建

## MessageClient

通过 `self.ctx.bus.messages` 访问。

### 获取消息

```python
# 获取最近 50 条消息
msgs = self.ctx.bus.messages.get(max_count=50)

# 按插件过滤
msgs = self.ctx.bus.messages.get(plugin_id="chat_plugin", max_count=20)

# 按优先级过滤
msgs = self.ctx.bus.messages.get(priority_min=5, max_count=10)

# 异步版本
msgs = await self.ctx.bus.messages.get_async(max_count=50)
```

### 参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `plugin_id` | `str` | `None` | 按来源插件过滤 |
| `max_count` | `int` | `50` | 最大返回数量 |
| `priority_min` | `int` | `None` | 最低优先级 |
| `timeout` | `float` | `5.0` | 超时时间 |

### 返回值

返回 `MessageList`（`BusList[MessageRecord]` 的子类），支持链式操作。

## MessageList 操作

```python
msgs = self.ctx.bus.messages.get(max_count=100)

# 过滤：只看文本消息
text_msgs = msgs.filter(type="text")

# 过滤：只看高优先级
urgent = msgs.filter(priority_min=8)

# 排序：按时间倒序
recent = msgs.sort("timestamp", reverse=True)

# 获取第一条
first = msgs.first()

# 转为列表
records = msgs.to_list()

# 统计
count = len(msgs)
```
