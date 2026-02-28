# 上下文

`PluginContext` 是插件运行时的核心上下文对象，提供与主系统交互的全部接口。
通过 `self.ctx` 访问。

## 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `ctx.plugin_id` | `str` | 插件 ID |
| `ctx.config_path` | `Path` | `plugin.toml` 路径 |
| `ctx.logger` | `Logger` | loguru 日志记录器 |
| `ctx.bus` | `BusHub` | Bus 数据访问中心 |

## 日志

插件基类自动提供 `self.logger`（来自 `ctx.logger`）：

```python
class MyPlugin(NekoPluginBase):
    @plugin_entry()
    def example(self):
        self.logger.debug("调试信息")
        self.logger.info("一般信息")
        self.logger.warning("警告信息")
        self.logger.error("错误信息")
        self.logger.exception("异常信息（包含堆栈）")
```

### 文件日志

```python
def __init__(self, ctx):
    super().__init__(ctx)
    self.file_logger = self.enable_file_logging(log_level="INFO")
    self.logger = self.file_logger  # 同时输出到文件和控制台
```

## 状态上报

通过 `self.report_status()` 向主进程上报插件状态：

```python
@plugin_entry(id="long_task")
def long_task(self, **_):
    total = 100
    for i in range(total):
        self._do_step(i)
        self.report_status({
            "status": "processing",
            "current_step": i + 1,
            "total_steps": total,
            "progress": (i + 1) / total * 100,
            "message": f"处理中: {i + 1}/{total}",
        })

    self.report_status({"status": "completed", "message": "任务完成"})
    return {"completed": True}
```

## 消息推送

通过 `self.ctx.push_message()` 向主进程推送消息：

```python
self.ctx.push_message(
    source="my_feature",          # 消息来源标识
    message_type="text",          # "text" | "url" | "binary" | "binary_url"
    description="操作完成",       # 消息描述
    priority=5,                   # 优先级 (0-10)
    content="任务已成功完成",     # 文本内容或 URL
    metadata={"task_id": "123"},  # 额外元数据
)
```

### 消息类型

| 类型 | 说明 | 主要字段 |
|------|------|----------|
| `"text"` | 文本消息 | `content` |
| `"url"` | URL 链接 | `content`（URL 字符串） |
| `"binary"` | 小文件直传 | `binary_data`（bytes） |
| `"binary_url"` | 大文件引用 | `binary_url`（URL 字符串） |

### 优先级

| 范围 | 级别 | 适用场景 |
|------|------|----------|
| 0-2 | 低 | 信息性消息 |
| 3-5 | 中 | 一般通知 |
| 6-8 | 高 | 重要通知 |
| 9-10 | 紧急 | 需要立即处理 |

### 示例

```python
# 文本消息
self.ctx.push_message(
    source="chat_handler",
    message_type="text",
    description="消息回复",
    priority=5,
    content="处理完成",
)

# URL 消息
self.ctx.push_message(
    source="web_scraper",
    message_type="url",
    description="发现新文章",
    priority=7,
    content="https://example.com/article",
    metadata={"title": "Example Article"},
)

# 二进制数据（小文件）
with open("image.png", "rb") as f:
    self.ctx.push_message(
        source="image_processor",
        message_type="binary",
        description="处理后的图片",
        priority=6,
        binary_data=f.read(),
        metadata={"format": "png"},
    )

# 大文件 URL 引用
self.ctx.push_message(
    source="file_processor",
    message_type="binary_url",
    description="大文件处理完成",
    priority=8,
    binary_url="https://storage.example.com/large_file.zip",
    metadata={"size": 1024 * 1024 * 100},
)
```

## Bus 数据访问

通过 `self.ctx.bus` 访问 Bus 系统的各种数据流：

```python
# 消息
messages = self.ctx.bus.messages

# 事件
events = self.ctx.bus.events

# 生命周期
lifecycle = self.ctx.bus.lifecycle

# 对话
conversations = self.ctx.bus.conversations

# 记忆
memory = self.ctx.bus.memory
```

:::{seealso}
Bus 系统的详细文档见 [系统架构 - Bus 通信](../architecture/bus/index.md)。
:::

## Export 推送

在 Run 执行过程中，可以通过 `ctx.export_push()` 向 Export 通道推送数据：

```python
# 推送文本
self.ctx.export_push(type="text", text="处理日志...")

# 推送 JSON 结构化数据
self.ctx.export_push(type="json", json_data={"result": 42}, label="final_result")

# 推送 URL
self.ctx.export_push(type="url", url="https://example.com/report.pdf")
```

:::{seealso}
Export 通道的详细文档见 [系统架构 - Run/Export](../architecture/runs/exports.md)。
:::
