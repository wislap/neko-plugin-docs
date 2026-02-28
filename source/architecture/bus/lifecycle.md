# 生命周期 (Lifecycle)

生命周期记录插件的启停、状态变更等系统级事件。

## LifecycleRecord

```python
@dataclass(frozen=True, slots=True)
class LifecycleRecord(BusRecord):
    lifecycle_id: Optional[str] = None
    detail: Optional[Dict[str, Any]] = None
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `lifecycle_id` | 生命周期事件 ID |
| `detail` | 详细信息（如状态变更的前后值） |

## LifecycleClient

通过 `self.ctx.bus.lifecycle` 访问。

```python
# 获取最近生命周期事件
lc = self.ctx.bus.lifecycle.get(max_count=20)

# 按插件过滤
lc = self.ctx.bus.lifecycle.get(plugin_id="my_plugin")
```

## 常见事件类型

| type | 说明 |
|------|------|
| `"startup"` | 插件启动 |
| `"shutdown"` | 插件关闭 |
| `"reload"` | 配置重载 |
| `"freeze"` | 状态冻结 |
| `"unfreeze"` | 状态恢复 |
| `"error"` | 运行时错误 |
