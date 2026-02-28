# 跨插件调用

`Plugins` 提供了插件间相互调用入口点的能力。通过 `self.plugins` 访问。

## 基本用法

### 同步调用

```python
result = self.plugins.call_entry(
    "target_plugin:entry_id",
    {"param1": "value1"},
    timeout=10.0,
)
```

### 异步调用

```python
result = await self.plugins.call_entry_async(
    "target_plugin:entry_id",
    {"param1": "value1"},
    timeout=10.0,
)
```

### 参数格式

调用格式为 `"plugin_id:entry_id"`：

```python
# 调用 timer_service 插件的 start_timer 入口
self.plugins.call_entry(
    "timer_service:start_timer",
    {
        "timer_id": "my_timer",
        "interval": 5.0,
        "callback_plugin_id": self.ctx.plugin_id,
        "callback_entry_id": "on_tick",
    },
    timeout=10.0,
)
```

## 超时

默认超时时间取决于系统配置。可以显式指定：

```python
# 长时间操作，设置较长超时
result = self.plugins.call_entry(
    "heavy_plugin:process",
    {"data": large_data},
    timeout=60.0,  # 60 秒
)
```

## 错误处理

```python
try:
    result = self.plugins.call_entry("other:api", {}, timeout=5.0)
except Exception as e:
    self.logger.error(f"Cross-plugin call failed: {e}")
```

常见错误：

| 错误 | 说明 |
|------|------|
| `PluginNotFoundError` | 目标插件不存在 |
| `PluginNotRunningError` | 目标插件未运行 |
| `PluginEntryNotFoundError` | 目标入口点不存在 |
| `PluginTimeoutError` | 调用超时 |
| `PluginExecutionError` | 目标入口执行出错 |

## CallChain 调用链追踪

SDK 内置调用链追踪，防止循环调用和死锁：

```python
from plugin.sdk import get_call_chain, get_call_depth, is_in_call_chain

@plugin_entry()
def my_entry(self, **_):
    # 查看当前调用链
    chain = get_call_chain()
    depth = get_call_depth()
    self.logger.info(f"Call chain: {chain}, depth: {depth}")

    # 检查是否在某个调用链中（防止循环）
    if is_in_call_chain("my_plugin:my_entry"):
        return fail(message="Circular call detected!")

    return ok()
```

| 函数 | 说明 |
|------|------|
| `get_call_chain()` | 获取当前调用链列表 |
| `get_call_depth()` | 获取当前调用深度 |
| `is_in_call_chain(id)` | 检查某个 ID 是否在调用链中 |

### 异常

| 异常 | 说明 |
|------|------|
| `CircularCallError` | 检测到循环调用 |
| `CallChainTooDeepError` | 调用链过深 |

:::{seealso}
调用链追踪的内部实现见 [系统架构 - 调用链追踪](../architecture/internals/call-chain.md)。
:::
