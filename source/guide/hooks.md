# Hook 系统

Hook 系统提供了 **中间件** 能力，可以在入口点执行前后插入自定义逻辑，支持插件内和跨插件。

## 四种 Hook 时机

| 时机 | 装饰器 | 说明 |
|------|--------|------|
| **before** | `@before_entry` | 入口执行前，可拦截 |
| **after** | `@after_entry` | 入口执行后，可修改结果 |
| **around** | `@around_entry` | 包裹入口，完全控制执行流 |
| **replace** | `@replace_entry` | 替换入口，原始入口不执行 |

## @before_entry

在目标入口执行 **之前** 运行。返回非 `None` 值可阻止原始入口执行。

```python
from plugin.sdk import before_entry, fail

@before_entry(target="save", priority=10)
async def validate_save(self, params, **_):
    if not params.get("name"):
        return fail(message="name is required")  # 阻止执行
    return None  # 返回 None → 继续执行原始入口
```

## @after_entry

在目标入口执行 **之后** 运行。可以读取和修改结果。

```python
from plugin.sdk import after_entry

@after_entry(target="query")
async def log_query_result(self, entry_id, result, **_):
    self.logger.info(f"{entry_id} returned: {result}")
    return None  # 返回 None → 使用原始结果
```

## @around_entry

**包裹** 目标入口，完全控制执行流。必须手动调用 `proceed()` 来执行原始入口。

```python
from plugin.sdk import around_entry
import time

@around_entry(target="*")  # 匹配所有入口
async def timing(self, entry_id, proceed, **_):
    start = time.time()
    result = await proceed()  # 执行原始入口
    elapsed = time.time() - start
    self.logger.info(f"{entry_id} took {elapsed:.3f}s")
    return result
```

## @replace_entry

**替换** 目标入口，原始入口完全不执行。

```python
from plugin.sdk import replace_entry, ok

@replace_entry(target="deprecated_api")
async def redirect(self, params, **_):
    return ok(data={"message": "This API has been replaced"})
```

## @hook（通用装饰器）

以上四种快捷方式底层都是 `@hook`：

```python
from plugin.sdk import hook

@hook(target="save", timing="before", priority=10)
async def validate(self, params, **_):
    ...

@hook(target="*", timing="around")
async def log_all(self, entry_id, proceed, **_):
    ...
```

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `target` | `str` | 目标入口 ID，`"*"` 匹配所有 |
| `timing` | `HookTiming` | `"before"` / `"after"` / `"around"` / `"replace"` |
| `priority` | `int` | 优先级，数字越小越先执行（默认 0） |

## 在 PluginRouter 中使用

Hook 在路由器中同样有效：

```python
from plugin.sdk import PluginRouter, hook, before_entry, ok, fail

class ValidationRouter(PluginRouter):
    @hook(target="*", timing="before")
    async def log_all(self, entry_id, params, **_):
        self.logger.info(f"Calling {entry_id} with {params}")
        return None

    @before_entry(target="save", priority=10)
    async def validate(self, params, **_):
        if not params.get("name"):
            return fail(message="name required")
        return None
```

## 执行顺序

```{mermaid}
sequenceDiagram
    participant C as Caller
    participant B as before hooks
    participant E as Entry
    participant A as after hooks

    C->>B: 调用入口
    Note over B: priority 从小到大执行
    alt before hook 返回非 None
        B-->>C: 拦截，返回 hook 结果
    else 全部返回 None
        B->>E: 执行入口
        E->>A: 返回结果
        Note over A: priority 从小到大执行
        A-->>C: 返回最终结果
    end
```

对于 `around` Hook，执行流程为：

```
around_hook_1 → around_hook_2 → ... → 原始入口 → ... → around_hook_2 → around_hook_1
```

每个 `around` hook 通过 `await proceed()` 调用下一层。
