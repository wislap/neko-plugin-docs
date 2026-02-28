# 开发指南

本章按主题深入讲解 SDK 的各项功能，帮助你掌握插件开发的方方面面。

## 概览

N.E.K.O Plugin SDK 提供了一套完整的工具集：

| 主题 | 说明 |
|------|------|
| [装饰器](decorators.md) | `@neko_plugin`, `@plugin_entry`, `@lifecycle`, `@timer_interval` 等 |
| [上下文](context.md) | `PluginContext` — 日志、状态上报、消息推送 |
| [配置系统](config.md) | `PluginConfig` — 读写 `plugin.toml` |
| [响应格式](responses.md) | `ok()` / `fail()` 标准响应 + `ErrorCode` |
| [状态持久化](state.md) | `__freezable__`, freeze/unfreeze, 扩展类型 |
| [Hook 系统](hooks.md) | before / after / around / replace 中间件 |
| [路由器](router.md) | `PluginRouter` 模块化拆分 |
| [跨插件调用](plugins-call.md) | `Plugins.call_entry()` 插件间通信 |
| [数据库](database.md) | `PluginDatabase` (SQLAlchemy ORM) + `PluginKVStore` |
| [键值存储](store.md) | `PluginStore` 轻量存储 |

## 导入方式

所有 SDK 功能统一从 `plugin.sdk` 导入：

```python
from plugin.sdk import (
    # 核心
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle,
    # 响应
    ok, fail, ErrorCode,
    # 装饰器
    timer_interval, message, on_event, custom_event, worker,
    # Hook
    hook, before_entry, after_entry, around_entry, replace_entry,
    # 路由
    PluginRouter,
    # 工具
    PluginConfig, Plugins, SystemInfo, MemoryClient,
    # 状态
    PluginStatePersistence, EXTENDED_TYPES,
    # 数据库
    PluginDatabase, PluginKVStore, PluginStore,
)
```

```{toctree}
:maxdepth: 2

decorators
context
config
responses
state
hooks
router
plugins-call
database
store
```
