# 状态持久化插件

演示 `__freezable__`、`__persist_mode__` 和扩展类型的使用。

## plugin.toml

```toml
[plugin]
id = "stateful_demo"
name = "Stateful Demo"
version = "1.0.0"
entry = "plugins.stateful_demo:StatefulPlugin"

[plugin_state]
persist_mode = "auto"
```

## __init__.py

```python
from datetime import datetime
from enum import Enum
from pathlib import Path
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok,
)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"


@neko_plugin
class StatefulPlugin(NekoPluginBase):
    __freezable__ = ["counter", "last_run", "status", "tags", "history"]
    __persist_mode__ = "auto"

    def __init__(self, ctx):
        super().__init__(ctx)
        self.counter = 0
        self.last_run = None             # datetime → 自动序列化
        self.status = TaskStatus.PENDING  # Enum → 自动序列化
        self.tags = set()                 # set → 转为 list
        self.history = []

    @lifecycle(id="unfreeze")
    def on_unfreeze(self, **_):
        self.logger.info(
            f"State restored! counter={self.counter}, "
            f"tags={self.tags}, status={self.status}"
        )

    @plugin_entry()
    def increment(self, value: int = 1):
        self.counter += value
        self.last_run = datetime.now()
        self.history.append({"action": "increment", "value": value, "at": str(self.last_run)})
        return ok(data={"counter": self.counter})

    @plugin_entry()
    def add_tag(self, tag: str):
        self.tags.add(tag)
        return ok(data={"tags": list(self.tags)})

    @plugin_entry()
    def set_status(self, status: str):
        self.status = TaskStatus(status)
        return ok(data={"status": self.status.value})

    @plugin_entry()
    def info(self, **_):
        return ok(data={
            "counter": self.counter,
            "last_run": str(self.last_run),
            "status": self.status.value,
            "tags": list(self.tags),
            "history_count": len(self.history),
        })
```

## 行为

1. 首次启动：所有属性为初始值
2. 调用 `increment`/`add_tag` 等入口后，状态自动保存（`persist_mode="auto"`）
3. 插件重启后，`on_unfreeze()` 被调用，所有 `__freezable__` 属性已恢复
4. `datetime`、`Enum`、`set` 等扩展类型自动处理
