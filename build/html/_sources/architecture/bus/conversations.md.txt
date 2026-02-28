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
# 获取最近对话
convos = self.ctx.bus.conversations.get(max_count=20)

# 按插件过滤
convos = self.ctx.bus.conversations.get(plugin_id="chat_adapter")
```

## 典型用例

- 查询触发插件的对话历史
- 构建对话上下文窗口
- 对话统计和分析
