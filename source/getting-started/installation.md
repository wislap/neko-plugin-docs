# 环境准备

## 系统要求

| 要求 | 最低版本 |
|------|----------|
| Python | 3.10+ |
| pip | 最新版 |
| OS | Linux / macOS / Windows |

## 依赖安装

N.E.K.O 插件系统的核心依赖会随主项目一起安装。插件开发者通常只需要关注 SDK 部分。

### 核心依赖

```bash
# SDK 核心（随主项目安装）
pip install pydantic fastapi loguru

# 可选：高性能序列化
pip install ormsgpack

# 可选：ZeroMQ 通信
pip install pyzmq

# 可选：数据库支持
pip install sqlalchemy aiosqlite
```

### 开发工具（可选）

```bash
# 类型检查
pip install mypy pyright

# 代码格式化
pip install ruff black

# 测试
pip install pytest pytest-asyncio
```

## 验证安装

```python
from plugin.sdk import SDK_VERSION, NekoPluginBase, neko_plugin
print(f"SDK Version: {SDK_VERSION}")
```

如果没有报错，说明环境已就绪。

## 目录结构

插件代码放在 `plugin/plugins/` 目录下：

```
plugin/
├── plugins/              # 所有插件
│   ├── my_plugin/        # 你的插件
│   │   ├── __init__.py   # 插件主代码
│   │   └── plugin.toml   # 插件配置
│   └── ...
├── sdk/                  # SDK 源码（不需要修改）
└── server/               # 服务端（不需要修改）
```

:::{note}
插件开发者通常只需要在 `plugin/plugins/` 下创建自己的目录，不需要修改 SDK 或 Server 代码。
:::
