# 进度上报

插件在执行过程中可以实时上报进度，通过 WebSocket 推送到前端显示。

## 上报方式

通过 `ctx.run_update()` 在 Run 执行过程中上报：

```python
@plugin_entry()
def long_task(self, **_):
    total = 100
    for i in range(total):
        self._process_item(i)
        self.ctx.run_update(
            progress=(i + 1) / total,          # 0.0 - 1.0
            stage="processing",                 # 当前阶段
            message=f"处理第 {i+1} 项...",      # 状态消息
            step=i + 1,                         # 当前步骤
            step_total=total,                   # 总步骤
        )
    return ok(data={"processed": total})
```

## 进度字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `progress` | `float` | 进度值 0.0 - 1.0 |
| `stage` | `str` | 当前阶段名称 |
| `message` | `str` | 状态描述文本 |
| `step` | `int` | 当前步骤编号 |
| `step_total` | `int` | 总步骤数 |
| `eta_seconds` | `float` | 预估剩余时间（秒） |
| `metrics` | `dict` | 自定义指标 |

## 前端显示

进度数据通过以下链路到达前端：

```
ctx.run_update() → RunRecord 更新 → WebSocket 推送 → AgentHUD
```

AgentHUD 根据数据显示：

- **确定进度条**：当 `progress` 有值 (0-1) 时
- **不确定动画**：当 `progress` 为 None 时
- **阶段/消息文本**：`stage` + `message`
- **步骤计数器**：`step / step_total`

## 指纹去重

轮询机制使用 fingerprint 检测变化，避免冗余回调：

```python
fingerprint = (progress, stage, message, step, step_total)
# 只有 fingerprint 变化时才触发 on_progress 回调
```

## 最佳实践

:::{tip}
- 不要每次循环都上报，建议每 1-5% 进度或每秒上报一次
- `stage` 用短词如 `"downloading"`, `"processing"`, `"uploading"`
- `message` 包含人类可读的详细信息
- 长时间任务提供 `eta_seconds` 改善用户体验
:::
