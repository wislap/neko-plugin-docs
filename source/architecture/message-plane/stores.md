# TopicStore

TopicStore 是 Message Plane 的内存存储引擎，按 topic 组织数据，使用环形缓冲区限制内存。

## 数据模型

```python
@dataclass
class TopicStore:
    name: str           # store 名称（如 "messages", "events"）
    maxlen: int         # 每个 topic 的最大条目数
```

每个 store 包含多个 topic，每个 topic 是一个独立的环形缓冲区（`deque(maxlen=N)`）。

## 核心操作

### publish

```python
def publish(self, topic: str, payload: Dict) -> Dict:
    """发布一条数据到指定 topic"""
    # 返回包含 seq, ts, store, topic, payload, index 的事件
```

发布时自动：
- 分配递增序号 `seq`
- 记录时间戳 `ts`
- 提取索引字段 `index`
- 更新 topic 元数据

### get_recent

```python
def get_recent(self, topic: str, limit: int, light: bool = False):
    """获取 topic 的最近 N 条数据"""
```

`light=True` 时只返回索引，不返回完整 payload，用于高效列表查询。

### list_topics

```python
def list_topics(self) -> List[Dict]:
    """列出所有 topic 及其元数据"""
    # 按 last_ts 倒序排列
```

## 元数据

每个 topic 维护元数据：

| 字段 | 说明 |
|------|------|
| `created_at` | 创建时间 |
| `last_ts` | 最后更新时间 |
| `count_total` | 历史总数（含已驱逐） |

## 索引提取

发布时自动从 payload 提取索引字段，用于快速过滤：

| 索引字段 | 来源 |
|---------|------|
| `plugin_id` | `payload["plugin_id"]` |
| `source` | `payload["source"]` |
| `priority` | `payload["priority"]` |
| `kind` | `payload["kind"]` |
| `type` | `payload["type"]` / `payload["message_type"]` |
| `timestamp` | `payload["timestamp"]` / `payload["time"]` |
| `id` | `payload["message_id"]` / `payload["event_id"]` / ... |

## 线程安全

TopicStore 使用 `threading.RLock` 保护所有操作，支持多线程并发访问。

## 环形缓冲

当 topic 中的条目数超过 `maxlen` 时，最旧的条目自动被驱逐。这确保了固定的内存占用。
