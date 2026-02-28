# Message Plane 消息平面

Message Plane 是 N.E.K.O 的高性能消息分发引擎，基于 ZeroMQ 构建，提供 Bus 数据的存储、查询和实时推送。

## 架构

```{mermaid}
graph LR
    subgraph Plugins["插件进程"]
        PA["Plugin A"]
        PB["Plugin B"]
    end

    subgraph MP["Message Plane"]
        INGEST["Ingest Server<br/>(ZMQ PULL)"]
        STORE["TopicStore<br/>(环形缓冲)"]
        RPC["RPC Server<br/>(ZMQ REP)"]
        PUB["PUB Server<br/>(ZMQ PUB)"]
    end

    subgraph Server["Plugin Server"]
        BRIDGE["PlaneBridge"]
    end

    PA -->|push| INGEST
    PB -->|push| INGEST
    INGEST --> STORE
    STORE --> PUB
    BRIDGE -->|delta_batch| INGEST

    PA <-->|request/reply| RPC
    PB <-->|request/reply| RPC
    RPC <--> STORE
```

## 三端口架构

| 端口 | 类型 | 方向 | 说明 |
|------|------|------|------|
| **Ingest** | ZMQ PULL | 入站 | 接收发布请求 |
| **RPC** | ZMQ REP | 双向 | 请求/响应查询 |
| **PUB** | ZMQ PUB | 出站 | 实时推送订阅者 |

## 数据流

1. **发布**：插件通过 Ingest 端口发送数据
2. **存储**：TopicStore 按 topic 存储到环形缓冲区
3. **推送**：PUB 端口向所有订阅者广播
4. **查询**：SDK 通过 RPC 端口查询历史数据

```{toctree}
:maxdepth: 2

protocol
stores
transport
bridge
```
