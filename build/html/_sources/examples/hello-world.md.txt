# Hello World

最简单的插件，展示基础结构。

## plugin.toml

```toml
[plugin]
id = "hello_world"
name = "Hello World"
version = "1.0.0"
entry = "plugins.hello_world:HelloPlugin"
```

## __init__.py

```python
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok


@neko_plugin
class HelloPlugin(NekoPluginBase):

    @lifecycle(id="startup")
    def on_startup(self, **_):
        self.logger.info("Hello plugin ready!")

    @plugin_entry()
    def greet(self, name: str = "World"):
        return ok(data={"message": f"Hello, {name}!"})

    @plugin_entry()
    def add(self, a: int = 0, b: int = 0):
        return ok(data={"sum": a + b})
```

## 调用

```bash
# greet
curl -X POST http://localhost:8000/plugin/trigger \
  -H "Content-Type: application/json" \
  -d '{"plugin_id":"hello_world","entry_id":"greet","args":{"name":"N.E.K.O"}}'

# add
curl -X POST http://localhost:8000/plugin/trigger \
  -H "Content-Type: application/json" \
  -d '{"plugin_id":"hello_world","entry_id":"add","args":{"a":3,"b":5}}'
```
