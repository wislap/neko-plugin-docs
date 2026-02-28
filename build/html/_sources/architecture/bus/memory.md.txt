# 记忆 (Memory)

记忆 Bus 用于长期记忆存储和检索。

## MemoryClient

通过 `self.ctx.bus.memory` 或 `MemoryClient` 访问。

```python
from plugin.sdk import MemoryClient

# 通过 ctx.bus
memory = self.ctx.bus.memory

# 或直接创建
memory = MemoryClient(self.ctx)
```

## 基本操作

```python
# 获取记忆
memories = memory.get(max_count=50)

# 按插件过滤
memories = memory.get(plugin_id="memory_plugin")
```

## MemoryRecord

```python
@dataclass(frozen=True, slots=True)
class MemoryRecord(BusRecord):
    memory_id: Optional[str] = None
```

## 典型用例

- 存储用户偏好
- 保存重要对话片段
- 跨会话的上下文传递
