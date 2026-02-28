# 常见问题

## 插件开发

### 插件不加载？

1. 检查 `plugin.toml` 的 `entry` 字段是否正确（格式：`模块路径:类名`）
2. 检查 SDK 版本兼容性（`[plugin.sdk]` 配置）
3. 查看日志中是否有 `PluginLoadError` 或 `PluginImportError`
4. 确保 `__init__.py` 中的类使用了 `@neko_plugin` 装饰器

### 入口点调用无响应？

1. 确认入口点使用了 `@plugin_entry` 装饰器
2. 检查 `id` 是否与调用时的 `entry_id` 一致
3. 查看日志中是否有异常信息
4. 确认插件状态为 running

### 状态持久化不生效？

1. 确认 `__persist_mode__` 不是 `"off"`（默认值）
2. 确认属性名在 `__freezable__` 列表中
3. 检查属性类型是否支持序列化（基本类型 + EXTENDED_TYPES）
4. 如果使用 `"manual"` 模式，确认 `@plugin_entry(persist=True)`

### 跨插件调用超时？

1. 检查目标插件是否正在运行
2. 增大 `timeout` 参数
3. 使用异步版本 `call_entry_async` 避免阻塞
4. 检查是否存在循环调用（查看 CallChain 日志）

### 同步调用报死锁警告？

在 handler 中执行同步 IPC 调用会阻塞命令循环。解决方案：

- 使用异步版本：`call_entry_async`、`config.get_async`
- 或使用 `@worker` 装饰器将入口放到线程池执行

## Bus 系统

### Bus 数据为空？

1. 确认 Message Plane 已启动
2. 检查 ZeroMQ 端点配置
3. 确认有插件在发布数据
4. 检查过滤条件是否过于严格

### Watcher 回调不触发？

1. 确认 Message Plane PUB 端口正常
2. 检查 `debounce_ms` 是否设置过大
3. 确认回调函数已注册

## Run/Export

### Run 一直卡在 queued？

1. 确认插件已正常启动
2. 检查 Host 进程是否正常
3. 查看日志中是否有 trigger 错误

### Export 数据看不到？

1. 确认在 Run 执行上下文中调用 `ctx.export_push()`
2. 检查 `category` 参数（默认 `"user"`）
3. 通过 API `GET /runs/{run_id}/export` 查询

## 性能

### 插件响应慢？

1. 检查是否有同步阻塞操作（文件 IO、网络请求）
2. 使用 `@worker` 将长时间任务放到线程池
3. 使用异步函数（`async def`）处理 IO 密集型任务
4. 检查 Bus 查询的 `max_count` 是否过大

### 内存占用过高？

1. 检查 Bus 数据是否持续增长（TopicStore 有环形缓冲限制）
2. 检查 `__freezable__` 中是否有大对象
3. 确认 Run/Export 驱逐策略正常工作
