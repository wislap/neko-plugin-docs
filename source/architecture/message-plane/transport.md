# 传输层

Message Plane 的传输层基于 ZeroMQ，提供三种通信模式。

## ZeroMQ 端口

| 端口 | ZMQ 模式 | 端点配置 | 说明 |
|------|---------|---------|------|
| Ingest | PULL | `MESSAGE_PLANE_ZMQ_INGEST_ENDPOINT` | 接收发布请求 |
| RPC | REP | `MESSAGE_PLANE_ZMQ_RPC_ENDPOINT` | 请求/响应查询 |
| PUB | PUB | (内部) | 广播给订阅者 |

## Ingest Server

接收 MsgPack 编码的消息：

```python
# 消息格式
{
    "v": 1,                    # 协议版本
    "kind": "delta_batch",     # 消息类型
    "from": "plugin_id",       # 来源
    "ts": 1704067200.0,        # 时间戳
    "batch_id": "uuid",        # 批次 ID
    "items": [                 # 数据项列表
        {
            "store": "messages",
            "topic": "plugin_id",
            "payload": {...},
        }
    ]
}
```

## RPC Server

处理 `RpcEnvelope` 请求，返回 `RpcResponse`。

支持的操作见 [RPC 协议](protocol.md)。

## SDK 侧客户端

`MessagePlaneRpcClient` 是 SDK 层的 RPC 客户端：

```python
from plugin.sdk.message_plane_transport import MessagePlaneRpcClient

client = MessagePlaneRpcClient(endpoint=RPC_ENDPOINT)
result = client.call("bus.get_recent", {
    "store": "messages",
    "topic": "my_plugin",
    "limit": 50,
})
```

### 特性

- 自动重连
- 超时处理
- MsgPack 序列化
- 错误格式化（`format_rpc_error()`）

## PUB Server

PUB 端口用于实时推送：

- 每次 TopicStore 有新数据时，自动通过 PUB 广播
- 订阅者通过 SUB socket 接收
- 支持 topic 过滤（ZeroMQ 原生支持）

## 启动

```python
from plugin.message_plane import run_message_plane

# 启动 Message Plane（通常由主进程调用）
await run_message_plane()
```

这会同时启动 Ingest、RPC 和 PUB 三个服务。
