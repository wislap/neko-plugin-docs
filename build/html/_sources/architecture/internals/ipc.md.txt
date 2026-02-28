# 进程间通信

N.E.K.O 的进程间通信基于 ZeroMQ，在主进程和插件子进程之间传递命令和响应。

## 通信模型

```{mermaid}
graph LR
    subgraph Main["主进程"]
        CMD["命令队列"]
        RES["响应队列"]
        ZMQ["ZeroMQ Server"]
    end

    subgraph Plugin["插件进程"]
        CL["命令循环"]
        ZC["ZeroMQ Client"]
    end

    CMD -->|命令| ZMQ
    ZMQ <-->|IPC| ZC
    ZC --> CL
    CL -->|结果| ZC
    ZC -->|响应| ZMQ
    ZMQ --> RES
```

## 命令队列

主进程通过命令队列向插件发送指令：

| 命令类型 | 说明 |
|---------|------|
| `trigger` | 触发入口点执行 |
| `lifecycle` | 生命周期事件 (startup/shutdown/reload/freeze/unfreeze) |
| `status_query` | 查询插件状态 |
| `config_update` | 配置变更通知 |

## 响应队列

插件通过响应队列返回执行结果：

```python
{
    "request_id": "uuid",
    "success": True,
    "data": {...},
    "error": None,
}
```

## ZeroMQ IPC

使用 `ipc://` 协议进行本机通信，避免网络开销：

```python
# 端点格式
"ipc:///tmp/neko_plugin_{plugin_id}.sock"
```

### 消息序列化

使用 `ormsgpack`（MsgPack）序列化，比 JSON 快 3-5x，体积小 30-50%。

## 同步调用警告

在 handler 中执行同步 IPC 调用可能导致死锁（因为命令循环被阻塞）。SDK 会根据 `SYNC_CALL_IN_HANDLER_POLICY` 配置：

| 策略 | 说明 |
|------|------|
| `"warn"` | 记录警告日志 |
| `"error"` | 抛出异常 |
| `"allow"` | 静默允许 |

:::{warning}
建议在 handler 中使用异步版本的 API（如 `call_entry_async`、`config.get_async`）避免死锁。
:::
