# 配置系统

`PluginConfig` 提供了对 `plugin.toml` 的读写访问，支持点分路径和同步/异步操作。

通过 `self.config` 访问。

## 读取配置

### 获取单个值

```python
# 同步
value = self.config.get("debug.timer.interval_seconds")

# 异步
value = await self.config.get_async("debug.timer.interval_seconds")
```

### 获取带默认值

```python
value = self.config.get("debug.enabled", default=False)
```

### 获取整个配置

```python
# 同步 - 导出全部配置
all_config = self.config.dump()

# 异步
all_config = await self.config.dump_async()
```

## 写入配置

### 设置单个值

```python
# 同步
self.config.set("debug.timer.interval_seconds", 5.0)

# 异步
await self.config.set_async("debug.timer.interval_seconds", 5.0)
```

### 点分路径

配置通过 `.` 分隔层级，自动创建中间节点：

```python
# 以下操作对应 toml 中的：
# [debug]
#   [debug.timer]
#     interval_seconds = 5.0
self.config.set("debug.timer.interval_seconds", 5.0)
```

## 错误处理

```python
from plugin.sdk.config import PluginConfigError

try:
    value = self.config.get("nonexistent.path")
except PluginConfigError as e:
    self.logger.error(f"Config error: {e}, path={e.path}, op={e.operation}")
```

| 异常 | 说明 |
|------|------|
| `PluginConfigError` | 配置路径无效或键不存在 |

## 示例：启动时加载配置

```python
@lifecycle(id="startup")
def on_startup(self, **_):
    # 从 toml 读取配置
    cfg = self.config.dump()
    debug_cfg = cfg.get("debug", {})

    self.enabled = debug_cfg.get("enabled", False)
    self.interval = debug_cfg.get("interval_seconds", 3.0)

    # 写入启动时间
    from datetime import datetime, timezone
    self.config.set("debug.loaded_at", datetime.now(timezone.utc).isoformat())
```
