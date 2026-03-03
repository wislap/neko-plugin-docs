# 创建第一个插件

> 目标：从 0 到 1 创建一个 `hello_world` 插件，并在插件管理界面中成功触发。

## 你将完成什么

- 创建插件目录与 `plugin.toml`
- 编写一个最小可运行的插件类
- 启动插件服务器并在 UI 里触发入口点
- 通过 `/runs` API 进行一次可脚本化调用（可选）

---

## 0. 前置条件

- 已完成环境准备：`installation.md`
- 你当前位于项目根目录：`N.E.K.O/`
- Python 3.11+（建议和主项目一致）

---

## 1. 创建插件目录

在项目根目录执行：

```bash
mkdir -p plugin/plugins/hello_world
```

期望结构：

```text
N.E.K.O/
└── plugin/
    └── plugins/
        └── hello_world/
```

---

## 2. 创建 `plugin.toml`

新建文件：`plugin/plugins/hello_world/plugin.toml`

```toml
[plugin]
id = "hello_world"
name = "Hello World Plugin"
description = "My first N.E.K.O plugin"
version = "0.1.0"
entry = "plugins.hello_world:HelloWorldPlugin"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"
supported = ">=0.1.0,<0.3.0"
untested = ">=0.3.0,<0.4.0"
conflicts = ["<0.1.0", ">=0.4.0"]

[plugin_runtime]
enabled = true
auto_start = true
```

:::{note}
最关键的是两个字段：
- `id`：插件唯一标识（建议与目录名一致）
- `entry`：入口类路径，格式 `模块路径:类名`
:::

---

## 3. 创建插件代码

新建文件：`plugin/plugins/hello_world/__init__.py`

```python
from plugin.sdk import NekoPluginBase, neko_plugin, plugin_entry, worker, ok


@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.logger.info("HelloWorldPlugin initialized")

    # 不传 id 时，默认使用函数名 greet 作为 entry_id
    @plugin_entry(name="Greet", description="Return greeting message")
    @worker(timeout=10.0)
    def greet(self, name: str = "World", **_):
        self.logger.info("greet called, name={}", name)
        return ok(data={"message": f"Hello, {name}!"})
```

### 这段代码的关键点

- 必须使用 `@neko_plugin` 标记插件类
- 插件类必须继承 `NekoPluginBase`
- `@plugin_entry` 可以不写 `id`，系统会自动使用函数名
- `input_schema` 也可以不手写，系统会根据函数签名自动推断
- 同步函数建议加 `@worker`，避免阻塞

---

## 4. 启动插件服务器

在项目根目录执行：

```bash
uv run python -m plugin.user_plugin_server
```

若你不用 `uv`：

```bash
python -m plugin.user_plugin_server
```

看到类似日志表示启动成功：

```text
User plugin server starting on 127.0.0.1:48916
... Loading plugins from .../plugin/plugins
... Plugin ID: hello_world
... Uvicorn running on http://127.0.0.1:48916
```

:::{important}
如果 `48916` 被占用，服务会自动切换到其他端口。请以终端日志中的实际端口为准。
:::

---

## 5. 在 UI 中触发插件

1. 浏览器打开：`http://127.0.0.1:48916/ui`（替换成你的实际端口）
2. 输入启动日志中的 4 位管理员验证码
3. 进入 `Plugins` 页面，找到 `hello_world`
4. 进入入口点列表，触发 `greet`
5. 参数示例：`{"name": "N.E.K.O"}`

成功后应看到返回：

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "message": "Hello, N.E.K.O!"
  }
}
```

---

## 6. 用 `/runs` API 触发（可选）

### 6.1 创建一次 run

```bash
curl -X POST http://127.0.0.1:48916/runs \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "hello_world",
    "entry_id": "greet",
    "args": {"name": "API"}
  }'
```

典型返回：

```json
{
  "run_id": "...",
  "status": "running",
  "run_token": "...",
  "expires_at": 1234567890
}
```

### 6.2 查询 run 结果

```bash
curl http://127.0.0.1:48916/runs/<run_id>
```

---

## 7. 查看日志

插件日志通常在：

```text
plugin/plugins/hello_world/logs/
```

实时查看：

```bash
tail -f plugin/plugins/hello_world/logs/*.log
```

---

## 常见问题

| 问题 | 现象 | 排查要点 |
|------|------|----------|
| 插件未显示 | UI 里看不到 `hello_world` | `plugin.toml` 路径是否正确；`id` 是否重复；`entry` 是否可导入 |
| 插件加载失败 | 启动日志报 import 错误 | `entry = "plugins.hello_world:HelloWorldPlugin"` 是否与类名一致 |
| 入口点不存在 | 调用时报 `entry_id` 错误 | `greet` 方法是否加了 `@plugin_entry` |
| 参数校验失败 | 调用时报参数类型错误 | `greet(name: str = "World")` 的类型与传参是否一致 |

---

## 下一步

- 学习装饰器：`../guide/decorators.md`
- 学习上下文能力：`../guide/context.md`
- 学习状态管理：`../guide/state.md`
- 查看完整示例：`../examples/index.md`
