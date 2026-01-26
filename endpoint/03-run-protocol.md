# Run Protocol 端点

> Run Protocol 是插件调用的主要 API,提供了创建运行、WebSocket 通信、文件上传下载等功能

---

## 概述

Run Protocol 是 N.E.K.O Plugin Server 的核心 API,提供了完整的插件运行生命周期管理。包括:
- 运行创建和状态查询
- WebSocket 实时通信
- 文件上传下载
- 运行取消和结果导出

---

## 1. 创建运行端点

#### `POST /runs`

**功能**: 创建一个新的插件运行实例

**请求体**:
```json
{
  "plugin_id": "plugin1",
  "input": {
    "message": "Hello",
    "params": {}
  },
  "config": {}
}
```

**认证要求**: 无 (但会记录客户端IP)

**响应格式**:
```json
{
  "run_id": "run_abc123",
  "status": "pending",
  "run_token": "eyJhbGc...",
  "expires_at": "2026-01-26T15:30:00.123456+08:00"
}
```

**字段说明**:
- `run_id`: 运行实例的唯一标识符
- `status`: 初始状态,通常为 `"pending"`
- `run_token`: WebSocket 连接令牌
- `expires_at`: 令牌过期时间

**实现细节**:
- 调用 `create_run()` 创建运行记录
- 调用 `issue_run_token()` 生成 WebSocket 令牌
- 记录客户端主机地址用于审计

**错误处理**:
- 返回 500 错误并包含详细错误信息

**使用场景**:
- 客户端发起插件调用
- 创建异步任务
- 获取 WebSocket 连接凭证

**代码位置**: `user_plugin_server.py:399-408`

---

## 2. WebSocket 运行端点

#### `WebSocket /ws/run`

**功能**: 通过 WebSocket 实时通信执行插件运行

**查询参数**:
- `run_token`: 从 `/runs` 端点获取的令牌

**认证要求**: 需要有效的 `run_token`

**消息格式**:
- 客户端 → 服务器: 发送输入数据、控制命令
- 服务器 → 客户端: 推送运行状态、输出结果、进度更新

**实现细节**:
- 调用 `ws_run_endpoint()` 处理 WebSocket 连接
- 支持双向实时通信
- 自动处理连接生命周期

**使用场景**:
- 实时接收插件输出
- 发送中断/取消命令
- 流式数据传输

**代码位置**: `user_plugin_server.py:411-413`

---

## 3. 管理员 WebSocket 端点

#### `WebSocket /ws/admin`

**功能**: 管理员专用的 WebSocket 端点,用于监控和管理

**认证要求**: 需要管理员权限

**实现细节**:
- 调用 `ws_admin_endpoint()` 处理连接
- 提供全局监控能力
- 可接收系统级事件

**使用场景**:
- 管理界面实时监控
- 系统事件推送
- 全局状态更新

**代码位置**: `user_plugin_server.py:416-418`

---

## 4. 查询运行状态端点

#### `GET /runs/{run_id}`

**功能**: 查询指定运行实例的详细状态

**路径参数**:
- `run_id`: 运行实例ID

**认证要求**: 无

**响应格式**:
```json
{
  "run_id": "run_abc123",
  "plugin_id": "plugin1",
  "status": "running",
  "created_at": "2026-01-26T14:30:00.123456+08:00",
  "started_at": "2026-01-26T14:30:01.123456+08:00",
  "completed_at": null,
  "result": null,
  "error": null
}
```

**字段说明**:
- `run_id`: 运行ID
- `plugin_id`: 插件ID
- `status`: 运行状态
  - `pending`: 等待中
  - `running`: 运行中
  - `completed`: 已完成
  - `failed`: 失败
  - `cancelled`: 已取消
  - `cancel_requested`: 取消请求中
- `created_at`: 创建时间
- `started_at`: 开始时间
- `completed_at`: 完成时间
- `result`: 运行结果
- `error`: 错误信息

**错误处理**:
- 404: 运行不存在
- 500: 服务器错误

**使用场景**:
- 轮询运行状态
- 获取运行结果
- 调试和审计

**代码位置**: `user_plugin_server.py:421-432`

---

## 5. 创建上传会话端点

#### `POST /runs/{run_id}/uploads`

**功能**: 为运行创建文件上传会话

**路径参数**:
- `run_id`: 运行实例ID

**请求体** (可选):
```json
{
  "filename": "data.json",
  "mime": "application/json",
  "max_bytes": 10485760
}
```

**认证要求**: 无 (但运行必须存在且处于运行状态)

**响应格式**:
```json
{
  "upload_id": "upload_xyz789",
  "blob_id": "blob_def456",
  "upload_url": "http://127.0.0.1:48912/uploads/upload_xyz789",
  "blob_url": "http://127.0.0.1:48912/runs/run_abc123/blobs/blob_def456"
}
```

**字段说明**:
- `upload_id`: 上传会话ID
- `blob_id`: 生成的 blob ID
- `upload_url`: 上传数据的 URL
- `blob_url`: 下载数据的 URL

**实现细节**:
- 调用 `blob_store.create_upload()` 创建上传会话
- 生成临时上传路径
- 设置文件大小限制

**错误处理**:
- 404: 运行不存在
- 500: 创建失败

**使用场景**:
- 向插件上传文件
- 传输大型数据
- 多文件上传管理

**代码位置**: `user_plugin_server.py:435-464`

---

## 6. 上传文件数据端点

#### `PUT /uploads/{upload_id}`

**功能**: 上传文件数据到指定的上传会话

**路径参数**:
- `upload_id`: 上传会话ID

**请求体**: 原始二进制数据 (流式传输)

**认证要求**: 无 (但上传会话必须存在且关联的运行必须在运行中)

**响应格式**:
```json
{
  "ok": true,
  "upload_id": "upload_xyz789",
  "blob_id": "blob_def456",
  "size": 1024
}
```

**字段说明**:
- `ok`: 上传是否成功
- `upload_id`: 上传会话ID
- `blob_id`: blob ID
- `size`: 上传的字节数

**实现细节**:
- 流式接收数据,避免内存溢出
- 检查文件大小限制 (`max_bytes`)
- 上传完成后调用 `blob_store.finalize_upload()`
- 失败时自动清理临时文件

**错误处理**:
- 404: 上传会话不存在或运行不存在
- 409: 运行不在运行状态
- 413: 文件过大
- 500: 上传失败

**使用场景**:
- 实际上传文件数据
- 大文件分块上传
- 断点续传

**代码位置**: `user_plugin_server.py:467-507`

---

## 7. 下载 Blob 数据端点

#### `GET /runs/{run_id}/blobs/{blob_id}`

**功能**: 下载运行关联的 blob 数据

**路径参数**:
- `run_id`: 运行实例ID
- `blob_id`: blob ID

**认证要求**: 无

**响应**: 文件下载 (FileResponse)

**响应头**:
- `Content-Disposition`: `attachment; filename="{blob_id}.bin"`

**实现细节**:
- 调用 `blob_store.get_blob_path()` 获取文件路径
- 使用 FastAPI 的 `FileResponse` 返回文件

**错误处理**:
- 404: blob 不存在
- 500: 下载失败

**使用场景**:
- 下载插件生成的文件
- 获取运行结果数据
- 文件传输

**代码位置**: `user_plugin_server.py:510-521`

---

## 8. 取消运行端点

#### `POST /runs/{run_id}/cancel`

**功能**: 请求取消正在运行的实例

**路径参数**:
- `run_id`: 运行实例ID

**请求体** (可选):
```json
{
  "reason": "User cancelled"
}
```

**认证要求**: 无

**响应格式**:
```json
{
  "run_id": "run_abc123",
  "status": "cancel_requested",
  "cancelled_at": "2026-01-26T14:35:00.123456+08:00"
}
```

**字段说明**:
- `run_id`: 运行ID
- `status`: 更新后的状态
- `cancelled_at`: 取消请求时间

**实现细节**:
- 调用 `cancel_run()` 设置取消标志
- 插件需要主动检查取消状态
- 不会立即终止运行

**错误处理**:
- 404: 运行不存在
- 500: 取消失败

**使用场景**:
- 用户主动取消任务
- 超时自动取消
- 资源回收

**代码位置**: `user_plugin_server.py:524-535`

---

## 9. 导出数据列表端点

#### `GET /runs/{run_id}/export`

**功能**: 获取运行导出的数据项列表

**路径参数**:
- `run_id`: 运行实例ID

**查询参数**:
- `after` (可选): 游标,用于分页
- `limit` (可选): 返回数量限制 (1-2000,默认 200)

**认证要求**: 无

**响应格式**:
```json
{
  "items": [
    {
      "id": "export_001",
      "type": "text",
      "data": "...",
      "created_at": "2026-01-26T14:30:05.123456+08:00"
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

**字段说明**:
- `items`: 导出项数组
  - `id`: 导出项ID
  - `type`: 数据类型
  - `data`: 数据内容
  - `created_at`: 创建时间
- `has_more`: 是否有更多数据
- `next_cursor`: 下一页游标

**实现细节**:
- 调用 `list_export_for_run()` 获取导出列表
- 支持分页查询
- 按时间顺序返回

**错误处理**:
- 404: 运行不存在
- 500: 查询失败

**使用场景**:
- 获取插件导出的数据
- 分页浏览大量结果
- 数据同步

**代码位置**: `user_plugin_server.py:538-553`

---
---

## 总结

Run Protocol 端点共 **9个**,全部无需认证(但会记录客户端信息):
- 运行管理: `/runs`, `/runs/{id}`, `/runs/{id}/cancel`
- WebSocket 通信: `/ws/run`, `/ws/admin`
- 文件传输: `/runs/{id}/uploads`, `/uploads/{id}`, `/runs/{id}/blobs/{blob_id}`
- 数据导出: `/runs/{id}/export`

这是插件调用的核心 API,推荐所有新代码使用 Run Protocol 而非旧的触发器机制。
