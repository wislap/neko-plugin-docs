# Adapter 协议适配

Adapter 系统提供多协议统一接入能力，让外部系统（MCP、HTTP、WebSocket 等）通过标准化管道调用 N.E.K.O 插件。

## 核心设计

```{mermaid}
graph LR
    EXT["外部协议<br/>(MCP/HTTP/WS)"]
    T["TransportAdapter<br/>协议解析"]
    N["RequestNormalizer<br/>请求规范化"]
    P["PolicyEngine<br/>策略引擎"]
    R["RouteEngine<br/>路由引擎"]
    I["PluginInvoker<br/>插件调用"]
    S["ResponseSerializer<br/>响应序列化"]

    EXT --> T --> N --> P --> R --> I --> S --> EXT
```

六管线 Gateway Core 编排器，每个环节可独立替换。

## 四种工作模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **Gateway** | 转发请求到其他插件 | API 网关 |
| **Router** | 直接处理请求 | 独立服务 |
| **Bridge** | 协议转换 | 协议桥接 |
| **Hybrid** | 根据规则选择 | 复杂场景 |

## 组件

| 组件 | 说明 |
|------|------|
| `AdapterBase` | Adapter 插件基类 |
| `AdapterConfig` | 从 `plugin.toml` `[adapter]` 解析的配置 |
| `AdapterGatewayCore` | Gateway 编排器 |
| 六管线接口 | Transport / Normalizer / Policy / Route / Invoker / Serializer |

```{toctree}
:maxdepth: 2

modes
gateway-core
contracts
building-adapter
```
