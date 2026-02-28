# 数据库

N.E.K.O 提供两种数据持久化方案：`PluginDatabase`（SQLAlchemy ORM）和 `PluginKVStore`（键值存储）。

## PluginDatabase

基于 SQLAlchemy 的完整 ORM 支持，自动管理数据库文件和 Session。

### 初始化

```python
from plugin.sdk import NekoPluginBase, neko_plugin, PluginDatabase
from sqlalchemy import Column, Integer, String, select

@neko_plugin
class MyPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.db = PluginDatabase(
            plugin_id=ctx.plugin_id,
            plugin_dir=ctx.config_path.parent,
            logger=ctx.logger,
        )
```

### 定义模型

```python
class User(self.db.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100))
```

### 创建表

```python
@lifecycle(id="startup")
def on_startup(self, **_):
    self.db.create_all()
```

### 同步操作

```python
@plugin_entry()
def add_user(self, name: str, email: str, **_):
    with self.db.session() as session:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        return ok(data={"id": user.id})
```

### 异步操作

```python
@plugin_entry()
async def list_users(self, **_):
    async with self.db.async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return ok(data={"users": [{"id": u.id, "name": u.name} for u in users]})
```

## PluginKVStore

基于 SQLite 的简单键值存储，适合轻量数据。

```python
from plugin.sdk import PluginDatabase

# PluginKVStore 通过 PluginDatabase 获取
kv = self.db.kv_store

# 设置值
kv.set("last_run", "2024-01-01T00:00:00Z")
kv.set("counter", "42")

# 获取值
value = kv.get("last_run")  # → "2024-01-01T00:00:00Z"
value = kv.get("missing", default="N/A")  # → "N/A"

# 删除
kv.delete("counter")

# 列出所有键
keys = kv.keys()
```

:::{note}
KVStore 的值都是字符串类型。复杂数据请用 JSON 序列化。
:::

## 选型建议

| 场景 | 推荐 |
|------|------|
| 简单配置、计数器 | `PluginKVStore` |
| 结构化数据、关联查询 | `PluginDatabase` (SQLAlchemy) |
| 需要持久化的运行状态 | `__freezable__` (状态持久化) |
