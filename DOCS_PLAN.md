# N.E.K.O Plugin SDK 文档规划

> Sphinx + MyST-Parser + sphinx-book-theme 五层架构
> 手写文档用 Markdown (MyST)，API 参考用 rST (autodoc)

## 基础设施

- [x] `source/conf.py` — Sphinx 主配置（autodoc + MyST + napoleon + sphinx-design）
- [x] `Makefile` — 构建脚本
- [x] `requirements.txt` — Python 依赖
- [x] `source/_static/custom.css` — 自定义样式

---

## 第一层：Getting Started（快速上手）

- [x] `source/getting-started/index.md` — 概述 + 架构图
- [x] `source/getting-started/installation.md` — 环境准备 & 依赖安装
- [x] `source/getting-started/first-plugin.md` — 第一个插件（Hello World）
- [x] `source/getting-started/project-structure.md` — plugin.toml 详解

---

## 第二层：Guide（开发指南）

- [x] `source/guide/index.md` — 指南总览
- [x] `source/guide/decorators.md` — 装饰器全集
- [x] `source/guide/context.md` — PluginContext 上下文
- [x] `source/guide/config.md` — 配置系统 PluginConfig
- [x] `source/guide/responses.md` — 响应格式 ok() / fail()
- [x] `source/guide/state.md` — 状态持久化
- [x] `source/guide/hooks.md` — Hook 系统
- [x] `source/guide/router.md` — 路由器 PluginRouter
- [x] `source/guide/plugins-call.md` — 跨插件调用 Plugins
- [x] `source/guide/database.md` — 数据库
- [x] `source/guide/store.md` — 键值存储 PluginStore

---

## 第三层：Architecture（系统架构）

### 3.0 总览
- [x] `source/architecture/index.md` — 架构总览 + 分层依赖图

### 3.1 Bus 通信系统
- [x] `source/architecture/bus/index.md` — Bus 概述
- [x] `source/architecture/bus/records.md` — BusRecord + BusFilter
- [x] `source/architecture/bus/messages.md` — MessageClient / MessageRecord
- [x] `source/architecture/bus/events.md` — EventClient / EventRecord
- [x] `source/architecture/bus/lifecycle.md` — LifecycleClient / LifecycleRecord
- [x] `source/architecture/bus/conversations.md` — ConversationClient / ConversationRecord
- [x] `source/architecture/bus/memory.md` — MemoryClient / MemoryRecord
- [x] `source/architecture/bus/bus-list.md` — BusList 核心操作
- [x] `source/architecture/bus/watchers.md` — BusListWatcher / BusListDelta

### 3.2 Run/Export 执行系统
- [x] `source/architecture/runs/index.md` — Run 概述
- [x] `source/architecture/runs/run-lifecycle.md` — RunRecord 状态机
- [x] `source/architecture/runs/run-progress.md` — 进度上报
- [x] `source/architecture/runs/exports.md` — Export 通道
- [x] `source/architecture/runs/run-api.md` — HTTP & WebSocket API
- [x] `source/architecture/runs/run-storage.md` — RunStore / ExportStore 协议

### 3.3 Message Plane 消息平面
- [x] `source/architecture/message-plane/index.md` — 概述
- [x] `source/architecture/message-plane/protocol.md` — RPC 协议
- [x] `source/architecture/message-plane/stores.md` — TopicStore
- [x] `source/architecture/message-plane/transport.md` — 传输层
- [x] `source/architecture/message-plane/bridge.md` — PlaneBridge

### 3.4 Adapter 协议适配
- [x] `source/architecture/adapter/index.md` — Adapter 概述
- [x] `source/architecture/adapter/modes.md` — 四种工作模式
- [x] `source/architecture/adapter/gateway-core.md` — AdapterGatewayCore
- [x] `source/architecture/adapter/contracts.md` — 六管线接口契约
- [x] `source/architecture/adapter/building-adapter.md` — 构建自定义 Adapter 指南

### 3.5 内部机制
- [x] `source/architecture/internals/index.md` — 内部机制总览
- [x] `source/architecture/internals/ipc.md` — 进程间通信
- [x] `source/architecture/internals/worker.md` — Worker 模式
- [x] `source/architecture/internals/call-chain.md` — 调用链追踪
- [x] `source/architecture/internals/registry.md` — 插件注册表
- [x] `source/architecture/internals/host.md` — Host 进程管理
- [x] `source/architecture/internals/state-machine.md` — 全局状态机

---

## 第四层：Examples（完整示例）

- [x] `source/examples/index.md` — 示例总览
- [x] `source/examples/hello-world.md` — 最简插件
- [x] `source/examples/file-processor.md` — 文件处理
- [x] `source/examples/api-client.md` — Web API 客户端
- [x] `source/examples/data-collector.md` — 数据采集
- [x] `source/examples/stateful-plugin.md` — 状态持久化
- [x] `source/examples/router-plugin.md` — 路由器模块化
- [x] `source/examples/hook-plugin.md` — Hook 中间件
- [x] `source/examples/bus-watcher.md` — Bus 实时监听
- [x] `source/examples/run-progress.md` — Run 进度上报
- [x] `source/examples/mcp-adapter.md` — MCP Adapter

---

## 第五层：Reference（API 参考 — Sphinx autodoc 自动生成）

### 5.1 SDK 公开 API
- [x] `source/reference/index.md` — API 参考总览
- [x] `source/reference/sdk/base.rst` — NekoPluginBase
- [x] `source/reference/sdk/decorators.rst` — 装饰器 API
- [x] `source/reference/sdk/config.rst` — PluginConfig API
- [x] `source/reference/sdk/router.rst` — PluginRouter API
- [x] `source/reference/sdk/hooks.rst` — Hook API
- [x] `source/reference/sdk/state.rst` — StatePersistence API
- [x] `source/reference/sdk/database.rst` — PluginDatabase API
- [x] `source/reference/sdk/store.rst` — PluginStore API
- [x] `source/reference/sdk/plugins.rst` — Plugins API
- [x] `source/reference/sdk/responses.rst` — ok() / fail() API
- [x] `source/reference/sdk/memory.rst` — MemoryClient API
- [x] `source/reference/sdk/system-info.rst` — SystemInfo API
- [x] `source/reference/sdk/types.rst` — SDK 类型

### 5.2 Bus API
- [x] `source/reference/bus/types.rst` — BusList / BusRecord / BusFilter
- [x] `source/reference/bus/records.rst` — BusRecord 基类
- [x] `source/reference/bus/messages.rst` — MessageClient / MessageRecord
- [x] `source/reference/bus/events.rst` — EventClient / EventRecord
- [x] `source/reference/bus/lifecycle.rst` — LifecycleClient / LifecycleRecord
- [x] `source/reference/bus/conversations.rst` — ConversationClient / ConversationRecord
- [x] `source/reference/bus/watchers.rst` — BusListWatcher / BusListDelta

### 5.3 Adapter API
- [x] `source/reference/adapter/base.rst` — AdapterBase / AdapterConfig
- [x] `source/reference/adapter/gateway-core.rst` — AdapterGatewayCore
- [x] `source/reference/adapter/gateway-models.rst` — Gateway 数据模型
- [x] `source/reference/adapter/contracts.rst` — 六管线接口
- [x] `source/reference/adapter/types.rst` — Adapter 类型

### 5.4 类型定义 API
- [x] `source/reference/types/errors.rst` — ErrorCode
- [x] `source/reference/types/result.rst` — Ok / Err / Result
- [x] `source/reference/types/exceptions.rst` — 异常层级
- [x] `source/reference/types/models.rst` — 数据模型
- [x] `source/reference/types/events.rst` — 事件类型
- [x] `source/reference/types/protocols.rst` — Protocol 接口

### 5.5 Server API
- [x] `source/reference/server/runs.rst` — Run/Export 管理器
- [x] `source/reference/server/services.rst` — 核心服务
- [x] `source/reference/server/routes.rst` — HTTP API 端点

---

## 其他

- [x] `source/faq.md` — 常见问题 & 故障排查

---

## 统计

| 层 | 页数 | 受众 | 状态 |
|---|---|---|---|
| 基础设施 | 4 | — | ✅ |
| Getting Started | 4 | 新手 | ✅ |
| Guide | 11 | 插件开发者 | ✅ |
| Architecture | 30 | 高级开发者 | ✅ |
| Examples | 11 | 所有人 | ✅ |
| Reference | 31 | 所有人 | ✅ |
| FAQ | 1 | 所有人 | ✅ |
| **总计** | **92** | | **✅ 全部完成** |

## 构建方式

```bash
cd plugin/neko-plugin-docs
pip install -r requirements.txt
make html
# 输出在 build/html/
```
