# 基础路由端点

> 基础路由端点提供健康检查、可用性检查和服务器信息查询功能

---

## 1. 健康检查端点

### `GET /health`

**功能**: 健康检查端点,用于监控服务器是否正常运行

**请求参数**: 无

**响应格式**:
```json
{
  "status": "ok",
  "time": "2026-01-26T14:30:00.123456+08:00"
}
```

**字段说明**:
- `status`: 固定返回 `"ok"`,表示服务器正常运行
- `time`: ISO 8601 格式的当前时间戳

**认证要求**: 无

**使用场景**:
- 服务器启动后的健康检查
- 负载均衡器的健康探测
- 监控系统的存活性检测

**代码位置**: `user_plugin_server.py:261-264`

---

## 2. 可用性检查端点

### `GET /available`

**功能**: 返回服务器可用性状态和基本统计信息

**请求参数**: 无

**响应格式**:
```json
{
  "status": "ok",
  "available": true,
  "plugins_count": 5,
  "time": "2026-01-26T14:30:00.123456+08:00"
}
```

**字段说明**:
- `status`: 服务器状态,固定返回 `"ok"`
- `available`: 可用性标志,固定返回 `true`
- `plugins_count`: 当前已注册的插件数量
- `time`: ISO 8601 格式的当前时间戳

**认证要求**: 无

**实现细节**:
- 使用专用线程池 `_api_executor` 执行锁操作,避免阻塞事件循环
- 通过 `state.plugins_lock` 保护插件列表的并发访问
- 统计的是 `state.plugins` 中注册的插件总数(包括未运行的)

**使用场景**:
- 客户端检查服务器是否可用
- 快速获取插件数量统计

**代码位置**: `user_plugin_server.py:267-282`

---

## 3. 服务器信息端点

### `GET /server/info`

**功能**: 返回详细的服务器信息,包括SDK版本、插件统计、运行状态等

**请求参数**: 无

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "sdk_version": "1.0.0",
  "plugins_count": 5,
  "registered_plugins": ["plugin1", "plugin2", "plugin3"],
  "running_plugins_count": 3,
  "running_plugins": ["plugin1", "plugin2"],
  "running_plugins_status": {
    "plugin1": {
      "alive": true,
      "pid": 12345
    },
    "plugin2": {
      "alive": true,
      "pid": 12346
    }
  },
  "time": "2026-01-26T14:30:00.123456+08:00"
}
```

**字段说明**:
- `sdk_version`: Plugin SDK 版本号
- `plugins_count`: 已注册的插件总数
- `registered_plugins`: 已注册的插件ID列表
- `running_plugins_count`: 正在运行的插件数量
- `running_plugins`: 正在运行的插件ID列表
- `running_plugins_status`: 运行插件的详细状态
  - `alive`: 进程是否存活
  - `pid`: 进程ID
- `time`: ISO 8601 格式的当前时间戳

**实现细节**:
- 使用 `_api_executor` 线程池执行锁操作
- 通过 `state.plugins_lock` 访问已注册插件列表
- 通过 `state.plugin_hosts_lock` 访问运行中的插件主机
- 不调用 `is_alive()` 方法避免阻塞,直接检查 `plugin_hosts` 中的存在性

**使用场景**:
- 管理界面获取服务器概览
- 监控系统收集服务器状态
- 调试时查看插件运行情况

**代码位置**: `user_plugin_server.py:285-327`

---

## 总结

基础路由端点共 **3个**:
- 2个无需认证 (`/health`, `/available`)
- 1个需要管理员认证 (`/server/info`)

这些端点主要用于服务器监控、健康检查和基本信息查询。
