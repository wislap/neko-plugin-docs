# 插件管理端点

> 插件管理端点提供插件的列表查询、状态监控、启动、停止和重载功能

---

## 1. 插件列表端点

### `GET /plugins`

**功能**: 获取所有已注册插件的详细信息列表

**请求参数**: 无

**认证要求**: 无

**响应格式**:
```json
{
  "plugins": [
    {
      "id": "plugin1",
      "name": "示例插件",
      "version": "1.0.0",
      "description": "这是一个示例插件",
      "status": "running",
      "enabled": true
    }
  ],
  "message": ""
}
```

**字段说明**:
- `plugins`: 插件信息数组
  - `id`: 插件唯一标识符
  - `name`: 插件名称
  - `version`: 插件版本
  - `description`: 插件描述
  - `status`: 运行状态 (`running`, `stopped`, `error` 等)
  - `enabled`: 是否启用
- `message`: 提示信息,无插件时返回 `"no plugins registered"`

**实现细节**:
- 调用 `build_plugin_list()` 函数构建插件列表
- 使用 `_api_executor` 线程池执行,避免锁竞争阻塞事件循环
- 空列表时返回友好提示信息

**错误处理**:
- 捕获 `PluginError`, `ValueError`, `AttributeError`, `KeyError`
- 统一通过 `handle_plugin_error` 处理并返回 500 错误

**使用场景**:
- 前端展示插件列表
- 获取所有插件的基本信息
- 插件管理界面的数据源

**代码位置**: `user_plugin_server.py:364-394`

---

## 2. 插件状态查询端点

### `GET /plugin/status`

**功能**: 查询插件的运行状态

**请求参数**:
- `plugin_id` (可选): 插件ID,不提供则返回所有插件状态

**认证要求**: 无

**响应格式** (单个插件):
```json
{
  "plugin_id": "plugin1",
  "status": "running",
  "pid": 12345,
  "uptime": 3600,
  "time": "2026-01-26T14:30:00.123456+08:00"
}
```

**响应格式** (所有插件):
```json
{
  "plugins": {
    "plugin1": {
      "status": "running",
      "pid": 12345,
      "uptime": 3600
    },
    "plugin2": {
      "status": "stopped"
    }
  },
  "time": "2026-01-26T14:30:00.123456+08:00"
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `status`: 运行状态
  - `running`: 正在运行
  - `stopped`: 已停止
  - `error`: 错误状态
  - `starting`: 启动中
  - `stopping`: 停止中
- `pid`: 进程ID (仅运行时)
- `uptime`: 运行时长(秒)
- `time`: 时间戳

**实现细节**:
- 调用 `status_manager.get_plugin_status()` 获取状态
- 使用 `_api_executor` 线程池执行,避免锁竞争
- 兼容性处理: 为旧版本调用方添加 `time` 字段

**使用场景**:
- 实时监控插件运行状态
- 前端状态指示器
- 健康检查和告警

**代码位置**: `user_plugin_server.py:330-359`

---

## 3. 启动插件端点

### `POST /plugin/{plugin_id}/start`

**功能**: 启动指定的插件

**路径参数**:
- `plugin_id`: 要启动的插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "status": "starting",
  "message": "Plugin started successfully",
  "pid": 12345
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `status`: 启动后的状态
- `message`: 操作结果消息
- `pid`: 启动的进程ID

**错误处理**:
- `PluginError`: 插件相关错误(如插件不存在、已在运行等)
- `ValueError`: 参数错误
- `AttributeError`: 属性访问错误
- `OSError`: 系统级错误(如进程创建失败)

**实现细节**:
- 调用 `start_plugin()` 异步函数
- 会检查插件是否已注册
- 会检查插件是否已在运行
- 启动新的插件进程

**使用场景**:
- 管理界面手动启动插件
- 自动化脚本批量启动插件
- 插件崩溃后重启

**代码位置**: `user_plugin_server.py:658-674`

---

## 4. 停止插件端点

### `POST /plugin/{plugin_id}/stop`

**功能**: 停止正在运行的插件

**路径参数**:
- `plugin_id`: 要停止的插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "status": "stopped",
  "message": "Plugin stopped successfully"
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `status`: 停止后的状态
- `message`: 操作结果消息

**错误处理**:
- `PluginError`: 插件相关错误(如插件未运行)
- `OSError`: 系统级错误
- `TimeoutError`: 停止超时

**实现细节**:
- 调用 `stop_plugin()` 异步函数
- 会尝试优雅关闭(SIGTERM)
- 超时后强制终止(SIGKILL)

**使用场景**:
- 管理界面手动停止插件
- 维护前停止插件
- 资源回收

**代码位置**: `user_plugin_server.py:677-693`

---

## 5. 重载插件端点

### `POST /plugin/{plugin_id}/reload`

**功能**: 重载插件(先停止再启动)

**路径参数**:
- `plugin_id`: 要重载的插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "status": "running",
  "message": "Plugin reloaded successfully",
  "pid": 12347
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `status`: 重载后的状态
- `message`: 操作结果消息
- `pid`: 新进程ID

**错误处理**:
- `PluginError`: 插件相关错误
- `OSError`: 系统级错误
- `TimeoutError`: 停止超时

**实现细节**:
- 调用 `reload_plugin()` 异步函数
- 内部执行 stop + start 操作
- 会重新加载插件配置

**使用场景**:
- 插件代码更新后重载
- 配置修改后应用更改
- 插件异常后恢复

**代码位置**: `user_plugin_server.py:696-712`

---

## 总结

插件管理端点共 **5个**:
- 2个无需认证 (`/plugins`, `/plugin/status`)
- 3个需要管理员认证 (`/plugin/{id}/start`, `/plugin/{id}/stop`, `/plugin/{id}/reload`)

这些端点提供了完整的插件生命周期管理功能。
