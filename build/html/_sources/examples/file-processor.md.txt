# 文件处理插件

演示 lifecycle、timer_interval 和 push_message 的组合使用。

## plugin.toml

```toml
[plugin]
id = "file_processor"
name = "File Processor"
version = "1.0.0"
entry = "plugins.file_processor:FileProcessorPlugin"
```

## __init__.py

```python
import os
import shutil
from pathlib import Path
from typing import Optional
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle,
    timer_interval, ok, fail,
)


@neko_plugin
class FileProcessorPlugin(NekoPluginBase):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.work_dir = Path("/tmp/file_processor")
        self.processed_count = 0

    @lifecycle(id="startup")
    def startup(self, **_):
        self.work_dir.mkdir(exist_ok=True)
        self.report_status({"status": "initialized", "work_dir": str(self.work_dir)})
        return {"status": "ready"}

    @lifecycle(id="shutdown")
    def shutdown(self, **_):
        if self.work_dir.exists():
            shutil.rmtree(self.work_dir)
        return {"status": "stopped"}

    @plugin_entry()
    def process_file(self, file_path: str, operation: str, options: Optional[dict] = None, **_):
        options = options or {}
        self.report_status({"status": "processing", "file": file_path})

        try:
            if operation == "compress":
                result = {"output_path": f"{file_path}.zip", "size": 1024}
            elif operation == "convert":
                fmt = options.get("format", "pdf")
                result = {"output_path": f"{file_path}.{fmt}", "size": 2048}
            else:
                return fail(message=f"Unknown operation: {operation}")

            self.processed_count += 1

            self.ctx.push_message(
                source="file_processor",
                message_type="text",
                description="文件处理完成",
                priority=6,
                content=f"文件 {file_path} 处理成功",
                metadata={"operation": operation, "result": result},
            )

            return ok(data={"success": True, "result": result})

        except Exception as e:
            self.ctx.push_message(
                source="file_processor",
                message_type="text",
                description="文件处理失败",
                priority=9,
                content=f"处理文件 {file_path} 时出错: {e}",
            )
            return fail(message=str(e))

    @timer_interval(id="cleanup", seconds=3600, auto_start=True)
    def cleanup(self, **_):
        self.logger.info("Running periodic cleanup...")
        return {"cleaned": True}
```
