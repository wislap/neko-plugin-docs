# 第一个插件

本教程将带你从零创建一个完整的 Hello World 插件。

## 步骤 1：创建插件目录

```bash
mkdir -p plugin/plugins/hello_world
```

## 步骤 2：创建配置文件

创建 `plugin/plugins/hello_world/plugin.toml`：

```toml
[plugin]
id = "hello_world"
name = "Hello World Plugin"
description = "一个简单的示例插件"
version = "1.0.0"
entry = "plugins.hello_world:HelloWorldPlugin"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"
supported = ">=0.1.0,<0.3.0"
```

## 步骤 3：编写插件代码

创建 `plugin/plugins/hello_world/__init__.py`：

```python
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok


@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    """Hello World 插件示例"""

    def __init__(self, ctx):
        super().__init__(ctx)
        self.call_count = 0

    @lifecycle(id="startup")
    def on_startup(self, **_):
        """插件启动时执行"""
        self.logger.info("HelloWorldPlugin started!")
        return {"status": "ready"}

    @lifecycle(id="shutdown")
    def on_shutdown(self, **_):
        """插件关闭时执行"""
        self.logger.info(f"HelloWorldPlugin stopped. Total calls: {self.call_count}")
        return {"status": "stopped"}

    @plugin_entry(
        id="greet",
        name="Greet",
        description="返回问候语",
    )
    def greet(self, name: str = "World", **_):
        """问候函数"""
        self.call_count += 1
        message = f"Hello, {name}!"
        self.logger.info(f"Greeting: {message}")
        return ok(data={"message": message, "call_count": self.call_count})
```

### 代码解析

| 部分 | 说明 |
|------|------|
| `@neko_plugin` | 标记类为 N.E.K.O 插件 |
| `NekoPluginBase` | 插件基类，提供 `logger`、`config`、`plugins` 等属性 |
| `@lifecycle(id="startup")` | 插件启动时自动调用 |
| `@plugin_entry(id="greet")` | 定义外部可调用的入口点 |
| `ok(data=...)` | 返回标准成功响应 |
| `**_` | 捕获额外参数（推荐写法） |

## 步骤 4：测试插件

启动插件服务器后，通过 HTTP API 调用：

```bash
curl -X POST http://localhost:8000/plugin/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "hello_world",
    "entry_id": "greet",
    "args": {"name": "N.E.K.O"}
  }'
```

预期响应：

```json
{
  "success": true,
  "code": 0,
  "data": {
    "message": "Hello, N.E.K.O!",
    "call_count": 1
  }
}
```

## 简化写法

SDK 支持多种简化方式，减少样板代码：

### 省略 id（自动推断）

```python
@plugin_entry()  # id 自动为 "greet"
def greet(self, name: str = "World"):
    return ok(data={"message": f"Hello, {name}!"})
```

### 省略 schema（自动推断）

```python
@plugin_entry(id="greet")  # input_schema 从函数签名自动生成
def greet(self, name: str = "World", count: int = 1):
    return ok(data={"message": f"Hello, {name}! x{count}"})
```

自动推断规则：

| Python 类型 | JSON Schema 类型 |
|-------------|------------------|
| `str` | `string` |
| `int` | `integer` |
| `float` | `number` |
| `bool` | `boolean` |
| `dict` | `object` |
| `list` | `array` |
| `Optional[X]` | `["<type>", "null"]` |
| `Annotated[X, "desc"]` | 提取 description |

### 使用 Pydantic Model

```python
from pydantic import BaseModel

class GreetParams(BaseModel):
    name: str = "World"
    count: int = 1

@plugin_entry(id="greet", params=GreetParams)
def greet(self, name: str = "World", count: int = 1, **_):
    return ok(data={"message": f"Hello, {name}! x{count}"})
```

:::{seealso}
了解 [项目结构](project-structure.md) 中 `plugin.toml` 的完整配置选项。
:::
