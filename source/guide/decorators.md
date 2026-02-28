# 装饰器

N.E.K.O SDK 提供了一组声明式装饰器，用于定义插件的入口点、生命周期、事件处理等。

## @neko_plugin

标记一个类为 N.E.K.O 插件。**必须**放在类定义之前。

```python
from plugin.sdk import neko_plugin, NekoPluginBase

@neko_plugin
class MyPlugin(NekoPluginBase):
    pass
```

- 不接收任何参数
- 插件元数据（id / name / version）全部从 `plugin.toml` 读取
- 仅用于打标记，方便框架反射和校验

## @plugin_entry

定义插件的 **外部可调用入口点**，是最核心的装饰器。

### 基本用法

```python
from plugin.sdk import plugin_entry, ok

@plugin_entry(
    id="process",
    name="Process Data",
    description="处理数据",
    kind="action",
)
def process(self, data: str, **_):
    return ok(data={"result": data.upper()})
```

### 完整参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `id` | `str` | 函数名 | 入口点 ID（可省略） |
| `name` | `str` | 同 id | 显示名称（可省略） |
| `description` | `str` | `""` | 描述 |
| `input_schema` | `dict` | 自动推断 | JSON Schema（可省略） |
| `params` | `BaseModel` | `None` | Pydantic Model 自动提取 schema |
| `kind` | `EntryKind` | `"action"` | 类型：`"service"` / `"action"` / `"hook"` / `"custom"` |
| `auto_start` | `bool` | `False` | 是否自动启动 |
| `persist` | `bool` | `False` | 执行后是否自动保存状态 |
| `extra` | `dict` | `{}` | 额外元数据 |

### 三种 Schema 定义方式

**方式一：自动推断（推荐）**

```python
@plugin_entry()
def greet(self, name: str = "World", count: int = 1):
    ...
```

自动生成的 JSON Schema：

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string", "default": "World"},
    "count": {"type": "integer", "default": 1}
  },
  "required": []
}
```

推断规则：

| Python 类型 | JSON Schema | 备注 |
|-------------|-------------|------|
| `str` | `"string"` | |
| `int` | `"integer"` | |
| `float` | `"number"` | |
| `bool` | `"boolean"` | |
| `dict` | `"object"` | |
| `list` | `"array"` | |
| `Optional[X]` | `["<type>", "null"]` | |
| `Annotated[X, "desc"]` | 提取 description | |

- 有默认值 → 不加入 `required`，写入 `default`
- 无默认值 → 加入 `required`
- `self`, `cls`, `**kwargs`, `_ctx` 自动跳过

**方式二：Pydantic Model**

```python
from pydantic import BaseModel, Field

class ProcessParams(BaseModel):
    data: str = Field(description="要处理的数据")
    format: str = Field(default="json", description="输出格式")

@plugin_entry(id="process", params=ProcessParams)
def process(self, data: str, format: str = "json", **_):
    ...
```

**方式三：显式 JSON Schema**

```python
@plugin_entry(
    id="process",
    input_schema={
        "type": "object",
        "properties": {
            "data": {"type": "string", "description": "要处理的数据"},
            "format": {"type": "string", "enum": ["json", "xml"], "default": "json"},
        },
        "required": ["data"],
    },
)
def process(self, data: str, format: str = "json", **_):
    ...
```

:::{note}
三种方式的优先级：显式 `input_schema` > `params` Model > 自动推断。
:::

### 异步支持

```python
@plugin_entry(id="fetch")
async def fetch(self, url: str, **_):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return ok(data={"text": await resp.text()})
```

## @lifecycle

定义 **生命周期事件** 处理器。系统会在对应阶段自动调用。

```python
from plugin.sdk import lifecycle

@lifecycle(id="startup")
def on_startup(self, **_):
    self.logger.info("Plugin starting...")
    return {"status": "ready"}

@lifecycle(id="shutdown")
def on_shutdown(self, **_):
    self.logger.info("Plugin stopping...")
    return {"status": "stopped"}

@lifecycle(id="reload")
def on_reload(self, **_):
    self.logger.info("Plugin reloading config...")
    return {"status": "reloaded"}

@lifecycle(id="freeze")
def on_freeze(self, **_):
    self.logger.info("Freezing state...")

@lifecycle(id="unfreeze")
def on_unfreeze(self, **_):
    self.logger.info("Restored from freeze!")
```

| 生命周期 ID | 触发时机 | 说明 |
|-------------|---------|------|
| `startup` | 插件加载后 | 初始化资源 |
| `shutdown` | 插件关闭前 | 清理资源 |
| `reload` | 配置重载时 | 重新加载配置 |
| `freeze` | 状态冻结前 | 保存前的准备 |
| `unfreeze` | 状态恢复后 | 恢复后的处理 |

## @timer_interval

定义 **定时任务**，按固定间隔执行。

```python
from plugin.sdk import timer_interval

@timer_interval(
    id="cleanup",
    seconds=3600,           # 每小时
    name="Cleanup Task",
    auto_start=True,        # 插件加载后自动开始
)
def cleanup(self, **_):
    self.logger.info("Running cleanup...")
    return {"cleaned": True}
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `id` | `str` | 定时任务 ID |
| `seconds` | `float` | 执行间隔（秒） |
| `auto_start` | `bool` | 是否自动启动 |

:::{important}
- 定时任务在独立线程中运行
- 异常不会中断定时器，会记录日志并继续
- 支持同步和异步函数
:::

## @message

定义 **消息事件** 处理器，用于处理来自主系统的消息。

```python
from plugin.sdk import message

@message(
    id="handle_chat",
    source="chat",          # 消息来源过滤
    auto_start=True,
)
def handle_chat(self, text: str, sender: str, **_):
    self.logger.info(f"Message from {sender}: {text}")
    return {"handled": True}
```

## @on_event

通用事件装饰器，可以定义自定义事件类型。

```python
from plugin.sdk import on_event

@on_event(
    event_type="custom_event",
    id="my_handler",
    kind="hook",
)
def my_handler(self, event_data: str, **_):
    return {"processed": True}
```

## @custom_event

`@on_event` 的快捷方式，`event_type` 固定为 `"custom_event"`。

```python
from plugin.sdk import custom_event

@custom_event(id="my_custom")
def my_custom(self, **_):
    return {"ok": True}
```

## @worker

将入口点标记为 **Worker 模式**（在独立线程池中执行，不阻塞主命令循环）。

```python
from plugin.sdk import worker, plugin_entry

@worker(timeout=60.0, priority=0)
@plugin_entry(id="heavy_task")
def heavy_task(self, **_):
    # 长时间运行的任务
    import time
    time.sleep(30)
    return {"done": True}
```

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `timeout` | `float` | `30.0` | 超时时间（秒） |
| `priority` | `int` | `0` | 优先级 |

## EntryKind 类型

`kind` 参数的可选值：

| Kind | 说明 |
|------|------|
| `"action"` | 动作型入口（默认），一次性执行 |
| `"service"` | 服务型入口，持续运行 |
| `"hook"` | Hook 入口 |
| `"custom"` | 自定义类型 |
| `"lifecycle"` | 生命周期（由 `@lifecycle` 自动设置） |
| `"consumer"` | 消费者（由 `@message` 自动设置） |
| `"timer"` | 定时器（由 `@timer_interval` 自动设置） |
