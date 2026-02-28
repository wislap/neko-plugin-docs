# PlaneBridge

PlaneBridge 是 Plugin Server（控制面）到 Message Plane 的桥接组件，将服务端产生的数据（如状态变更、消息推送）发送到 Message Plane。

## 架构位置

```
Plugin Server (FastAPI)
    ↓ enqueue_delta()
PlaneBridge (后台线程)
    ↓ ZMQ PUSH
Message Plane Ingest Server
```

## 核心接口

```python
def publish_record(*, store: str, topic: str, payload: Dict) -> None:
    """发布一条记录到 Message Plane"""
```

### 参数

| 参数 | 说明 |
|------|------|
| `store` | 目标 store（如 `"messages"`, `"events"`, `"lifecycle"`） |
| `topic` | 目标 topic（通常是 `plugin_id`） |
| `payload` | 数据内容 |

## delta_batch 格式

PlaneBridge 将数据包装为 `delta_batch` 格式发送：

```python
{
    "v": 1,
    "kind": "delta_batch",
    "from": "control_plane",
    "ts": time.time(),
    "batch_id": str(uuid.uuid4()),
    "items": [
        {
            "store": "messages",
            "topic": "my_plugin",
            "payload": {...},
        }
    ],
}
```

## 内部实现

`_Bridge` 类使用后台线程和内存队列：

- **队列**：`queue.Queue(maxsize=4096)` 限制背压
- **后台线程**：daemon 线程，持续从队列消费并发送到 ZMQ
- **序列化**：使用 `ormsgpack` 高效编码
- **连接管理**：支持 TCP endpoint 解析和连接检测

### 生命周期

```python
bridge = _Bridge()
bridge.start()   # 启动后台线程
bridge.stop()    # 设置停止标志

# 发布数据（非阻塞，放入队列）
bridge.enqueue_delta(store="messages", topic="my_plugin", payload={...})
```

## 配置

| 配置项 | 说明 |
|--------|------|
| `MESSAGE_PLANE_BRIDGE_ENABLED` | 是否启用桥接 |
| `MESSAGE_PLANE_ZMQ_INGEST_ENDPOINT` | Ingest 端点地址 |
