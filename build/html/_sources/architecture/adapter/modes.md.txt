# 工作模式

Adapter 支持四种工作模式，通过 `plugin.toml` 的 `[adapter].mode` 配置。

## AdapterMode 枚举

```python
class AdapterMode(str, Enum):
    GATEWAY = "gateway"
    ROUTER = "router"
    BRIDGE = "bridge"
    HYBRID = "hybrid"
```

## Gateway 模式

**转发请求到其他插件**。Adapter 本身不处理业务逻辑，只负责协议转换和路由分发。

```
外部请求 → 协议解析 → 路由匹配 → 调用目标插件 → 格式化响应 → 返回
```

适用场景：MCP Server、REST API 网关。

## Router 模式

**直接处理请求**。Adapter 自身包含业务逻辑，不转发到其他插件。

```
外部请求 → 协议解析 → Adapter 内部处理 → 格式化响应 → 返回
```

适用场景：独立 HTTP 服务、WebSocket 服务。

## Bridge 模式

**协议转换**。将一种协议转换为另一种，两端都是外部系统。

```
协议 A → 解析 → 转换 → 协议 B
```

适用场景：MQTT → HTTP 桥接、WebSocket → gRPC 桥接。

## Hybrid 模式

**根据规则动态选择**。默认模式，可以根据请求内容决定走 Gateway、Router 还是 Bridge 路径。

```
外部请求 → 路由规则匹配 → Gateway / Router / Bridge
```

## 配置示例

```toml
[adapter]
mode = "gateway"
priority = 0

[adapter.protocols.mcp]
enabled = true
port = 8080
```
