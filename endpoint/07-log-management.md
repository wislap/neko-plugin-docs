# 日志管理端点

> 日志管理端点提供日志查询、文件列表和实时日志流功能

---

## 概述

日志管理端点用于查看和监控插件日志:
- 支持多种过滤条件(级别、时间范围、关键词)
- 提供日志文件列表
- 支持 WebSocket 实时日志流

所有端点都需要管理员认证。

---

## 1. 获取插件日志端点

### 7.1 获取插件日志端点

#### `GET /plugin/{plugin_id}/logs`

**功能**: 获取插件或服务器的日志内容

**路径参数**:
- `plugin_id`: 插件ID,使用 `_server` 获取服务器日志

**查询参数**:
- `lines` (可选): 返回行数 (1-10000,默认 100)
- `level` (可选): 日志级别过滤 (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
- `start_time` (可选): 开始时间 (ISO 8601 格式)
- `end_time` (可选): 结束时间 (ISO 8601 格式)
- `search` (可选): 关键词搜索

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "logs": [
    {
      "timestamp": "2026-01-26T14:30:00.123456+08:00",
      "level": "INFO",
      "message": "Plugin started",
      "source": "main.py:42"
    }
  ],
  "total_lines": 1000,
  "returned_lines": 100
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `logs`: 日志条目数组
  - `timestamp`: 时间戳
  - `level`: 日志级别
  - `message`: 日志消息
  - `source`: 源文件位置
- `total_lines`: 总行数
- `returned_lines`: 返回的行数

**实现细节**:
- 调用 `get_plugin_logs()` 获取日志
- 支持多种过滤条件
- 错误时返回空结果而非抛出异常

**使用场景**:
- 日志查看器
- 问题诊断
- 日志搜索

**代码位置**: `user_plugin_server.py:1425-1474`

---

### 7.2 获取日志文件列表端点

#### `GET /plugin/{plugin_id}/logs/files`

**功能**: 获取插件或服务器的日志文件列表

**路径参数**:
- `plugin_id`: 插件ID,使用 `_server` 获取服务器日志文件

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "log_files": [
    {
      "name": "plugin1.log",
      "path": "/path/to/plugin1.log",
      "size": 1024000,
      "modified": "2026-01-26T14:30:00.123456+08:00"
    }
  ],
  "count": 1,
  "time": "2026-01-26T14:30:05.123456+08:00"
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `log_files`: 日志文件数组
  - `name`: 文件名
  - `path`: 文件路径
  - `size`: 文件大小(字节)
  - `modified`: 最后修改时间
- `count`: 文件数量
- `time`: 响应时间戳

**实现细节**:
- 调用 `get_plugin_log_files()` 获取文件列表
- 扫描日志目录

**使用场景**:
- 日志文件管理
- 日志归档
- 文件下载选择

**代码位置**: `user_plugin_server.py:1477-1500`

---

### 7.3 WebSocket 日志流端点

#### `WebSocket /ws/logs/{plugin_id}`

**功能**: 通过 WebSocket 实时推送日志流

**路径参数**:
- `plugin_id`: 插件ID,使用 `_server` 获取服务器日志流

**查询参数**:
- `code`: 管理员验证码 (WebSocket 认证通过查询参数)

**认证要求**: **需要管理员验证码** (查询参数)

**消息格式**:
```json
{
  "timestamp": "2026-01-26T14:30:00.123456+08:00",
  "level": "INFO",
  "message": "New log entry",
  "source": "main.py:42"
}
```

**实现细节**:
- 调用 `log_stream_endpoint()` 处理 WebSocket 连接
- 实时推送新的日志条目
- 认证失败时关闭连接 (code 1008)

**使用场景**:
- 实时日志监控
- 调试和问题追踪
- 日志控制台

**代码位置**: `user_plugin_server.py:1503-1521`

---

## 8. 前端UI端点

### 8.1 前端首页端点

#### `GET /ui`
#### `GET /ui/`

**功能**: 返回前端管理界面的首页

**认证要求**: 无

**响应**: HTML 页面 (index.html)

**响应头**:
- `Cache-Control`: `no-store, no-cache, must-revalidate, max-age=0`
- `Pragma`: `no-cache`
- `Expires`: `0`

**实现细节**:
- 返回 `frontend/exported/index.html`
- 禁用缓存,确保总是获取最新版本
- 文件不存在时返回 404

**使用场景**:
- 访问管理界面
- SPA 应用入口

**代码位置**: `user_plugin_server.py:594-611`

---

### 8.2 前端静态资源端点

#### `StaticFiles /ui/assets`

**功能**: 提供前端静态资源 (JS, CSS, 图片等)

**认证要求**: 无

**缓存策略**:
- `Cache-Control`: `public, max-age=31536000, immutable`
- 长期缓存,提高加载性能

**实现细节**:
- 使用 FastAPI 的 `StaticFiles` 挂载
- 资源路径: `frontend/exported/assets/`
- 自动处理 MIME 类型

**使用场景**:
- 加载前端 JS/CSS 文件
- 加载图片和字体资源

**代码位置**: `user_plugin_server.py:234-238, 246-248`

---

### 8.3 前端 SPA 路由端点

#### `GET /ui/{full_path:path}`

**功能**: 处理前端 SPA 的所有路由 (History API fallback)

**路径参数**:
- `full_path`: 任意路径

**认证要求**: 无

**实现细节**:
- 如果路径对应的文件存在,返回该文件
- 如果文件不存在,返回 `index.html` (SPA fallback)
- HTML 文件禁用缓存
- 防止路径遍历攻击

**使用场景**:
- 支持前端路由刷新
- SPA 应用路由处理
- 例如: `/ui/plugins/plugin1` 刷新时仍能正常工作

**代码位置**: `user_plugin_server.py:614-653`

---


---

## 总结

日志管理端点共 **3个**,全部需要管理员认证:
- `/plugin/{id}/logs`: 查询日志内容,支持多种过滤条件
- `/plugin/{id}/logs/files`: 获取日志文件列表
- `WS /ws/logs/{id}`: WebSocket 实时日志流

用于日志查看、问题诊断和实时监控。特殊ID `_server` 用于访问服务器自身的日志。
