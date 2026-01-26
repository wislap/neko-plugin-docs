# Message Plane 服务器

> Message Plane 是基于 ZeroMQ 的高性能消息总线系统,提供 RPC、PUB/SUB 和 INGEST 三个服务器

---

> Message Plane 是基于 ZeroMQ 的高性能消息总线系统,提供 RPC、PUB/SUB 和 INGEST 三个服务器

### 9.1 架构概述

Message Plane 由三个独立的 ZeroMQ 服务器组成:

1. **RPC Server** (ROUTER socket): 处理同步请求/响应
2. **PUB Server** (PUB socket): 发布消息到订阅者
3. **INGEST Server** (PULL socket): 接收插件推送的消息

**默认端点**:
- RPC: `tcp://127.0.0.1:48913`
- PUB: `tcp://127.0.0.1:48914`
- INGEST: `tcp://127.0.0.1:48915`

**数据存储**:
- 使用内存中的 `TopicStore` 存储消息
- 支持多个独立的 store: `messages`, `events`, `lifecycle`, `runs`, `export`, `memory`
- 每个 store 包含多个 topic,每个 topic 有独立的消息队列

---

### 9.2 RPC Server 端点

RPC Server 使用 ZeroMQ ROUTER socket,支持以下操作:

#### 9.2.1 健康检查

**操作**: `ping` 或 `health`

**请求格式**:
```json
{
  "req_id": "req_001",
  "op": "ping",
  "v": 1
}
```

**响应格式**:
```json
{
  "req_id": "req_001",
  "ok": true,
  "result": {
    "ok": true,
    "ts": 1706252400.123
  }
}
```

**用途**: 检查 RPC 服务器是否正常运行

---

#### 9.2.2 列出 Topics

**操作**: `bus.list_topics`

**请求格式**:
```json
{
  "req_id": "req_002",
  "op": "bus.list_topics",
  "args": {
    "store": "messages"
  }
}
```

**响应格式**:
```json
{
  "req_id": "req_002",
  "ok": true,
  "result": {
    "store": "messages",
    "stores": ["messages", "events", "lifecycle"],
    "topics": ["plugin1.output", "plugin2.log"],
    "topic_count": 2
  }
}
```

**字段说明**:
- `store`: 当前查询的 store 名称
- `stores`: 所有可用的 store 列表
- `topics`: 该 store 中的所有 topic
- `topic_count`: topic 数量

**用途**: 发现可用的消息主题

---

#### 9.2.3 发布消息

**操作**: `bus.publish`

**请求格式**:
```json
{
  "req_id": "req_003",
  "op": "bus.publish",
  "args": {
    "store": "messages",
    "topic": "plugin1.output",
    "payload": {
      "plugin_id": "plugin1",
      "content": "Hello",
      "priority": 5
    }
  }
}
```

**响应格式**:
```json
{
  "req_id": "req_003",
  "ok": true,
  "result": {
    "accepted": true,
    "event": {
      "seq": 123,
      "ts": 1706252400.123,
      "store": "messages",
      "topic": "plugin1.output",
      "index": {
        "plugin_id": "plugin1",
        "priority": 5
      },
      "payload": {
        "plugin_id": "plugin1",
        "content": "Hello",
        "priority": 5
      }
    }
  }
}
```

**限制**:
- Topic 名称最大长度: 128 字符
- Payload 最大大小: 1MB
- 每个 store 最多 10000 个 topic

**用途**: 向消息总线发布消息

---

#### 9.2.4 获取最近消息

**操作**: `bus.get_recent`

**请求格式**:
```json
{
  "req_id": "req_004",
  "op": "bus.get_recent",
  "args": {
    "store": "messages",
    "topic": "plugin1.output",
    "limit": 100,
    "light": false
  }
}
```

**响应格式**:
```json
{
  "req_id": "req_004",
  "ok": true,
  "result": {
    "store": "messages",
    "topic": "plugin1.output",
    "items": [
      {
        "seq": 123,
        "ts": 1706252400.123,
        "store": "messages",
        "topic": "plugin1.output",
        "index": {...},
        "payload": {...}
      }
    ],
    "light": false
  }
}
```

**参数说明**:
- `limit`: 返回数量限制 (最大 10000)
- `light`: 是否只返回索引信息 (不包含完整 payload)

**用途**: 获取 topic 的最新消息

---

#### 9.2.5 获取增量消息

**操作**: `bus.get_since`

**请求格式**:
```json
{
  "req_id": "req_005",
  "op": "bus.get_since",
  "args": {
    "store": "messages",
    "topic": "plugin1.output",
    "after_seq": 100,
    "limit": 200,
    "light": false
  }
}
```

**响应格式**:
```json
{
  "req_id": "req_005",
  "ok": true,
  "result": {
    "store": "messages",
    "topic": "plugin1.output",
    "after_seq": 100,
    "items": [...],
    "light": false
  }
}
```

**参数说明**:
- `after_seq`: 起始序列号,只返回序列号大于此值的消息
- `topic`: 可选,不指定则返回所有 topic 的消息

**用途**: 增量同步消息,实现实时更新

---

#### 9.2.6 查询消息

**操作**: `bus.query`

**请求格式**:
```json
{
  "req_id": "req_006",
  "op": "bus.query",
  "args": {
    "store": "messages",
    "topic": "plugin1.output",
    "plugin_id": "plugin1",
    "priority_min": 5,
    "since_ts": 1706252000.0,
    "until_ts": 1706252400.0,
    "limit": 100
  }
}
```

**响应格式**:
```json
{
  "req_id": "req_006",
  "ok": true,
  "result": {
    "store": "messages",
    "topic": "plugin1.output",
    "items": [...],
    "light": false
  }
}
```

**过滤参数**:
- `plugin_id`: 插件ID过滤
- `source`: 来源过滤
- `kind`: 类型过滤
- `type`: 消息类型过滤
- `priority_min`: 最低优先级
- `since_ts`: 开始时间戳
- `until_ts`: 结束时间戳

**用途**: 复杂条件查询消息

---

#### 9.2.7 高级查询 (Replay)

**操作**: `bus.replay`

**请求格式**:
```json
{
  "req_id": "req_007",
  "op": "bus.replay",
  "args": {
    "store": "messages",
    "plan": {
      "op": "filter",
      "params": {
        "plugin_id": "plugin1",
        "priority_min": 5
      },
      "input": {
        "op": "topic",
        "params": {
          "topic": "plugin1.output"
        }
      }
    },
    "light": false
  }
}
```

**支持的操作**:
- `topic`: 获取 topic 的所有消息
- `filter`: 过滤消息 (支持正则表达式)
- `limit`: 限制返回数量
- `sort`: 排序 (按时间戳或其他字段)
- `where_eq`: 字段相等过滤
- `where_in`: 字段在集合中过滤
- `where_contains`: 字段包含子串过滤
- `union`: 合并多个查询结果
- `intersect`: 取交集
- `diff`: 取差集

**响应格式**:
```json
{
  "req_id": "req_007",
  "ok": true,
  "result": {
    "store": "messages",
    "items": [...],
    "light": false
  }
}
```

**用途**: 构建复杂的查询管道,支持过滤、排序、集合运算等

**代码位置**: `message_plane/rpc_server.py:755-813`

---

### 9.3 PUB Server

**功能**: 使用 ZeroMQ PUB socket 向订阅者广播消息

**订阅主题格式**: `{store}.{topic}`
- 例如: `messages.plugin1.output`, `events.lifecycle`

**消息格式**:
```
[topic_bytes, event_json_bytes]
```

**实现细节**:
- 自动将 RPC Server 和 INGEST Server 接收的消息广播出去
- 支持 topic 过滤订阅
- 使用 JSON 编码

**用途**:
- 实时监控消息流
- 多客户端消息分发
- 事件驱动架构

**代码位置**: `message_plane/pub_server.py:22-28`

---

### 9.4 INGEST Server

**功能**: 使用 ZeroMQ PULL socket 接收插件推送的消息

**消息格式 (Delta Batch)**:
```json
{
  "kind": "delta",
  "items": [
    {
      "store": "messages",
      "topic": "plugin1.output",
      "payload": {
        "plugin_id": "plugin1",
        "content": "Hello"
      }
    }
  ]
}
```

**消息格式 (Snapshot)**:
```json
{
  "kind": "snapshot",
  "store": "messages",
  "topic": "plugin1.state",
  "mode": "replace",
  "items": [
    {"key": "value1"},
    {"key": "value2"}
  ]
}
```

**Snapshot 模式**:
- `replace`: 替换 topic 的所有消息 (默认)
- `append`: 追加到现有消息

**性能优化**:
- 高水位标记 (RCVHWM): 防止内存溢出
- 批量处理: 减少锁竞争
- 统计日志: 监控吞吐量和丢弃率

**限制**:
- Payload 大小验证可配置
- Topic 数量限制
- 自动丢弃超限消息

**用途**:
- 插件推送消息到消息总线
- 高吞吐量消息摄取
- 异步消息处理

**代码位置**: `message_plane/ingest_server.py:256-321`



---

## 总结

Message Plane 共 **9个端点**,基于 ZeroMQ,无 HTTP 认证:
- RPC Server (7个操作): ping, list_topics, publish, get_recent, get_since, query, replay
- PUB Server: 消息广播
- INGEST Server: 消息摄取

**默认端口**:
- RPC: `tcp://127.0.0.1:48913`
- PUB: `tcp://127.0.0.1:48914`
- INGEST: `tcp://127.0.0.1:48915`

提供了高性能的消息总线功能,用于插件间通信和事件分发。
