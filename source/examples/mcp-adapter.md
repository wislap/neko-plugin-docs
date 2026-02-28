# MCP Adapter 示例

演示构建一个 MCP (Model Context Protocol) Adapter，将 MCP 请求路由到 N.E.K.O 插件。

:::{note}
这是一个高级示例，展示 Adapter 系统的完整使用方式。
:::

## 架构

```{mermaid}
graph LR
    LLM["LLM Client"] -->|MCP| T["MCP Transport"]
    T --> N["Normalizer"]
    N --> P["Policy"]
    P --> R["Router"]
    R --> I["Invoker"]
    I -->|trigger| PLUGIN["Target Plugin"]
    PLUGIN --> I
    I --> S["Serializer"]
    S --> T
    T -->|MCP| LLM
```

## plugin.toml

```toml
[plugin]
id = "mcp_adapter"
name = "MCP Adapter"
type = "adapter"
entry = "plugins.mcp_adapter:McpAdapter"

[adapter]
mode = "gateway"
priority = 0

[adapter.protocols.mcp]
enabled = true
transport = "stdio"
```

## 简化实现

```python
from plugin.sdk import NekoPluginBase, neko_plugin, lifecycle
from plugin.sdk.adapter import (
    AdapterBase, AdapterGatewayCore,
    DefaultRequestNormalizer, DefaultPolicyEngine,
    DefaultRouteEngine, CallablePluginInvoker,
    DefaultResponseSerializer,
    on_adapter_startup, on_adapter_shutdown,
    ExternalEnvelope, Protocol,
)


class McpTransport:
    """MCP 传输层（简化示例）"""
    protocol_name = "mcp"

    def __init__(self, on_request):
        self.on_request = on_request

    async def start(self):
        # 启动 MCP stdio transport
        pass

    async def stop(self):
        pass

    async def handle_tool_call(self, tool_name: str, arguments: dict):
        """处理 MCP tool call"""
        # 解析 tool_name → plugin_id:entry_id
        parts = tool_name.split(".", 1)
        plugin_id = parts[0]
        entry_id = parts[1] if len(parts) > 1 else "default"

        envelope = ExternalEnvelope(
            protocol=Protocol.MCP,
            raw={
                "action": "call",
                "plugin_id": plugin_id,
                "entry_id": entry_id,
                "params": arguments,
            },
            metadata={"tool_name": tool_name},
        )
        return await self.on_request(envelope)


@neko_plugin
class McpAdapter(AdapterBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.gateway = None

    @on_adapter_startup
    async def start(self):
        transport = McpTransport(on_request=self._handle)

        self.gateway = AdapterGatewayCore(
            transport=transport,
            normalizer=DefaultRequestNormalizer(),
            policy=DefaultPolicyEngine(),
            router=DefaultRouteEngine(),
            invoker=CallablePluginInvoker(self.plugins),
            serializer=DefaultResponseSerializer(),
            logger=self.logger,
        )
        await self.gateway.start()
        self.logger.info("MCP Adapter started")

    @on_adapter_shutdown
    async def stop(self):
        if self.gateway:
            await self.gateway.stop()

    async def _handle(self, envelope):
        return await self.gateway.handle(envelope)
```

## 自定义 PolicyEngine 示例

```python
class McpPolicyEngine:
    """只允许特定工具被调用"""

    def __init__(self, allowed_tools: set):
        self.allowed = allowed_tools

    async def check(self, request):
        tool = f"{request.plugin_id}.{request.entry_id}"
        if tool not in self.allowed:
            from plugin.sdk.adapter import GatewayError, GatewayErrorException
            raise GatewayErrorException(
                GatewayError(code="FORBIDDEN", message=f"Tool {tool} not allowed")
            )
```
