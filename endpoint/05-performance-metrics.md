# 性能监控端点

> 性能监控端点提供插件的实时性能指标和历史数据查询

---

## 概述

性能监控端点用于监控插件的资源使用情况,包括 CPU、内存、线程数等指标。所有端点都需要管理员认证。

---

## 1. 获取所有插件性能指标端点

### 5.1 获取所有插件性能指标端点

#### `GET /plugin/metrics`

**功能**: 获取所有运行中插件的性能指标

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "metrics": [
    {
      "plugin_id": "plugin1",
      "pid": 12345,
      "cpu_percent": 5.2,
      "memory_mb": 128.5,
      "memory_percent": 1.2,
      "num_threads": 8,
      "timestamp": "2026-01-26T14:30:00.123456+08:00"
    }
  ],
  "count": 1,
  "global": {
    "total_cpu_percent": 5.2,
    "total_memory_mb": 128.5,
    "total_memory_percent": 1.2,
    "total_threads": 8,
    "active_plugins": 1
  },
  "time": "2026-01-26T14:30:05.123456+08:00"
}
```

**字段说明**:
- `metrics`: 性能指标数组
  - `plugin_id`: 插件ID
  - `pid`: 进程ID
  - `cpu_percent`: CPU 使用率 (%)
  - `memory_mb`: 内存使用量 (MB)
  - `memory_percent`: 内存使用率 (%)
  - `num_threads`: 线程数
  - `timestamp`: 采集时间
- `count`: 指标数量
- `global`: 全局统计
  - `total_cpu_percent`: 总 CPU 使用率
  - `total_memory_mb`: 总内存使用量
  - `total_memory_percent`: 总内存使用率
  - `total_threads`: 总线程数
  - `active_plugins`: 活跃插件数
- `time`: 响应时间戳

**实现细节**:
- 调用 `metrics_collector.get_current_metrics()` 获取指标
- 计算全局性能统计
- 错误时返回空结果而非抛出异常,避免前端显示错误

**使用场景**:
- 监控所有插件的资源使用
- 性能分析和优化
- 资源告警

**代码位置**: `user_plugin_server.py:717-788`

---

### 5.2 获取单个插件性能指标端点

#### `GET /plugin/metrics/{plugin_id}`

**功能**: 获取指定插件的性能指标

**路径参数**:
- `plugin_id`: 插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式** (有指标):
```json
{
  "plugin_id": "plugin1",
  "metrics": {
    "pid": 12345,
    "cpu_percent": 5.2,
    "memory_mb": 128.5,
    "memory_percent": 1.2,
    "num_threads": 8,
    "timestamp": "2026-01-26T14:30:00.123456+08:00"
  },
  "time": "2026-01-26T14:30:05.123456+08:00"
}
```

**响应格式** (无指标):
```json
{
  "plugin_id": "plugin1",
  "metrics": null,
  "message": "Plugin is running but no metrics available yet (may be collecting, check collector status)",
  "plugin_running": true,
  "process_alive": true,
  "time": "2026-01-26T14:30:05.123456+08:00"
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `metrics`: 性能指标对象 (无数据时为 `null`)
- `message`: 状态消息
- `plugin_running`: 插件是否在运行
- `process_alive`: 进程是否存活
- `time`: 响应时间戳

**错误处理**:
- 404: 插件不存在
- 500: 获取失败

**实现细节**:
- 使用 `_api_executor` 线程池检查插件状态
- 区分插件未注册、未运行、进程崩溃等情况
- 提供详细的诊断信息

**使用场景**:
- 监控特定插件的性能
- 诊断插件问题
- 性能调优

**代码位置**: `user_plugin_server.py:791-887`

---

### 5.3 获取插件性能历史端点

#### `GET /plugin/metrics/{plugin_id}/history`

**功能**: 获取插件的历史性能指标数据

**路径参数**:
- `plugin_id`: 插件ID

**查询参数**:
- `limit` (可选): 返回数量限制 (1-1000,默认 100)
- `start_time` (可选): 开始时间 (ISO 8601 格式)
- `end_time` (可选): 结束时间 (ISO 8601 格式)

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin_id": "plugin1",
  "history": [
    {
      "cpu_percent": 5.2,
      "memory_mb": 128.5,
      "memory_percent": 1.2,
      "num_threads": 8,
      "timestamp": "2026-01-26T14:30:00.123456+08:00"
    }
  ],
  "count": 1,
  "time": "2026-01-26T14:30:05.123456+08:00"
}
```

**字段说明**:
- `plugin_id`: 插件ID
- `history`: 历史指标数组 (按时间倒序)
- `count`: 历史记录数量
- `time`: 响应时间戳

**实现细节**:
- 调用 `metrics_collector.get_metrics_history()` 获取历史数据
- 支持时间范围过滤
- 支持限制返回数量

**使用场景**:
- 性能趋势分析
- 历史数据回溯
- 性能报告生成

**代码位置**: `user_plugin_server.py:890-923`

---


---

## 总结

性能监控端点共 **3个**,全部需要管理员认证:
- `/plugin/metrics`: 获取所有插件的实时性能指标
- `/plugin/metrics/{id}`: 获取单个插件的性能指标
- `/plugin/metrics/{id}/history`: 获取插件的历史性能数据

这些端点用于性能分析、资源监控和问题诊断。
