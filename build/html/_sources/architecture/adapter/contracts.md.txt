# 接口契约

Gateway Core 的六个管线组件均通过 Protocol 定义接口，支持自定义实现。

## TransportAdapter

负责接收外部请求并转换为 `ExternalEnvelope`：

```python
class TransportAdapter(Protocol):
    @property
    def protocol_name(self) -> str: ...

    async def start(self) -> None: ...
    async def stop(self) -> None: ...
```

## RequestNormalizer

将 `ExternalEnvelope` 转换为统一的 `GatewayRequest`：

```python
class RequestNormalizer(Protocol):
    async def normalize(self, envelope: ExternalEnvelope) -> GatewayRequest: ...
```

## PolicyEngine

执行权限检查、速率限制等策略：

```python
class PolicyEngine(Protocol):
    async def check(self, request: GatewayRequest) -> None: ...
    # 不通过时抛出 GatewayErrorException
```

## RouteEngine

根据请求决定路由目标：

```python
class RouteEngine(Protocol):
    async def route(self, request: GatewayRequest) -> RouteDecision: ...
```

### RouteDecision

```python
class RouteDecision(BaseModel):
    plugin_id: str
    entry_id: str
    mode: RouteMode        # "direct" | "broadcast" | "round_robin"
    params: Dict[str, Any]
```

### RouteMode

| 模式 | 说明 |
|------|------|
| `"direct"` | 直接路由到指定插件 |
| `"broadcast"` | 广播到多个插件 |
| `"round_robin"` | 轮询分发 |

## PluginInvoker

执行实际的插件调用：

```python
class PluginInvoker(Protocol):
    async def invoke(
        self, decision: RouteDecision, request: GatewayRequest
    ) -> Any: ...
```

## ResponseSerializer

将插件响应转换为外部协议格式：

```python
class ResponseSerializer(Protocol):
    async def serialize(
        self, result: Any, envelope: ExternalEnvelope
    ) -> Any: ...
```

## LoggerLike

日志接口（可选注入）：

```python
class LoggerLike(Protocol):
    def info(self, msg: str, *args, **kwargs) -> None: ...
    def warning(self, msg: str, *args, **kwargs) -> None: ...
    def error(self, msg: str, *args, **kwargs) -> None: ...
    def debug(self, msg: str, *args, **kwargs) -> None: ...
```

## 自定义实现示例

```python
class MyPolicyEngine:
    """自定义策略：只允许白名单插件"""

    def __init__(self, allowed: set):
        self.allowed = allowed

    async def check(self, request: GatewayRequest) -> None:
        if request.plugin_id not in self.allowed:
            raise GatewayErrorException(
                GatewayError(code="FORBIDDEN", message="Plugin not allowed")
            )
```
