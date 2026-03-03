# BusList 操作

`BusList` 是所有 Bus Client 返回的数据容器，提供链式查询和集合运算。

## 核心特性

- **不可变**：所有操作返回新的 BusList，不修改原始数据
- **链式调用**：支持 `.filter().sort(by="timestamp").limit(20)` 式组合
- **集合去重**：`merge/intersect/difference` 按 Record 唯一键去重
- **可重放计划**：结构化操作可用于 `reload()` / `watch()`

## 过滤

```python
msgs = client.get(max_count=100)

# 精确匹配
by_plugin = msgs.filter(plugin_id="my_plugin")
by_type = msgs.filter(type="text")
by_priority = msgs.filter(priority_min=5)

# 正则匹配
by_pattern = msgs.filter(plugin_id_re="chat_.*")
by_content = msgs.filter(content_re="error|fail")

# 时间范围
import time
recent = msgs.filter(since_ts=time.time() - 3600)  # 最近 1 小时

# 组合过滤（AND 关系）
filtered = msgs.filter(plugin_id="chat", priority_min=5, type="text")
```

## 排序

```python
# 按时间戳排序（默认升序）
by_time = msgs.sort(by="timestamp")

# 降序
by_time_desc = msgs.sort(by="timestamp", reverse=True)

# 按优先级排序
by_priority = msgs.sort(by="priority", reverse=True)
```

## 去重与唯一键

集合运算（`merge` / `intersect` / `difference`）使用以下顺序计算唯一 key：
1. Record 专属 ID（`message_id`, `event_id`, `lifecycle_id`）
2. `trace_id`
3. `dump()` 指纹（最后手段）

## 集合运算

```python
# 合并两个列表（按唯一键去重）
combined = list1.merge(list2)

# 交集
common = list1.intersect(list2)

# 差集
only_in_1 = list1.difference(list2)
```

## 访问元素

```python
# 获取第一条
first = msgs[0] if len(msgs) > 0 else None

# 转为 record 列表
records = msgs.dump_records()

# 转为可序列化 dict 列表
payloads = msgs.dump()

# 长度
count = len(msgs)
# 或
count2 = msgs.count()

# 迭代
for record in msgs:
    print(record.content)
```

## 内部实现

`BusList` 底层基于 `BusListCore`，支持：

- **Plan 机制**：记录可重放操作链，用于增量更新和 Watcher
- **Replay 缓存**：避免重复 RPC 调用
- **二进制序列化**：高效传输
