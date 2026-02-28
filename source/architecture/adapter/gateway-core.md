# Gateway Core

`AdapterGatewayCore` 是 Gateway 模式的核心编排器，协调六个管线组件处理请求。

## 六管线架构

```{mermaid}
graph TD
    T["1. TransportAdapter<br/>接收外部请求"]
    N["2. RequestNormalizer<br/>→ GatewayRequest"]
    P["3. PolicyEngine<br/>权限/限流检查"]
    R["4. RouteEngine<br/>路由到目标插件"]
    I["5. PluginInvoker<br/>调用插件入口"]
    S["6. ResponseSerializer<br/>→ 外部响应格式"]

    T --> N --> P --> R --> I --> S
```

## 初始化

```python
from plugin.sdk.adapter import AdapterGatewayCore

core = AdapterGatewayCore(
    transport=my_transport,       # 传输层
    normalizer=my_normalizer,     # 规范化器
    policy=my_policy,             # 策略引擎
    router=my_router,             # 路由引擎
    invoker=my_invoker,           # 插件调用器
    serializer=my_serializer,     # 响应序列化器
    logger=self.logger,           # 可选日志
)
```

## 生命周期

```python
await core.start()   # 启动传输层
await core.stop()    # 停止传输层
```

## 请求处理流程

```python
async def handle(self, envelope: ExternalEnvelope):
    # 1. Transport 接收原始请求 → ExternalEnvelope
    # 2. Normalizer 规范化 → GatewayRequest
    request = await self._normalizer.normalize(envelope)

    # 3. Policy 检查 → 通过/拒绝
    await self._policy.check(request)

    # 4. Router 路由 → RouteDecision (plugin_id, entry_id)
    decision = await self._router.route(request)

    # 5. Invoker 调用 → 插件响应
    result = await self._invoker.invoke(decision, request)

    # 6. Serializer 序列化 → 外部响应格式
    response = await self._serializer.serialize(result, envelope)
    return response
```

## 数据模型

### GatewayRequest

```python
class GatewayRequest(BaseModel):
    action: GatewayAction     # "call" | "list" | "describe"
    plugin_id: Optional[str]
    entry_id: Optional[str]
    params: Dict[str, Any]
    metadata: Dict[str, Any]
```

### GatewayAction

| 动作 | 说明 |
|------|------|
| `"call"` | 调用插件入口 |
| `"list"` | 列出可用入口 |
| `"describe"` | 获取入口描述/schema |

### GatewayError

```python
class GatewayError(BaseModel):
    code: str
    message: str
    details: Optional[Dict] = None
```

### GatewayErrorException

可抛出的异常，在管线任何阶段中断处理：

```python
raise GatewayErrorException(
    GatewayError(code="NOT_FOUND", message="Plugin not found")
)
```

## 默认实现

SDK 提供开箱即用的默认实现：

| 接口 | 默认实现 |
|------|---------|
| `RequestNormalizer` | `DefaultRequestNormalizer` |
| `PolicyEngine` | `DefaultPolicyEngine`（全部通过） |
| `RouteEngine` | `DefaultRouteEngine`（从 request 提取） |
| `ResponseSerializer` | `DefaultResponseSerializer` |
| `PluginInvoker` | `CallablePluginInvoker` |
