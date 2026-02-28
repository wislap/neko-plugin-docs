# 系统架构

本章深入讲解 N.E.K.O 插件系统的核心子系统，面向高级开发者和贡献者。

## 分层依赖图

```{mermaid}
graph TD
    T["_types/<br/>类型定义（零依赖）"]
    C["core/<br/>核心实现"]
    S["sdk/<br/>开发者 SDK"]
    SV["server/<br/>HTTP 接口"]
    MP["message_plane/<br/>消息平面"]

    T --> C
    T --> S
    C --> S
    C --> SV
    S --> SV
    MP --> SV
```

| 层 | 目录 | 说明 |
|---|------|------|
| **第零层** | `_types/` | 类型定义 — `ErrorCode`, `Ok`, `Err`, `Result`, 异常, 模型, Protocol |
| **第一层** | `core/` | 核心运行时 — PluginContext, Host, Registry, Worker, 状态机 |
| **第二层** | `sdk/` | 开发者 SDK — 装饰器, 基类, Router, Bus Client, Adapter |
| **第三层** | `server/` | HTTP 接口 — FastAPI 路由, Run/Export, WebSocket, 服务 |
| **辅助** | `message_plane/` | 高性能消息分发 — ZeroMQ, TopicStore, RPC |

## 子系统概览

| 子系统 | 说明 | 复杂度 |
|--------|------|--------|
| [Bus 通信](bus/index.md) | 五大数据流 + BusList + Watcher 实时订阅 | ⭐⭐⭐⭐⭐ |
| [Run/Export](runs/index.md) | 任务执行生命周期 + 进度 + 多格式导出 | ⭐⭐⭐⭐ |
| [Message Plane](message-plane/index.md) | ZeroMQ 三端口消息分发引擎 | ⭐⭐⭐⭐ |
| [Adapter](adapter/index.md) | 多协议统一接入 + Gateway 六管线 | ⭐⭐⭐⭐ |
| [内部机制](internals/index.md) | IPC / Worker / CallChain / Registry / Host | ⭐⭐⭐ |

```{toctree}
:maxdepth: 2

bus/index
runs/index
message-plane/index
adapter/index
internals/index
```
