# Message Plane 架构设计文档

> Message Plane 是 N.E.K.O Plugin Server 的高性能消息总线系统

---

## 概述

Message Plane 是基于 ZeroMQ 的分布式消息总线,为插件系统提供高性能的进程间通信能力。它采用三服务器架构,支持请求/响应、发布/订阅和消息摄取三种通信模式。

**核心特性**:
- 基于 ZeroMQ 的高性能消息传递
- 支持 MessagePack 和 JSON 双序列化格式
- 内存消息存储,支持多 store 和多 topic
- 灵活的查询和过滤能力
- 支持正则表达式查询和复杂查询管道

---

## 架构设计

### 三服务器架构

Message Plane 由三个独立的 ZeroMQ 服务器组成:

```
┌─────────────────────────────────────────────────────────┐
│                    Message Plane                         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ RPC Server   │  │ PUB Server   │  │INGEST Server │  │
│  │ (ROUTER)     │  │ (PUB)        │  │ (PULL)       │  │
│  │ :48913       │  │ :48914       │  │ :48915       │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                  │                  │          │
│         └──────────────────┼──────────────────┘          │
│                            │                             │
│                    ┌───────▼────────┐                    │
│                    │  Store Registry│                    │
│                    │  ┌────────────┐│                    │
│                    │  │ messages   ││                    │
│                    │  │ events     ││                    │
│                    │  │ lifecycle  ││                    │
│                    │  │ runs       ││                    │
│                    │  │ export     ││                    │
│                    │  │ memory     ││                    │
│                    │  └────────────┘│                    │
│                    └────────────────┘                    │
└─────────────────────────────────────────────────────────┘
```

#### 1. RPC Server (ROUTER Socket)

**功能**: 处理同步请求/响应通信

**端点**: `tcp://127.0.0.1:48913`

**支持的操作**:
- `ping` / `health`: 健康检查
- `bus.list_topics`: 列出所有 topic
- `bus.publish`: 发布消息
- `bus.get_recent`: 获取最近的消息
- `bus.get_since`: 获取增量消息
- `bus.query`: 条件查询消息
- `bus.replay`: 高级查询管道

**通信模式**: REQ-REP (请求-响应)

**序列化**: JSON 和 MessagePack 双支持

#### 2. PUB Server (PUB Socket)

**功能**: 向订阅者广播消息

**端点**: `tcp://127.0.0.1:48914`

**通信模式**: PUB-SUB (发布-订阅)

**主题格式**: `{store}.{topic}`
- 例如: `messages.plugin1.output`

**序列化**: JSON

**特性**:
- 自动广播 RPC 和 INGEST 接收的消息
- 支持主题过滤订阅
- 零拷贝消息转发

#### 3. INGEST Server (PULL Socket)

**功能**: 接收插件推送的消息

**端点**: `tcp://127.0.0.1:48915`

**通信模式**: PUSH-PULL (推送-拉取)

**支持的消息类型**:
- `delta_batch`: 批量增量消息
- `snapshot`: 快照消息 (replace/append 模式)

**序列化**: MessagePack

**性能优化**:
- 高水位标记 (RCVHWM) 防止内存溢出
- 批量处理减少锁竞争
- 统计日志监控吞吐量

---

## 数据模型

### Store Registry

Store Registry 管理多个独立的消息存储:

```python
StoreRegistry
├── messages    (默认 store)
├── events
├── lifecycle
├── runs
├── export
└── memory
```

每个 Store 包含:
- 多个 Topic (主题)
- 每个 Topic 有独立的消息队列
- 元数据 (创建时间、最后更新时间、消息总数)

### Topic Store

Topic Store 是单个消息存储的实现:

**核心数据结构**:
```python
class TopicStore:
    name: str                                    # Store 名称
    maxlen: int                                  # 每个 topic 最大消息数
    items: Dict[str, Deque[Dict[str, Any]]]     # topic -> 消息队列
    meta: Dict[str, Dict[str, Any]]             # topic -> 元数据
    _seq: int                                    # 全局序列号
    _lock: threading.RLock                       # 并发控制锁
```

**消息结构**:
```python
{
    "seq": 123,                    # 全局序列号
    "ts": 1706252400.123,          # 时间戳
    "store": "messages",           # Store 名称
    "topic": "plugin1.output",     # Topic 名称
    "payload": {...},              # 原始 payload
    "index": {                     # 索引字段 (用于快速查询)
        "plugin_id": "plugin1",
        "source": "main",
        "priority": 5,
        "kind": "log",
        "type": "info",
        "timestamp": 1706252400.123,
        "id": "msg_001"
    }
}
```

### 索引提取

Message Plane 自动从 payload 中提取索引字段:

**提取规则**:
- `plugin_id`: 直接从 payload.plugin_id
- `source`: 直接从 payload.source
- `priority`: 从 payload.priority,默认 0
- `kind`: 从 payload.kind
- `type`: 从 payload.type 或 payload.message_type
- `timestamp`: 从 payload.timestamp 或 payload.time,默认当前时间
- `id`: 按优先级从 message_id, event_id, lifecycle_id, id, task_id, run_id 提取

**用途**:
- 快速过滤和查询
- 避免扫描完整 payload
- 支持复杂查询条件

---

## 查询能力

### 基础查询

#### 1. get_recent - 获取最近消息

```python
# 获取 topic 的最近 100 条消息
items = store.get_recent("plugin1.output", limit=100)
```

**特性**:
- 无锁优化的快速路径
- 直接从 deque 尾部切片
- 并发安全

#### 2. get_since - 增量查询

```python
# 获取序列号 > 1000 的消息
items = store.get_since(topic="plugin1.output", after_seq=1000, limit=200)
```

**特性**:
- 支持跨 topic 查询 (topic=None 或 "*")
- 按序列号排序
- 用于实时同步

#### 3. query - 条件查询

```python
# 复杂条件查询
items = store.query(
    topic="plugin1.output",
    plugin_id="plugin1",
    priority_min=5,
    since_ts=1706252000.0,
    until_ts=1706252400.0,
    limit=100
)
```

**支持的过滤条件**:
- `plugin_id`: 插件ID
- `source`: 来源
- `kind`: 类型
- `type`: 消息类型
- `priority_min`: 最低优先级
- `since_ts`: 开始时间戳
- `until_ts`: 结束时间戳

### 高级查询 (Replay)

Replay 提供了强大的查询管道能力:

#### 支持的操作

**一元操作** (Unary Operations):
- `limit`: 限制返回数量
- `sort`: 排序 (支持多字段、正序/倒序)
- `filter`: 过滤 (支持正则表达式)
- `where_eq`: 字段相等过滤
- `where_in`: 字段在集合中过滤
- `where_contains`: 字段包含子串过滤
- `where_regex`: 正则表达式过滤

**二元操作** (Binary Operations):
- `merge`: 合并两个查询结果 (去重)
- `intersection`: 取交集
- `difference`: 取差集

#### 查询管道示例

```python
# 复杂查询管道
plan = {
    "kind": "unary",
    "op": "limit",
    "params": {"n": 50},
    "child": {
        "kind": "unary",
        "op": "filter",
        "params": {
            "plugin_id": "plugin1",
            "priority_min": 5
        },
        "child": {
            "kind": "get",
            "op": "topic",
            "params": {
                "topic": "plugin1.output",
                "max_count": 200
            }
        }
    }
}
```

**执行流程**:
1. 从 topic 获取最近 200 条消息
2. 过滤 plugin_id="plugin1" 且 priority>=5 的消息
3. 限制返回前 50 条

---

## 并发控制

### 锁策略

**RLock (可重入锁)**:
- 保护 Store 的并发访问
- 支持同一线程多次获取
- 避免死锁

**无锁优化**:
- `get_recent` 使用乐观读取
- 失败时重试,最多 3 次
- 减少锁竞争,提高吞吐量

### 线程安全

**Python 版本**:
- 使用 `threading.RLock` 保护共享状态
- Deque 操作在锁保护下进行
- 服务器使用独立线程

**Rust 版本**:
- 使用 `Arc<RwLock>` 共享状态
- 读写锁提高并发性能
- 多线程事件循环

---

## 性能优化

### 内存管理

**Deque 最大长度**:
- 每个 topic 的 deque 有 maxlen 限制
- 自动丢弃最老的消息
- 防止内存无限增长

**默认配置**:
- `MESSAGE_PLANE_STORE_MAXLEN`: 10000 条/topic
- `MESSAGE_PLANE_TOPIC_MAX`: 10000 个 topic/store
- `MESSAGE_PLANE_PAYLOAD_MAX_BYTES`: 1MB/payload

### 序列化优化

**MessagePack**:
- 二进制格式,比 JSON 更紧凑
- 更快的序列化/反序列化
- INGEST Server 使用 MessagePack

**JSON**:
- 人类可读,便于调试
- RPC Server 双支持
- PUB Server 使用 JSON

### 查询优化

**索引加速**:
- 提取常用字段到 index
- 避免扫描完整 payload
- 快速过滤不匹配的消息

**批量处理**:
- INGEST Server 批量摄取
- 减少锁获取次数
- 提高吞吐量

---

## 协议设计

### RPC 协议

**请求格式**:
```json
{
  "v": 1,
  "op": "bus.query",
  "req_id": "req_001",
  "args": {...},
  "from_plugin": "plugin1"
}
```

**响应格式**:
```json
{
  "v": 1,
  "req_id": "req_001",
  "ok": true,
  "result": {...},
  "error": null
}
```

**错误格式**:
```json
{
  "v": 1,
  "req_id": "req_001",
  "ok": false,
  "result": null,
  "error": {
    "code": "BAD_ARGS",
    "message": "Invalid arguments",
    "details": {...}
  }
}
```

### INGEST 协议

**Delta Batch**:
```json
{
  "kind": "delta",
  "items": [
    {
      "store": "messages",
      "topic": "plugin1.output",
      "payload": {...}
    }
  ]
}
```

**Snapshot**:
```json
{
  "kind": "snapshot",
  "store": "messages",
  "topic": "plugin1.state",
  "mode": "replace",
  "items": [...]
}
```

---

## 安全特性

### 输入验证

**Pydantic 模型**:
- 严格的类型检查
- 字段长度限制
- 防止注入攻击

**正则表达式保护**:
- 最大长度限制 (128 字符)
- 超时保护 (20ms)
- 使用 `regex` 库支持超时

### 资源限制

**Topic 限制**:
- 最大 topic 数量
- Topic 名称长度限制
- 自动拒绝超限请求

**Payload 限制**:
- 最大 payload 大小
- 可配置验证开关
- 防止内存溢出

---

## 监控和诊断

### 统计日志

INGEST Server 提供统计日志:
- 接收消息数
- 接受消息数
- 丢弃消息数
- 最后处理的 store/topic/plugin

### 健康检查

- `ping` / `health` 端点
- 返回时间戳
- 验证服务器可用性

---

## 配置参数

主要配置位于 `plugin/settings.py`:

```python
# 端点配置
MESSAGE_PLANE_ZMQ_RPC_ENDPOINT = "tcp://127.0.0.1:48913"
MESSAGE_PLANE_ZMQ_PUB_ENDPOINT = "tcp://127.0.0.1:48914"
MESSAGE_PLANE_ZMQ_INGEST_ENDPOINT = "tcp://127.0.0.1:48915"

# 存储配置
MESSAGE_PLANE_STORE_MAXLEN = 10000
MESSAGE_PLANE_TOPIC_MAX = 10000
MESSAGE_PLANE_TOPIC_NAME_MAX_LEN = 128

# 性能配置
MESSAGE_PLANE_PAYLOAD_MAX_BYTES = 1048576  # 1MB
MESSAGE_PLANE_GET_RECENT_MAX_LIMIT = 10000
MESSAGE_PLANE_INGEST_RCVHWM = 10000

# 验证配置
MESSAGE_PLANE_VALIDATE_MODE = "off"  # off, warn, strict
MESSAGE_PLANE_VALIDATE_PAYLOAD_BYTES = False

# 统计配置
MESSAGE_PLANE_INGEST_STATS_LOG_ENABLED = True
MESSAGE_PLANE_INGEST_STATS_INTERVAL_SECONDS = 5.0
```

---

## 使用场景

### 1. 插件间通信

插件通过 Message Plane 发送和接收消息:
```python
# 插件 A 发布消息
bus.publish("messages", "pluginA.output", {"data": "hello"})

# 插件 B 订阅消息
bus.subscribe("messages.pluginA.output", callback)
```

### 2. 事件分发

系统事件通过 Message Plane 分发:
```python
# 发布生命周期事件
bus.publish("lifecycle", "plugin.started", {
    "plugin_id": "plugin1",
    "timestamp": time.time()
})
```

### 3. 运行状态同步

Run Protocol 使用 Message Plane 同步状态:
```python
# 发布运行状态
bus.publish("runs", f"run.{run_id}.status", {
    "run_id": run_id,
    "status": "running"
})
```

### 4. 数据导出

插件导出数据到 Message Plane:
```python
# 导出数据
bus.publish("export", f"run.{run_id}.export", {
    "run_id": run_id,
    "type": "text",
    "data": "result"
})
```

---

## 总结

Message Plane 是 N.E.K.O Plugin Server 的核心基础设施,提供了:
- ✅ 高性能的进程间通信
- ✅ 灵活的消息存储和查询
- ✅ 强大的过滤和查询能力
- ✅ 完善的并发控制和安全保护
- ✅ 丰富的监控和诊断功能

它为插件系统提供了可靠、高效的消息总线能力,是实现插件间通信和事件驱动架构的关键组件。
