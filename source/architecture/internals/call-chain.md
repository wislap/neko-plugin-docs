# 调用链追踪

SDK 内置调用链追踪机制，防止跨插件调用时的循环依赖和死锁。

## 工作原理

每次跨插件调用都会在调用链中记录一个节点：

```
Plugin A → Plugin B → Plugin C
```

如果 Plugin C 试图调用 Plugin A，就形成了循环，会抛出 `CircularCallError`。

## API

```python
from plugin.sdk import (
    CallChain, AsyncCallChain,
    get_call_chain, get_call_depth, is_in_call_chain,
    CircularCallError, CallChainTooDeepError,
)
```

### 查询当前调用链

```python
chain = get_call_chain()     # → ["plugin_a:entry_x", "plugin_b:entry_y"]
depth = get_call_depth()     # → 2
```

### 检查循环

```python
if is_in_call_chain("plugin_a:entry_x"):
    # 检测到潜在循环
    return fail(message="Would cause circular call")
```

## 异常

### CircularCallError

```python
# 当调用链形成环时自动抛出
# A → B → C → A (循环!)
raise CircularCallError(chain=["A:x", "B:y", "C:z", "A:x"])
```

### CallChainTooDeepError

```python
# 当调用链深度超过限制时抛出
raise CallChainTooDeepError(depth=20, max_depth=16)
```

## 同步 vs 异步

| 类 | 用途 |
|---|------|
| `CallChain` | 同步调用链追踪（基于 threading.local） |
| `AsyncCallChain` | 异步调用链追踪（基于 contextvars） |

## 死锁检测

`core/deadlock_detector.py` 提供更深层的死锁检测：

- 监控插件间的等待关系
- 检测等待图中的环
- 超时时自动中断并报告
