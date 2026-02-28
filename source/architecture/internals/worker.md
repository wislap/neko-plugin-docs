# Worker 模式

Worker 模式允许入口点在独立线程池中执行，不阻塞插件的主命令循环。

## 工作原理

```{mermaid}
sequenceDiagram
    participant CL as 命令循环
    participant TP as 线程池
    participant E as Entry 函数

    CL->>CL: 收到 trigger 命令
    alt Worker 模式
        CL->>TP: 提交到线程池
        CL->>CL: 继续处理其他命令
        TP->>E: 执行入口函数
        E->>TP: 返回结果
        TP->>CL: 回写响应
    else 普通模式
        CL->>E: 同步执行
        E->>CL: 返回结果
    end
```

## 使用

```python
from plugin.sdk import worker, plugin_entry

@worker(timeout=60.0, priority=0)
@plugin_entry(id="heavy_task")
def heavy_task(self, **_):
    import time
    time.sleep(30)  # 不阻塞命令循环
    return {"done": True}
```

## contextvars 传播

Worker 线程自动继承调用时的 `contextvars` 上下文：

```python
# core/worker.py 中的实现
ctx_snapshot = contextvars.copy_context()
future = executor.submit(ctx_snapshot.run, func, *args)
```

这确保以下变量在 Worker 线程中可用：

| ContextVar | 说明 |
|-----------|------|
| `_IN_HANDLER` | 当前 handler 标识 |
| `_CURRENT_RUN_ID` | 当前 Run ID |
| `_IN_WORKER` | Worker 标记 |

## 配置

| 参数 | 默认 | 说明 |
|------|------|------|
| `timeout` | `30.0` | 执行超时（秒） |
| `priority` | `0` | 调度优先级 |

Worker 线程池大小取决于系统配置（通常 4-8 个线程）。
