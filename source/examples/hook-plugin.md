# Hook 中间件插件

演示使用 Hook 实现验证、日志、响应转换。

## __init__.py

```python
import time
from plugin.sdk import (
    NekoPluginBase, neko_plugin, PluginRouter,
    plugin_entry, hook, before_entry, after_entry, around_entry,
    ok, fail,
)


class HookRouter(PluginRouter):
    # ── before: 参数验证 ──
    @before_entry(target="save", priority=10)
    async def validate_save(self, params, **_):
        if not params.get("name"):
            return fail(message="name is required")
        if len(params.get("name", "")) > 100:
            return fail(message="name too long (max 100)")
        return None  # 继续执行

    # ── around: 性能计时 ──
    @around_entry(target="*")
    async def timing(self, entry_id, proceed, **_):
        start = time.time()
        result = await proceed()
        elapsed = time.time() - start
        self.logger.info(f"[timing] {entry_id} took {elapsed:.3f}s")
        return result

    # ── after: 响应增强 ──
    @after_entry(target="*")
    async def add_metadata(self, entry_id, result, **_):
        if isinstance(result, dict) and "data" in result:
            result["data"]["_entry_id"] = entry_id
            result["data"]["_timestamp"] = time.time()
        return None  # 使用原始 result（已就地修改）

    # ── 业务入口 ──
    @plugin_entry()
    def save(self, name: str, value: str = "", **_):
        return ok(data={"saved": True, "name": name, "value": value})

    @plugin_entry()
    def query(self, key: str = "", **_):
        return ok(data={"key": key, "found": True})


@neko_plugin
class HookDemoPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.include_router(HookRouter())
```

## 执行流程

调用 `save` 时：

```
1. validate_save (before, priority=10) → 检查 name
2. timing (around, *) → 开始计时
3. save() → 执行业务
4. timing → 记录耗时
5. add_metadata (after, *) → 添加 _entry_id, _timestamp
```

调用 `query` 时：

```
1. timing (around, *) → 开始计时
2. query() → 执行业务
3. timing → 记录耗时
4. add_metadata (after, *) → 添加 _entry_id, _timestamp
```

注意 `validate_save` 只对 `save` 生效（`target="save"`），`timing` 和 `add_metadata` 对所有入口生效（`target="*"`）。
