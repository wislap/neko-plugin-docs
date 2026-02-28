# HTTP & WebSocket API

Run 系统提供 REST API 和 WebSocket 实时推送。

## REST API

### 创建 Run

```
POST /runs
```

```json
{
  "plugin_id": "my_plugin",
  "entry_id": "process",
  "args": {"data": "hello"},
  "task_id": "optional-task-id",
  "idempotency_key": "optional-dedup-key"
}
```

响应：

```json
{
  "run_id": "run_abc123",
  "status": "queued",
  "token": "eyJ...",
  "token_expires_at": 1704067200
}
```

### 查询 Run

```
GET /runs/{run_id}
```

返回完整的 `RunRecord`。

### 取消 Run

```
POST /runs/{run_id}/cancel
```

```json
{
  "reason": "用户手动取消"
}
```

### 获取 Export

```
GET /runs/{run_id}/export?limit=50&after=cursor&category=user
```

返回 `ExportListResponse`。

## WebSocket

WebSocket 端点提供 Run 状态的实时推送。

### 连接

```
WS /runs/{run_id}/ws?token=<run_token>
```

### Token 认证

连接时需要提供创建 Run 时返回的 token：

```python
token, expires_at = issue_run_token(run_id=run_id, perm="read")
```

Token 结构：`base64url(payload).base64url(hmac_sha256(payload))`

Payload 包含：

```json
{
  "run_id": "run_abc123",
  "exp": 1704067200,
  "nonce": "random_string",
  "perm": "read"
}
```

### 推送消息格式

WebSocket 推送以下类型的消息：

```json
{
  "type": "run_update",
  "run": {
    "run_id": "run_abc123",
    "status": "running",
    "progress": 0.5,
    "stage": "processing",
    "message": "处理中..."
  }
}
```

```json
{
  "type": "export_new",
  "item": {
    "export_item_id": "exp_123",
    "type": "text",
    "text": "新的日志内容"
  }
}
```

```json
{
  "type": "run_complete",
  "run": {
    "run_id": "run_abc123",
    "status": "succeeded"
  }
}
```
