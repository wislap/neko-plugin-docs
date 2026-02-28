# Run/Export 执行系统

Run 系统管理插件入口点的 **任务执行生命周期**，提供状态追踪、进度上报和多格式数据导出。

## 核心概念

| 概念 | 说明 |
|------|------|
| **Run** | 一次入口点执行的完整生命周期记录 |
| **RunRecord** | Run 的状态数据（状态、进度、时间戳、结果） |
| **Export** | Run 执行过程中产出的数据（文本、JSON、URL、二进制） |
| **ExportItem** | 单个导出数据项 |

## 架构

```{mermaid}
sequenceDiagram
    participant C as Client
    participant S as Server
    participant RM as RunManager
    participant P as Plugin
    participant ES as ExportStore

    C->>S: POST /runs (create)
    S->>RM: create_run()
    RM->>RM: RunRecord (queued)
    RM->>P: trigger_plugin()
    RM->>RM: RunRecord (running)

    loop 执行中
        P->>RM: run_update(progress, stage, message)
        P->>ES: export_push(text/json/url/binary)
    end

    alt 成功
        P->>RM: 返回结果
        RM->>RM: RunRecord (succeeded)
        RM->>ES: 系统 export (plugin_response)
    else 失败
        P->>RM: 抛出异常
        RM->>RM: RunRecord (failed, error)
    end

    C->>S: GET /runs/{id}
    C->>S: GET /runs/{id}/export
```

## 数据流概览

```
Plugin → ctx.run_update(progress, stage, message)
       → RunRecord 更新
       → WebSocket 实时推送到前端
       → AgentHUD 进度条 + 状态文本

Plugin → ctx.export_push(type, text/json/url/binary)
       → ExportStore 追加
       → 客户端通过 API 获取
```

```{toctree}
:maxdepth: 2

run-lifecycle
run-progress
exports
run-api
run-storage
```
