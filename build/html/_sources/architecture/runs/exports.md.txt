# Export 通道

Export 是 Run 执行过程中产出的结构化数据，支持五种类型。

## ExportItem

```python
class ExportItem(BaseModel):
    export_item_id: str
    run_id: str
    type: ExportType                          # "text" | "json" | "url" | "binary_url" | "binary"
    category: ExportCategory = "user"         # "system" | "user"
    created_at: float
    label: Optional[str] = None
    description: Optional[str] = None
    text: Optional[str] = None
    json_data: Optional[Dict[str, Any]] = None  # alias="json"
    url: Optional[str] = None
    binary_url: Optional[str] = None
    binary: Optional[str] = None              # Base64
    mime: Optional[str] = None
    metadata: Dict[str, Any] = {}
```

## 五种 Export 类型

| 类型 | 说明 | 主要字段 |
|------|------|----------|
| `text` | 纯文本 | `text` |
| `json` | 结构化 JSON | `json_data` |
| `url` | URL 链接 | `url` |
| `binary_url` | 二进制文件 URL | `binary_url`, `mime` |
| `binary` | 内联二进制 (Base64) | `binary`, `mime` |

## ExportCategory

| 类别 | 说明 |
|------|------|
| `"user"` | 插件主动推送的数据（默认） |
| `"system"` | 系统自动生成的数据（如 trigger response） |

## 推送 API

通过 `ctx.export_push()` / `ctx.export_push_async()` 推送：

```python
# 推送文本
self.ctx.export_push(type="text", text="处理日志内容...")

# 推送 JSON
self.ctx.export_push(
    type="json",
    json_data={"result": 42, "items": [1, 2, 3]},
    label="final_result",
)

# 推送 URL
self.ctx.export_push(type="url", url="https://example.com/report.pdf")

# 推送二进制 URL
self.ctx.export_push(
    type="binary_url",
    binary_url="https://storage.example.com/image.png",
    mime="image/png",
)

# 推送内联二进制（小文件）
import base64
with open("small.png", "rb") as f:
    data = base64.b64encode(f.read()).decode()
self.ctx.export_push(type="binary", binary=data, mime="image/png")
```

### label 字段

`label` 用于标识 export 项的用途，方便客户端筛选：

```python
self.ctx.export_push(type="json", json_data=result, label="plugin_response")
self.ctx.export_push(type="text", text=log, label="execution_log")
```

## 系统 Export

系统会自动为每个 Run 创建 `category="system"` 的 export：

- trigger 成功时：`type="json"`, `label="plugin_response"`, 包含插件返回值
- trigger 失败时：`type="json"`, `label="plugin_error"`, 包含错误信息

## 查询 API

```
GET /runs/{run_id}/export?limit=50&category=user
```

返回 `ExportListResponse`：

```python
class ExportListResponse(BaseModel):
    items: List[ExportItem]
    next_after: Optional[str] = None  # 分页游标
```
