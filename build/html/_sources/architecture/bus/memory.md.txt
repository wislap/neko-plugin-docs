# 记忆 (Memory)

记忆 Bus 用于长期记忆存储和检索。

## MemoryClient

通过 `self.ctx.bus.memory` 或 `MemoryClient` 访问。

```python
from plugin.sdk import MemoryClient

# 通过 ctx.bus（推荐）
memory = self.ctx.bus.memory

# 或直接创建
memory = MemoryClient(self.ctx)
```

## 基本操作

```python
# 从指定 bucket 获取记忆
memories = memory.get(bucket_id="user:alice", limit=50)

# 调整超时
memories = memory.get(bucket_id="session:chat_001", limit=20, timeout=3.0)

# 异步版本
memories = await memory.get_async(bucket_id="user:alice", limit=50)
```

### 参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `bucket_id` | `str` | - | 记忆桶 ID（必填） |
| `limit` | `int` | `20` | 最大返回数量 |
| `timeout` | `float` | `5.0` | 超时时间 |

## MemoryRecord

```python
@dataclass(frozen=True)
class MemoryRecord(BusRecord):
    bucket_id: str = "default"
```

## 典型用例

- 存储用户偏好
- 保存重要对话片段
- 跨会话的上下文传递
