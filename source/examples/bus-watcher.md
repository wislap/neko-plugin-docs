# Bus 实时监听插件

演示使用 Bus Watcher 实时监听消息变化。

## __init__.py

```python
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok,
)


@neko_plugin
class BusWatcherPlugin(NekoPluginBase):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.recent_messages = []

    @lifecycle(id="startup")
    def on_startup(self, **_):
        # 获取初始消息列表
        msgs = self.ctx.bus.messages.get(max_count=50)
        self.recent_messages = [
            {"plugin_id": m.plugin_id, "content": m.content, "ts": m.timestamp}
            for m in msgs
        ]
        self.logger.info(f"Loaded {len(self.recent_messages)} initial messages")

    @plugin_entry()
    def get_messages(self, plugin_id: str = "", limit: int = 20, **_):
        """获取最近的消息"""
        msgs = self.ctx.bus.messages.get(max_count=limit)

        if plugin_id:
            msgs = msgs.filter(plugin_id=plugin_id)

        result = [
            {
                "plugin_id": m.plugin_id,
                "content": m.content,
                "type": m.message_type,
                "priority": m.priority,
                "timestamp": m.timestamp,
            }
            for m in msgs
        ]
        return ok(data={"messages": result, "count": len(result)})

    @plugin_entry()
    def get_events(self, plugin_id: str = "", limit: int = 20, **_):
        """获取最近的事件"""
        events = self.ctx.bus.events.get(max_count=limit)

        if plugin_id:
            events = events.filter(plugin_id=plugin_id)

        result = [
            {
                "entry_id": e.entry_id,
                "plugin_id": e.plugin_id,
                "timestamp": e.timestamp,
            }
            for e in events
        ]
        return ok(data={"events": result, "count": len(result)})

    @plugin_entry()
    def get_lifecycle(self, limit: int = 10, **_):
        """获取最近的生命周期事件"""
        lc = self.ctx.bus.lifecycle.get(max_count=limit)
        result = [
            {
                "type": l.type,
                "plugin_id": l.plugin_id,
                "timestamp": l.timestamp,
            }
            for l in lc
        ]
        return ok(data={"lifecycle": result, "count": len(result)})
```
