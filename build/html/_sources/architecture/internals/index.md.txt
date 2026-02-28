# 内部机制

本章介绍 N.E.K.O 插件系统的底层内部机制，面向核心贡献者和需要深入调试的开发者。

## 概览

| 机制 | 模块 | 说明 |
|------|------|------|
| [进程间通信](ipc.md) | `core/communication.py`, `utils/zeromq_ipc.py` | ZeroMQ IPC + 命令/响应队列 |
| [Worker 模式](worker.md) | `core/worker.py` | 线程池 + contextvars 传播 |
| [调用链追踪](call-chain.md) | `sdk/call_chain.py` | 循环检测 + 深度限制 |
| [插件注册表](registry.md) | `core/registry.py` | 插件发现 + 依赖解析 |
| [Host 进程](host.md) | `core/host.py` | 子进程管理 + 命令分发 |
| [全局状态机](state-machine.md) | `core/state.py` | 单例状态 + 插件列表 |

```{toctree}
:maxdepth: 2

ipc
worker
call-chain
registry
host
state-machine
```
