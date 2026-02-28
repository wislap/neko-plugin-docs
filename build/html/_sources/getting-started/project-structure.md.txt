# 项目结构

## 插件目录布局

```
plugin/plugins/my_plugin/
├── __init__.py          # 插件主代码（必须）
├── plugin.toml          # 插件配置文件（必须）
├── config.json          # 自定义配置（可选）
├── routers/             # 路由器模块（可选）
│   ├── debug.py
│   └── admin.py
└── models/              # 数据模型（可选）
    └── user.py
```

只有 `__init__.py` 和 `plugin.toml` 是必需的。

## plugin.toml 详解

### 完整示例

```toml
[plugin]
id = "my_plugin"                    # 唯一标识符（必须）
name = "My Plugin"                  # 显示名称
description = "插件描述"            # 描述
version = "1.0.0"                   # 版本号
entry = "plugins.my_plugin:MyPlugin" # 入口点（必须）

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"     # 推荐 SDK 版本
supported = ">=0.1.0,<0.3.0"       # 支持的 SDK 版本
untested = ">=0.3.0,<0.4.0"        # 未测试但允许的版本
conflicts = ["<0.1.0", ">=0.4.0"]  # 冲突版本（拒绝加载）

[plugin_state]
persist_mode = "auto"               # 状态持久化模式

[adapter]                           # 仅 type="adapter" 的插件
mode = "gateway"
priority = 0
```

### 字段说明

#### `[plugin]` 基本信息

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `id` | string | ✅ | 插件唯一标识符，全局唯一 |
| `name` | string | | 显示名称 |
| `description` | string | | 插件描述 |
| `version` | string | | 语义化版本号 |
| `entry` | string | ✅ | 入口点，格式 `模块路径:类名` |

#### `[plugin.sdk]` SDK 版本兼容

| 字段 | 说明 |
|------|------|
| `recommended` | 推荐版本范围，不匹配时警告 |
| `supported` | 完全支持的版本范围，不匹配时拒绝加载（除非命中 `untested`） |
| `untested` | 未测试但允许加载的版本范围，命中时警告 |
| `conflicts` | 冲突版本列表，命中即拒绝加载 |

```{mermaid}
flowchart TD
    A[检查 SDK 版本] --> B{命中 conflicts?}
    B -->|是| C[拒绝加载]
    B -->|否| D{命中 supported?}
    D -->|是| E{命中 recommended?}
    E -->|是| F[正常加载]
    E -->|否| G[警告 + 加载]
    D -->|否| H{命中 untested?}
    H -->|是| I[警告 + 加载]
    H -->|否| C
```

#### `[plugin_state]` 状态持久化

| 字段 | 值 | 说明 |
|------|-----|------|
| `persist_mode` | `"auto"` | 每次 entry 执行后自动保存 |
| | `"manual"` | 仅 freeze 时保存，或 `@plugin_entry(persist=True)` |
| | `"off"` | 完全禁用（默认） |

:::{important}
优先级：`plugin.toml` 中的 `persist_mode` > 类属性 `__persist_mode__` > 默认值 `"off"`
:::

## 入口点格式

`entry` 字段格式为 `模块路径:类名`：

```toml
entry = "plugins.hello_world:HelloWorldPlugin"
#        ^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^
#        Python 模块导入路径     类名
```

等效于 Python 中的：

```python
from plugins.hello_world import HelloWorldPlugin
```
