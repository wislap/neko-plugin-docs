# N.E.K.O Plugin SDK

**构建强大、可扩展的 AI 插件系统**

N.E.K.O 插件系统是一个基于 Python 的插件框架，为 AI 助手提供可扩展的功能模块。
每个插件运行在独立进程中，通过高性能消息通道与主系统交互。

---

::::{grid} 2 2 3 3
:gutter: 3

:::{grid-item-card} 🚀 快速上手
:link: getting-started/index
:link-type: doc

5 分钟创建你的第一个插件
:::

:::{grid-item-card} 📖 开发指南
:link: guide/index
:link-type: doc

按主题深入学习 SDK 全部功能
:::

:::{grid-item-card} 🏗️ 系统架构
:link: architecture/index
:link-type: doc

Bus / Run / MessagePlane / Adapter 深入
:::

:::{grid-item-card} 💡 完整示例
:link: examples/index
:link-type: doc

从 Hello World 到 MCP Adapter
:::

:::{grid-item-card} 📚 API 参考
:link: reference/index
:link-type: doc

autodoc 自动生成的精确 API 文档
:::

:::{grid-item-card} ❓ 常见问题
:link: faq
:link-type: doc

FAQ & 故障排查
:::

::::

---

## 核心特性

| 特性 | 说明 |
|------|------|
| **进程隔离** | 每个插件运行在独立进程中，互不影响 |
| **异步支持** | 同步和异步函数均可，自动适配 |
| **类型安全** | Pydantic 数据验证 + Python 类型提示 |
| **实时 Bus** | 消息 / 事件 / 生命周期 / 对话 / 记忆五大数据流 |
| **Run/Export** | 任务执行生命周期管理 + 多格式导出通道 |
| **状态持久化** | freeze/unfreeze 自动保存恢复，支持扩展类型 |
| **Hook 系统** | before / after / around / replace 四种中间件 |
| **Adapter** | Gateway / Router / Bridge / Hybrid 四种协议适配模式 |
| **高性能消息平面** | ZeroMQ 三端口架构，环形缓冲 + 增量推送 |

## 架构概览

```{mermaid}
graph TB
    subgraph Main["主进程"]
        Server["Plugin Server<br/>(FastAPI)"]
        Registry["注册表"]
        RunMgr["Run Manager"]
        MP["Message Plane<br/>(ZeroMQ)"]
    end

    subgraph Plugins["插件进程"]
        P1["Plugin A"]
        P2["Plugin B"]
        P3["Adapter"]
    end

    Server --> Registry
    Server --> RunMgr
    Server --> MP
    P1 <-->|IPC| Server
    P2 <-->|IPC| Server
    P3 <-->|IPC| Server
    P1 <-.->|Bus| MP
    P2 <-.->|Bus| MP
    P3 <-.->|Bus| MP

    External["外部协议<br/>(MCP/HTTP/WS)"] --> P3
```

## 快速一览

```python
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok

@neko_plugin
class MyPlugin(NekoPluginBase):
    @lifecycle(id="startup")
    def on_startup(self):
        self.logger.info("Plugin started!")

    @plugin_entry()
    def greet(self, name: str = "World"):
        return ok(data={"message": f"Hello, {name}!"})
```

---

```{toctree}
:maxdepth: 2
:hidden:

getting-started/index
guide/index
architecture/index
examples/index
reference/index
faq
```
