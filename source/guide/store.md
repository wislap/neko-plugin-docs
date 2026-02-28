# 键值存储

`PluginStore` 提供插件级别的轻量键值存储。

## 基本用法

```python
from plugin.sdk import PluginStore

# 通过插件基类访问
store = self.store

# 设置
store.set("key", "value")

# 获取
value = store.get("key")
value = store.get("missing", default="fallback")

# 删除
store.delete("key")

# 检查是否存在
exists = store.has("key")

# 列出所有键
keys = store.keys()
```

## 与其他存储方式对比

| 方式 | 持久化 | 结构 | 适用场景 |
|------|--------|------|----------|
| `PluginStore` | 是 | 键值 | 配置项、标志位 |
| `PluginKVStore` | 是 | 键值 (SQLite) | 同上，基于数据库 |
| `PluginDatabase` | 是 | ORM 表 | 结构化数据 |
| `__freezable__` | 是 | 属性 | 运行时状态 |
| 内存变量 | 否 | 任意 | 临时缓存 |
