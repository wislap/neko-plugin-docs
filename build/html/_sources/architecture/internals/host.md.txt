# Host 进程

`core/host.py` 是插件系统中最大的模块，管理插件子进程的完整生命周期。

## 职责

| 功能 | 说明 |
|------|------|
| 子进程管理 | 启动、停止、重启插件进程 |
| 命令分发 | 将 trigger/lifecycle 命令路由到正确的插件 |
| 状态同步 | 收集插件状态上报 |
| 消息路由 | 处理插件间消息传递 |
| 异常处理 | 子进程崩溃检测和重启 |

## 插件进程生命周期

```{mermaid}
stateDiagram-v2
    [*] --> Loading: load_plugin()
    Loading --> Starting: 进程创建
    Starting --> Running: startup 完成
    Running --> Freezing: freeze 请求
    Freezing --> Frozen: 状态保存完成
    Frozen --> Unfreezing: unfreeze 请求
    Unfreezing --> Running: 状态恢复
    Running --> Stopping: shutdown 请求
    Stopping --> Stopped: 进程退出
    Stopped --> [*]

    Running --> Crashed: 进程异常退出
    Crashed --> Starting: 自动重启
```

## 命令分发

Host 维护每个插件的命令队列：

```python
# host.py 中的核心循环
async def _dispatch_command(self, plugin_id, command):
    queue = self._cmd_queues[plugin_id]
    await queue.put(command)
    result = await self._wait_response(plugin_id, command.request_id)
    return result
```

## 作用域管理

Host 在命令执行前设置上下文变量：

```python
# _run_scope 和 _handler_scope 在 submit 前设置
# 确保 contextvars 在 Worker 线程中正确传播
_IN_HANDLER.set(entry_id)
_CURRENT_RUN_ID.set(run_id)
```

## 插件间通信

Host 处理 `plugin_to_plugin` 调用请求：

```
Plugin A → call_entry("B:func") → Host → dispatch to Plugin B → 结果返回 → Plugin A
```

Host 负责：
1. 验证目标插件存在且正在运行
2. 转发调用请求
3. 处理超时
4. 调用链传播
