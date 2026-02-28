# 数据采集插件

演示定时采集数据、配置读写、消息推送。

## __init__.py

```python
import time
from datetime import datetime, timezone
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle,
    timer_interval, ok,
)


@neko_plugin
class DataCollectorPlugin(NekoPluginBase):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.collected = []

    @lifecycle(id="startup")
    def startup(self, **_):
        cfg = self.config.dump()
        self.source_url = cfg.get("collector", {}).get("url", "https://example.com/data")
        self.max_items = cfg.get("collector", {}).get("max_items", 1000)
        self.logger.info(f"Collector ready: url={self.source_url}, max={self.max_items}")

    @timer_interval(id="collect", seconds=300, auto_start=True)
    def collect(self, **_):
        now = datetime.now(timezone.utc).isoformat()
        item = {"timestamp": now, "value": len(self.collected) + 1}
        self.collected.append(item)

        if len(self.collected) > self.max_items:
            self.collected = self.collected[-self.max_items:]

        self.config.set("collector.last_run", now)
        self.config.set("collector.total_collected", len(self.collected))

        self.ctx.push_message(
            source="data_collector",
            message_type="text",
            description="数据采集完成",
            priority=3,
            content=f"已采集 {len(self.collected)} 条数据",
        )
        return {"collected": len(self.collected)}

    @plugin_entry()
    def query(self, limit: int = 10, **_):
        return ok(data={"items": self.collected[-limit:], "total": len(self.collected)})

    @plugin_entry()
    def clear(self, **_):
        count = len(self.collected)
        self.collected.clear()
        return ok(data={"cleared": count})
```
