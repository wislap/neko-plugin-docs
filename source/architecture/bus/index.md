# Bus 通信系统

Bus 是 N.E.K.O 插件系统的 **实时数据流** 基础设施，采用发布/订阅架构，提供五大数据流。

## 五大数据流

| 数据流 | Client | Record | 说明 |
|--------|--------|--------|------|
| **消息** | `MessageClient` | `MessageRecord` | 插件间消息传递 |
| **事件** | `EventClient` | `EventRecord` | 入口调用事件追踪 |
| **生命周期** | `LifecycleClient` | `LifecycleRecord` | 插件启停、状态变更 |
| **对话** | `ConversationClient` | `ConversationRecord` | 对话上下文存储 |
| **记忆** | `MemoryClient` | `MemoryRecord` | 长期记忆存储 |

## 架构

```{mermaid}
graph LR
    subgraph Plugins
        PA["Plugin A"]
        PB["Plugin B"]
    end

    subgraph MessagePlane["Message Plane"]
        TS["TopicStore<br/>(环形缓冲)"]
        PUB["PUB 端口"]
    end

    subgraph SDK["Bus SDK"]
        MC["MessageClient"]
        EC["EventClient"]
        LC["LifecycleClient"]
        CC["ConversationClient"]
        MEM["MemoryClient"]
    end

    PA -->|publish| TS
    PB -->|publish| TS
    TS --> PUB
    PUB -->|subscribe| MC
    PUB -->|subscribe| EC
    PUB -->|subscribe| LC
    PUB -->|subscribe| CC
    PUB -->|subscribe| MEM
```

## 数据流模型

所有 Bus 数据基于统一的 `BusRecord` 基类：

```python
@dataclass(frozen=True, slots=True)
class BusRecord:
    kind: str                       # "message" | "event" | "lifecycle" | "conversation" | "memory"
    type: str                       # 子类型
    timestamp: Optional[float]      # 时间戳
    plugin_id: Optional[str]        # 来源插件
    source: Optional[str]           # 来源标识
    priority: int                   # 优先级
    content: Optional[str]          # 内容
    metadata: Dict[str, Any]        # 元数据
    raw: Dict[str, Any]             # 原始数据
```

## 访问方式

通过 `self.ctx.bus` 访问：

```python
# 获取最近的消息
messages = self.ctx.bus.messages.get(max_count=50)

# 获取某个插件的事件
events = self.ctx.bus.events.get(plugin_id="my_plugin", max_count=20)

# 获取生命周期记录
lifecycle = self.ctx.bus.lifecycle.get(max_count=10)

# 获取指定 conversation_id 的对话
conversations = self.ctx.bus.conversations.get(conversation_id="conv_123", max_count=20)

# 获取指定 bucket 的记忆
memories = self.ctx.bus.memory.get(bucket_id="user:alice", limit=20)
```

## BusList 操作

所有 Client 返回的都是 `BusList`，支持丰富的查询操作：

```python
msgs = self.ctx.bus.messages.get(max_count=100)

# 过滤
high_priority = msgs.filter(priority_min=7)
from_plugin = msgs.filter(plugin_id="my_plugin")

# 排序
by_time = msgs.sort(by="timestamp", reverse=True)

# 截断
top20 = by_time.limit(20)

# 集合运算
combined = msgs1.merge(msgs2)
common = msgs1.intersect(msgs2)
diff = msgs1.difference(msgs2)

# 导出结果
records = msgs.dump_records()   # List[MessageRecord]
payloads = msgs.dump()          # List[Dict[str, Any]]
```

```{toctree}
:maxdepth: 2

records
messages
events
lifecycle
conversations
memory
bus-list
watchers
```
