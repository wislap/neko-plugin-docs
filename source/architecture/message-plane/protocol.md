# RPC 协议

Message Plane 使用自定义 RPC 协议通过 ZeroMQ REP/REQ 通信。

## 协议版本

当前版本：`PROTOCOL_VERSION = 1`

## RPC 操作

```python
RpcOp = Literal[
    "ping",
    "health",
    "bus.list_topics",
    "bus.publish",
    "bus.get_recent",
    "bus.get_since",
    "bus.query",
    "bus.replay",
]
```

| 操作 | 说明 |
|------|------|
| `ping` | 心跳检测 |
| `health` | 健康检查 |
| `bus.list_topics` | 列出所有 topic |
| `bus.publish` | 发布消息 |
| `bus.get_recent` | 获取最近 N 条 |
| `bus.get_since` | 获取某序号之后的数据 |
| `bus.query` | 条件查询 |
| `bus.replay` | 回放历史数据 |

## 请求格式 (RpcEnvelope)

```python
class RpcEnvelope(BaseModel):
    v: int                              # 协议版本 (≥1)
    op: RpcOp                           # 操作类型
    req_id: str                         # 请求 ID (1-64 字符)
    args: Dict[str, Any] = {}           # 操作参数
    from_plugin: Optional[str] = None   # 来源插件 ID
```

## 响应格式 (RpcResponse)

```python
class RpcResponse(BaseModel):
    v: int                              # 协议版本
    req_id: str                         # 对应的请求 ID
    ok: bool                            # 是否成功
    result: Optional[Any] = None        # 成功时的结果
    error: Optional[RpcError] = None    # 失败时的错误
```

## 错误格式 (RpcError)

```python
class RpcError(BaseModel):
    code: str                           # 错误码 (1-64 字符)
    message: str                        # 错误信息
    details: Optional[Dict] = None      # 详细信息
```

## 查询参数示例

### bus.get_recent

```python
class BusGetRecentArgs(BaseModel):
    store: str          # store 名称
    topic: str          # topic 名称
    limit: int          # 最大返回数 (1-10000)
    light: bool = False # 轻量模式（只返回 index，不返回 payload）
```

## 序列化

所有 RPC 消息使用 `ormsgpack` 序列化（MsgPack 格式），高性能且紧凑。
