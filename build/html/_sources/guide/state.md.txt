# 状态持久化

N.E.K.O 支持自动保存和恢复插件状态（freeze/unfreeze 机制），让插件在重启后恢复到之前的状态。

## 核心概念

### __freezable__

声明需要持久化的属性名列表：

```python
@neko_plugin
class MyPlugin(NekoPluginBase):
    __freezable__ = ["counter", "cache", "user_prefs"]

    def __init__(self, ctx):
        super().__init__(ctx)
        self.counter = 0
        self.cache = {}
        self.user_prefs = {"theme": "dark"}
```

只有在 `__freezable__` 中声明的属性才会被保存和恢复。

### __persist_mode__

控制保存时机：

| 模式 | 说明 |
|------|------|
| `"auto"` | 每次 entry 执行后自动保存 |
| `"manual"` | 仅在 freeze 时保存，或 `@plugin_entry(persist=True)` 时保存 |
| `"off"` | 完全禁用（默认） |

```python
@neko_plugin
class MyPlugin(NekoPluginBase):
    __freezable__ = ["counter"]
    __persist_mode__ = "auto"  # 每次 entry 后自动保存
```

:::{important}
优先级：`plugin.toml` 中 `[plugin_state].persist_mode` > 类属性 `__persist_mode__` > 默认值 `"off"`
:::

### @plugin_entry(persist=True)

对单个入口点启用持久化（在 `manual` 模式下有用）：

```python
__persist_mode__ = "manual"

@plugin_entry(id="increment", persist=True)  # 执行后自动保存
def increment(self, value: int = 1):
    self.counter += value
    return ok(data={"counter": self.counter})

@plugin_entry(id="query")  # 不触发保存
def query(self):
    return ok(data={"counter": self.counter})
```

## 生命周期

```{mermaid}
sequenceDiagram
    participant S as System
    participant P as Plugin

    Note over S,P: 首次启动
    S->>P: startup
    P->>P: 初始化属性

    Note over S,P: 正常关闭
    S->>P: freeze
    P->>P: on_freeze() 回调
    S->>S: 保存 __freezable__ 到磁盘

    Note over S,P: 下次启动（检测到保存文件）
    S->>S: 从磁盘加载状态
    S->>P: startup（属性已恢复）
    S->>P: unfreeze
    P->>P: on_unfreeze() 回调
```

### freeze / unfreeze 回调

```python
@lifecycle(id="freeze")
def on_freeze(self, **_):
    self.logger.info("即将冻结...")
    # 可以在这里做清理，如关闭连接

@lifecycle(id="unfreeze")
def on_unfreeze(self, **_):
    self.logger.info("从冻结状态恢复!")
    self.logger.info(f"恢复的 counter = {self.counter}")
    # 可以在这里重新初始化资源
```

## 支持的类型 (EXTENDED_TYPES)

除了基本类型（str, int, float, bool, list, dict），还支持：

| 类型 | 说明 |
|------|------|
| `datetime` | 自动序列化为 ISO 格式 |
| `date` | 自动序列化为 ISO 格式 |
| `timedelta` | 序列化为秒数 |
| `Enum` | 保存枚举值和类路径 |
| `set` | 转为 list 保存 |
| `frozenset` | 转为 list 保存 |
| `Path` | 转为字符串保存 |
| `bytes` | Base64 编码保存 |
| `dataclass` | 转为 dict 保存 |

### 嵌套支持

支持嵌套的扩展类型：

```python
__freezable__ = ["tasks"]

# 列表中嵌套 datetime
self.tasks = [
    {"name": "task1", "created_at": datetime.now()},
    {"name": "task2", "created_at": datetime.now()},
]
# → 所有 datetime 都会被正确序列化和反序列化
```

## 完整示例

```python
from datetime import datetime
from enum import Enum
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok

class Priority(Enum):
    LOW = "low"
    HIGH = "high"

@neko_plugin
class StatefulPlugin(NekoPluginBase):
    __freezable__ = ["counter", "last_run", "priority", "tags"]
    __persist_mode__ = "auto"

    def __init__(self, ctx):
        super().__init__(ctx)
        self.counter = 0
        self.last_run = None
        self.priority = Priority.LOW
        self.tags = set()

    @lifecycle(id="unfreeze")
    def on_unfreeze(self, **_):
        self.logger.info(f"Restored: counter={self.counter}, tags={self.tags}")

    @plugin_entry()
    def increment(self, value: int = 1):
        self.counter += value
        self.last_run = datetime.now()
        return ok(data={"counter": self.counter})

    @plugin_entry()
    def add_tag(self, tag: str):
        self.tags.add(tag)
        return ok(data={"tags": list(self.tags)})
```
