# API 参考

本章由 Sphinx autodoc 从源码自动生成，提供精确的 API 签名、参数说明和类型定义。

## 模块索引

### SDK 公开 API

| 模块 | 说明 |
|------|------|
| {doc}`sdk/base` | `NekoPluginBase` 插件基类 |
| {doc}`sdk/decorators` | 装饰器 API |
| {doc}`sdk/config` | `PluginConfig` |
| {doc}`sdk/router` | `PluginRouter` |
| {doc}`sdk/hooks` | Hook 系统 |
| {doc}`sdk/state` | 状态持久化 |
| {doc}`sdk/database` | 数据库 |
| {doc}`sdk/store` | 键值存储 |
| {doc}`sdk/plugins` | 跨插件调用 |
| {doc}`sdk/responses` | `ok()` / `fail()` |
| {doc}`sdk/memory` | `MemoryClient` |
| {doc}`sdk/system-info` | `SystemInfo` |
| {doc}`sdk/types` | SDK 类型 |

### Bus API

| 模块 | 说明 |
|------|------|
| {doc}`bus/types` | BusList / BusRecord 核心类型 |
| {doc}`bus/records` | BusRecord / BusFilter |
| {doc}`bus/messages` | MessageClient / MessageRecord |
| {doc}`bus/events` | EventClient / EventRecord |
| {doc}`bus/lifecycle` | LifecycleClient / LifecycleRecord |
| {doc}`bus/conversations` | ConversationClient / ConversationRecord |
| {doc}`bus/watchers` | BusListWatcher / BusListDelta |

### Adapter API

| 模块 | 说明 |
|------|------|
| {doc}`adapter/base` | AdapterBase / AdapterConfig |
| {doc}`adapter/gateway-core` | AdapterGatewayCore |
| {doc}`adapter/gateway-models` | GatewayRequest / GatewayError |
| {doc}`adapter/contracts` | 六管线接口 |
| {doc}`adapter/types` | AdapterMessage / AdapterResponse |

### 类型定义

| 模块 | 说明 |
|------|------|
| {doc}`types/errors` | ErrorCode |
| {doc}`types/result` | Ok / Err / Result |
| {doc}`types/exceptions` | PluginError 异常层级 |
| {doc}`types/models` | Pydantic 数据模型 |
| {doc}`types/events` | 事件类型定义 |
| {doc}`types/protocols` | Protocol 接口 |

### Server API

| 模块 | 说明 |
|------|------|
| {doc}`server/runs` | Run/Export 管理器 |
| {doc}`server/services` | trigger_plugin 等服务 |
| {doc}`server/routes` | HTTP API 端点 |

```{toctree}
:maxdepth: 1
:hidden:

sdk/base
sdk/decorators
sdk/config
sdk/router
sdk/hooks
sdk/state
sdk/database
sdk/store
sdk/plugins
sdk/responses
sdk/memory
sdk/system-info
sdk/types
bus/types
bus/records
bus/messages
bus/events
bus/lifecycle
bus/conversations
bus/watchers
adapter/base
adapter/gateway-core
adapter/gateway-models
adapter/contracts
adapter/types
types/errors
types/result
types/exceptions
types/models
types/events
types/protocols
server/runs
server/services
server/routes
```
