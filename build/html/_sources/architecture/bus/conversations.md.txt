# 对话 (Conversations)

对话 Bus 独立于 Messages，专门用于存储和查询对话上下文。

## ConversationRecord

```python
@dataclass(frozen=True, slots=True)
class ConversationRecord(BusRecord):
    conversation_id: Optional[str] = None
    turn_type: Optional[str] = None       # "turn_end" | "session_end" | "renew_session"
    lanlan_name: Optional[str] = None
    message_count: int = 0
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `conversation_id` | 对话 ID |
| `turn_type` | 轮次类型 |
| `lanlan_name` | 关联的 AI 角色名称 |
| `message_count` | 消息计数 |

这些字段从 `metadata` 中自动提取。

## ConversationClient

通过 `self.ctx.bus.conversations` 访问。

```python
import time

# 获取最近对话
convos = self.ctx.bus.conversations.get(max_count=20)

# 按 conversation_id 过滤
convos = self.ctx.bus.conversations.get(conversation_id="conv_123", max_count=50)

# 按时间过滤（最近 1 小时）
convos = self.ctx.bus.conversations.get(since_ts=time.time() - 3600, max_count=100)

# 便捷方法：按 ID 获取
convos = self.ctx.bus.conversations.get_by_id("conv_123", max_count=50)
```

### 参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `conversation_id` | `str` | `None` | 只返回指定会话 |
| `max_count` | `int` | `50` | 最大返回数量 |
| `since_ts` | `float` | `None` | 起始时间戳过滤 |
| `timeout` | `float` | `5.0` | 超时时间 |

## 典型用例

- 查询触发插件的对话历史
- 构建对话上下文窗口
- 对话统计和分析
