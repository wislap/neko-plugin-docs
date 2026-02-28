# 构建自定义 Adapter

本指南介绍如何构建一个完整的 Adapter 插件。

## 步骤概览

1. 继承 `AdapterBase`
2. 实现 `TransportAdapter`
3. 组装 `AdapterGatewayCore`
4. 处理生命周期

## 完整示例：HTTP Adapter

### plugin.toml

```toml
[plugin]
id = "http_adapter"
name = "HTTP Adapter"
type = "adapter"
entry = "plugins.http_adapter:HttpAdapter"

[adapter]
mode = "gateway"
priority = 0

[adapter.protocols.http]
host = "0.0.0.0"
port = 9000
```

### 实现 TransportAdapter

```python
from aiohttp import web
from plugin.sdk.adapter import TransportAdapter, ExternalEnvelope, Protocol

class HttpTransport(TransportAdapter):
    protocol_name = "http"

    def __init__(self, host: str, port: int, on_request):
        self.host = host
        self.port = port
        self.on_request = on_request
        self.app = web.Application()
        self.runner = None

    async def start(self):
        self.app.router.add_post("/invoke", self._handle)
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()

    async def _handle(self, request):
        body = await request.json()
        envelope = ExternalEnvelope(
            protocol=Protocol.HTTP,
            raw=body,
            metadata={"method": "POST", "path": "/invoke"},
        )
        result = await self.on_request(envelope)
        return web.json_response(result)
```

### 组装 Adapter

```python
from plugin.sdk import NekoPluginBase, neko_plugin, lifecycle
from plugin.sdk.adapter import (
    AdapterBase, AdapterGatewayCore,
    DefaultRequestNormalizer, DefaultPolicyEngine,
    DefaultRouteEngine, CallablePluginInvoker,
    DefaultResponseSerializer,
    on_adapter_startup, on_adapter_shutdown,
)

@neko_plugin
class HttpAdapter(AdapterBase):
    def __init__(self, ctx):
        super().__init__(ctx)

    @on_adapter_startup
    async def start(self):
        cfg = self.adapter_config.protocols.get("http", {})
        transport = HttpTransport(
            host=cfg.get("host", "0.0.0.0"),
            port=cfg.get("port", 9000),
            on_request=self._handle_request,
        )

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

    @on_adapter_shutdown
    async def stop(self):
        await self.gateway.stop()

    async def _handle_request(self, envelope):
        return await self.gateway.handle(envelope)
```

## 关键点

:::{tip}
- `AdapterBase` 继承 `NekoPluginBase`，拥有所有插件能力
- 用 `@on_adapter_startup` / `@on_adapter_shutdown` 管理 Adapter 生命周期
- 默认实现 (`Default*`) 可以快速原型，然后逐步替换为自定义实现
- `CallablePluginInvoker` 接收 `self.plugins`，自动处理跨插件调用
:::
