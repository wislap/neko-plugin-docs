# 完整示例

本章提供可运行的完整示例，覆盖各种实际场景。

## 示例列表

| 示例 | 难度 | 涉及功能 |
|------|------|----------|
| [Hello World](hello-world.md) | ⭐ | 基础插件结构 |
| [文件处理](file-processor.md) | ⭐⭐ | lifecycle + timer + push_message |
| [API 客户端](api-client.md) | ⭐⭐ | async + batch + semaphore |
| [数据采集](data-collector.md) | ⭐⭐ | timer + config + push |
| [状态持久化](stateful-plugin.md) | ⭐⭐⭐ | freeze/unfreeze + EXTENDED_TYPES |
| [路由器模块化](router-plugin.md) | ⭐⭐⭐ | 多 Router + prefix |
| [Hook 中间件](hook-plugin.md) | ⭐⭐⭐ | validate + log + transform |
| [Bus 实时监听](bus-watcher.md) | ⭐⭐⭐⭐ | Watcher + Delta |
| [Run 进度上报](run-progress.md) | ⭐⭐⭐⭐ | export_push + progress |
| [MCP Adapter](mcp-adapter.md) | ⭐⭐⭐⭐⭐ | Gateway Core + TransportAdapter |

```{toctree}
:maxdepth: 1

hello-world
file-processor
api-client
data-collector
stateful-plugin
router-plugin
hook-plugin
bus-watcher
run-progress
mcp-adapter
```
