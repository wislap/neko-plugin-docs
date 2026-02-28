# 全局状态机

`core/state.py` 维护整个插件系统的全局状态，是一个单例对象。

## 状态对象

```python
from plugin.core.state import state
```

`state` 是全局单例，所有组件共享同一个实例。

## 主要属性

| 属性 | 说明 |
|------|------|
| `plugins` | 已注册的插件字典 |
| `running_plugins` | 正在运行的插件集合 |
| `app` | FastAPI 应用实例 |

## 插件状态查询

```python
# 检查插件是否注册
if state.has_plugin("my_plugin"):
    ...

# 获取插件信息
info = state.get_plugin("my_plugin")

# 获取所有插件列表
all_plugins = state.list_plugins()

# 检查插件是否正在运行
is_running = state.is_running("my_plugin")
```

## 状态更新

状态更新由 Host 和 Registry 在插件生命周期中自动管理：

```{mermaid}
sequenceDiagram
    participant R as Registry
    participant S as State
    participant H as Host

    R->>S: register_plugin(info)
    H->>S: set_running(plugin_id)
    Note over S: 插件运行中...
    H->>S: set_stopped(plugin_id)
    R->>S: unregister_plugin(plugin_id)
```

## 线程安全

State 对象使用锁保护共享数据，支持多线程并发访问。所有修改操作都是原子的。

## 与其他模块的关系

| 模块 | 使用方式 |
|------|---------|
| `registry.py` | 注册/注销插件 |
| `host.py` | 更新运行状态 |
| `server/services.py` | 查询插件信息用于 trigger |
| `server/routes/` | HTTP API 返回插件列表 |
| `sdk/bus/` | 查询消息路由目标 |
