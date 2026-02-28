# Run 进度上报插件

演示使用 Run 系统进行进度上报和 Export 导出。

## __init__.py

```python
import time
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, ok,
)


@neko_plugin
class RunProgressPlugin(NekoPluginBase):

    @plugin_entry()
    def process_batch(self, items: list = None, **_):
        """批量处理，上报进度"""
        items = items or list(range(20))
        total = len(items)
        results = []

        for i, item in enumerate(items):
            # 模拟处理
            time.sleep(0.5)

            # 上报进度
            self.ctx.run_update(
                progress=(i + 1) / total,
                stage="processing",
                message=f"处理第 {i + 1}/{total} 项",
                step=i + 1,
                step_total=total,
            )

            # 推送中间结果到 Export
            self.ctx.export_push(
                type="text",
                text=f"Item {item} processed at step {i + 1}",
                label=f"step_{i + 1}",
            )

            results.append({"item": item, "status": "done"})

        # 推送最终结果到 Export
        self.ctx.export_push(
            type="json",
            json_data={"results": results, "total": total},
            label="final_result",
        )

        return ok(data={"processed": total, "results": results})

    @plugin_entry()
    def generate_report(self, title: str = "Report", **_):
        """生成报告，演示多种 Export 类型"""
        self.ctx.run_update(progress=0.0, stage="preparing", message="准备中...")

        # 步骤 1: 文本日志
        self.ctx.export_push(type="text", text="开始生成报告...", label="log")
        self.ctx.run_update(progress=0.3, stage="collecting", message="收集数据...")
        time.sleep(1)

        # 步骤 2: JSON 数据
        data = {"title": title, "sections": 3, "generated_at": time.time()}
        self.ctx.export_push(type="json", json_data=data, label="report_data")
        self.ctx.run_update(progress=0.7, stage="formatting", message="格式化中...")
        time.sleep(1)

        # 步骤 3: URL 结果
        self.ctx.export_push(
            type="url",
            url="https://example.com/reports/latest",
            label="report_url",
        )
        self.ctx.run_update(progress=1.0, stage="done", message="报告生成完成")

        return ok(data={"title": title, "url": "https://example.com/reports/latest"})
```
