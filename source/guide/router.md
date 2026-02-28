# 路由器

`PluginRouter` 提供类似 FastAPI Router 的模块化入口点组织方式，将插件功能拆分到多个独立模块中。

## 基本用法

### 定义 Router

```python
from plugin.sdk import PluginRouter, plugin_entry, ok

class DebugRouter(PluginRouter):
    @plugin_entry(id="config_debug")
    async def config_debug(self, **_):
        cfg = await self.config.dump()
        return ok(data={"config": cfg})

    @plugin_entry(id="ping")
    def ping(self, **_):
        return ok(data={"pong": True})
```

### 注册到主插件

```python
from plugin.sdk import NekoPluginBase, neko_plugin

@neko_plugin
class MyPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.include_router(DebugRouter())
        self.include_router(MemoryRouter(), prefix="mem_")
```

## prefix

`prefix` 为路由器的所有入口点添加前缀：

```python
self.include_router(DebugRouter(), prefix="debug_")
# "config_debug" → "debug_config_debug"
# "ping" → "debug_ping"
```

## Router 中访问插件属性

Router 绑定后自动获得主插件的属性代理：

```python
class MyRouter(PluginRouter):
    @plugin_entry()
    async def example(self, **_):
        # 这些属性都来自主插件
        self.logger.info("Hello from router!")
        cfg = await self.config.dump()
        result = self.plugins.call_entry("other:ping", {})
        return ok(data=cfg)
```

可用属性：

| 属性 | 说明 |
|------|------|
| `self.ctx` | PluginContext |
| `self.logger` | 日志记录器 |
| `self.config` | PluginConfig |
| `self.plugins` | Plugins（跨插件调用） |
| `self.store` | PluginStore |
| `self.db` | PluginDatabase |

## Hook 在 Router 中

Router 中的 Hook 对该 Router 的入口点以及主插件的入口点都生效：

```python
class LoggingRouter(PluginRouter):
    @hook(target="*", timing="before")
    async def log_all(self, entry_id, **_):
        self.logger.info(f"Entering {entry_id}")
        return None
```

## 错误处理

| 异常 | 场景 |
|------|------|
| `PluginRouterError.not_bound()` | Router 未绑定就访问属性 |
| `PluginRouterError.already_bound()` | Router 重复绑定 |
| `PluginRouterError.dependency_missing()` | 依赖注入失败 |

## 完整示例

```python
from plugin.sdk import (
    NekoPluginBase, neko_plugin, PluginRouter,
    plugin_entry, lifecycle, hook, ok, fail,
)

class AdminRouter(PluginRouter):
    @plugin_entry(id="status")
    def status(self, **_):
        return ok(data={"uptime": "1h", "requests": 42})

    @plugin_entry(id="reset")
    def reset(self, **_):
        self.logger.warning("Resetting plugin state!")
        return ok(data={"reset": True})

class ApiRouter(PluginRouter):
    @hook(target="*", timing="before")
    async def rate_limit(self, entry_id, **_):
        # 简单速率限制
        return None  # 通过

    @plugin_entry(id="query")
    async def query(self, q: str, **_):
        return ok(data={"results": [q]})

@neko_plugin
class MyPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.include_router(AdminRouter(), prefix="admin_")
        self.include_router(ApiRouter(), prefix="api_")

    @lifecycle(id="startup")
    def on_startup(self, **_):
        self.logger.info("Plugin ready with admin + api routers")
```

调用时使用完整 ID：`admin_status`, `admin_reset`, `api_query`。
