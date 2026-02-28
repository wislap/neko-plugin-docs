# 记录与过滤

## BusRecord 基类

所有 Bus 数据的基类，不可变数据类：

```python
@dataclass(frozen=True, slots=True)
class BusRecord:
    kind: str                       # "message" | "event" | "lifecycle" | "conversation"
    type: Optional[str]             # 子类型（如 message_type, event type）
    timestamp: Optional[float]      # Unix 时间戳
    plugin_id: Optional[str]        # 来源插件 ID
    source: Optional[str]           # 来源标识
    priority: int                   # 优先级 (0-10)
    content: Optional[str]          # 文本内容
    metadata: Dict[str, Any]        # 额外元数据
    raw: Dict[str, Any]             # 原始 payload（完整保留）
```

### 特点

- `frozen=True`：创建后不可修改，线程安全
- `slots=True`：内存高效
- `raw` 字段保留完整原始数据，方便调试

### 去重标识

每种 Record 有不同的去重 key：

| Record 类型 | 去重字段 |
|-------------|---------|
| `MessageRecord` | `message_id` |
| `EventRecord` | `event_id` |
| `LifecycleRecord` | `lifecycle_id` |
| `ConversationRecord` | `conversation_id` |

如果没有专属 ID，回退到 `trace_id`，再回退到 `dump()` 指纹。

## BusFilter 过滤器

```python
@dataclass(frozen=True)
class BusFilter:
    kind: Optional[str] = None           # 精确匹配 kind
    type: Optional[str] = None           # 精确匹配 type
    plugin_id: Optional[str] = None      # 精确匹配 plugin_id
    source: Optional[str] = None         # 精确匹配 source
    kind_re: Optional[str] = None        # 正则匹配 kind
    type_re: Optional[str] = None        # 正则匹配 type
    plugin_id_re: Optional[str] = None   # 正则匹配 plugin_id
    source_re: Optional[str] = None      # 正则匹配 source
    content_re: Optional[str] = None     # 正则匹配 content
    priority_min: Optional[int] = None   # 最低优先级
    since_ts: Optional[float] = None     # 起始时间戳
    until_ts: Optional[float] = None     # 结束时间戳
```

### 过滤器组合

精确匹配和正则匹配可以组合使用，所有条件为 **AND** 关系：

```python
# 获取某个插件的高优先级消息
messages = client.get(
    plugin_id="my_plugin",
    priority_min=7,
    max_count=50,
)
```

## 时间戳解析

Bus 支持多种时间戳格式，统一解析为 Unix float：

| 输入格式 | 示例 |
|---------|------|
| Unix float | `1704067200.0` |
| Unix int | `1704067200` |
| ISO 8601 (Z) | `"2024-01-01T00:00:00Z"` |
| ISO 8601 (tz) | `"2024-01-01T00:00:00+08:00"` |
| ISO 8601 (naive) | `"2024-01-01T00:00:00"` (假定 UTC) |
