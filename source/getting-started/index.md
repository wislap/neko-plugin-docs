# 快速上手

欢迎来到 N.E.K.O 插件开发！本章将帮助你在 **5 分钟内** 创建并运行第一个插件。

## 什么是 N.E.K.O 插件系统？

N.E.K.O 插件系统是一个基于 Python 的插件框架，允许开发者创建可扩展的功能模块。核心设计理念：

- **进程隔离**：每个插件运行在独立进程中，崩溃不会影响主系统
- **异步优先**：同步和异步函数均可，框架自动适配
- **声明式 API**：通过装饰器定义入口点、生命周期、Hook 等
- **实时通信**：Bus 系统提供消息、事件、生命周期等多种数据流
- **类型安全**：Pydantic 验证 + Python 类型提示

## 架构总览

```
┌─────────────────────────────────────────┐
│         主进程 (Main Process)            │
│  ┌───────────────────────────────────┐  │
│  │   Plugin Server (FastAPI)         │  │
│  │   - HTTP API 端点                 │  │
│  │   - 插件注册表                    │  │
│  │   - Run/Export 管理               │  │
│  │   - Message Plane                 │  │
│  └───────────────────────────────────┘  │
└───────────────┬─────────────────────────┘
                │ IPC (ZeroMQ)
    ┌───────────┼───────────┬─────────────┐
    │           │           │             │
    ▼           ▼           ▼             ▼
┌────────┐ ┌────────┐ ┌────────┐   ┌──────────┐
│Plugin A│ │Plugin B│ │Plugin C│   │ Adapter  │
│Process │ │Process │ │Process │   │ Process  │
└────────┘ └────────┘ └────────┘   └──────────┘
```

## 最小示例

```python
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, ok

@neko_plugin
class HelloPlugin(NekoPluginBase):
    @plugin_entry()
    def greet(self, name: str = "World"):
        return ok(data={"message": f"Hello, {name}!"})
```

:::{tip}
`@plugin_entry()` 不传 `id` 时，自动使用函数名 `greet` 作为入口点 ID。
不传 `input_schema` 时，自动从函数签名推断 JSON Schema。
:::

```{toctree}
:maxdepth: 2

installation
first-plugin
project-structure
```
