# 路由器模块化插件

演示使用 `PluginRouter` 将功能拆分为独立模块。

## __init__.py

```python
from plugin.sdk import (
    NekoPluginBase, neko_plugin, PluginRouter,
    plugin_entry, lifecycle, ok, fail,
)


# ── Router 1: 调试功能 ──
class DebugRouter(PluginRouter):
    @plugin_entry()
    async def dump_config(self, **_):
        cfg = await self.config.dump()
        return ok(data={"config": cfg})

    @plugin_entry()
    def ping(self, **_):
        return ok(data={"pong": True, "plugin_id": self.ctx.plugin_id})


# ── Router 2: 用户功能 ──
class UserRouter(PluginRouter):
    def __init__(self):
        super().__init__()
        self._users = {}

    @plugin_entry()
    def create_user(self, name: str, email: str, **_):
        uid = f"u_{len(self._users) + 1}"
        self._users[uid] = {"name": name, "email": email}
        return ok(data={"id": uid})

    @plugin_entry()
    def get_user(self, id: str, **_):
        user = self._users.get(id)
        if not user:
            return fail(message=f"User {id} not found", code=404)
        return ok(data=user)

    @plugin_entry()
    def list_users(self, **_):
        return ok(data={"users": self._users, "count": len(self._users)})


# ── 主插件 ──
@neko_plugin
class ModularPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.include_router(DebugRouter(), prefix="debug_")
        self.include_router(UserRouter(), prefix="user_")

    @lifecycle(id="startup")
    def on_startup(self, **_):
        self.logger.info("Modular plugin ready with debug + user routers")
```

## 入口点列表

| 入口 ID | 来源 |
|---------|------|
| `debug_dump_config` | DebugRouter |
| `debug_ping` | DebugRouter |
| `user_create_user` | UserRouter |
| `user_get_user` | UserRouter |
| `user_list_users` | UserRouter |
