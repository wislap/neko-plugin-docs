# 插件注册表

`core/registry.py` 管理所有插件的注册、发现和依赖解析。

## 功能

| 功能 | 说明 |
|------|------|
| 插件发现 | 扫描 `plugin/plugins/` 目录 |
| 元数据解析 | 解析 `plugin.toml` |
| SDK 版本检查 | 检查兼容性（recommended / supported / untested / conflicts） |
| 入口点收集 | 扫描所有 `@plugin_entry` 装饰的方法 |
| 依赖解析 | `core/dependency.py` 处理插件间依赖 |

## 插件发现流程

```{mermaid}
flowchart TD
    A[扫描 plugins/ 目录] --> B[解析 plugin.toml]
    B --> C{SDK 版本兼容?}
    C -->|recommended| D[正常注册]
    C -->|supported| E[警告 + 注册]
    C -->|untested| F[强警告 + 注册]
    C -->|conflicts 或不支持| G[拒绝加载]
    D --> H[收集入口点]
    E --> H
    F --> H
    H --> I[注册到全局状态]
```

## 入口点收集

通过反射扫描插件类上的装饰器：

- `@plugin_entry` → `EventHandler` (kind="action"/"service"/...)
- `@lifecycle` → `EventHandler` (kind="lifecycle")
- `@timer_interval` → `EventHandler` (kind="timer")
- `@message` → `EventHandler` (kind="consumer")
- `@hook` → `HookHandler`

## 依赖解析

`core/dependency.py` 处理插件间的启动顺序依赖：

- 拓扑排序确定启动顺序
- 循环依赖检测
- 可选依赖和强依赖

## 查询注册表

```python
# 通过全局状态查询
from plugin.core.state import state

# 获取插件列表
plugins = state.plugins

# 检查插件是否存在
exists = state.has_plugin("my_plugin")

# 获取插件信息
info = state.get_plugin("my_plugin")
```
