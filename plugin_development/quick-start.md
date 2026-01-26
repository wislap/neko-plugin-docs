# 插件开发快速上手指南

> 从零开始创建一个可被识别和运行的 N.E.K.O 插件 - 超详细版

---

## 前置要求

- Python 3.11 或更高版本
- N.E.K.O 已下载
- 文本编辑器 (如 VS Code, 或记事本)

**不需要**:
- ❌ 不需要高级编程知识
- ❌ 不需要了解异步编程 (我们会提供完整代码)

---

## 第一步: 找到插件目录

### 方法 A: 使用文件管理器

1. **打开文件管理器** (Windows 资源管理器 / macOS Finder / Linux 文件管理器)

2. **导航到 N.E.K.O 项目目录**

3. **进入 plugin 文件夹**
   - 双击打开 `plugin` 文件夹

4. **进入 plugins 文件夹**
   - 双击打开 `plugins` 文件夹
   - 这里存放所有的插件

5. **为插件创建文件夹**
   - **Windows**: 右键 → 新建 → 文件夹 → 命名为 `hello_world`
   - **macOS**: 右键 → 新建文件夹 → 命名为 `hello_world`
   - **Linux**: 右键 → 创建文件夹 → 命名为 `hello_world`

6. **进入新创建的文件夹**
   - 双击打开 `hello_world` 文件夹

现在你应该在这个路径: `N.E.K.O/plugin/plugins/hello_world/`

### 方法 B: 使用命令行

**Windows (PowerShell 或 CMD)**:
```powershell
# 1. 打开 PowerShell 或命令提示符
# 2. 导航到 N.E.K.O 目录
cd C:\Users\YourName\N.E.K.O\plugin

# 3. 创建插件目录
mkdir plugins\hello_world

# 4. 进入插件目录
cd plugins\hello_world

# 5. 确认当前位置
pwd
# 应该显示: C:\Users\YourName\N.E.K.O\plugin\plugins\hello_world
```

**Linux / macOS (Terminal)**:
```bash
# 1. 打开终端
# 2. 导航到 N.E.K.O 目录
cd /home/yourname/N.E.K.O/plugin

# 3. 创建插件目录
mkdir -p plugins/hello_world

# 4. 进入插件目录
cd plugins/hello_world

# 5. 确认当前位置
pwd
# 应该显示: /home/yourname/N.E.K.O/plugin/plugins/hello_world
```

**目录结构确认**:
```
N.E.K.O/
└── plugin/
    └── plugins/
        └── hello_world/          ← 你现在在这里
            (空的,我们接下来会创建文件)
```

---

## 第二步: 创建配置文件

### 方法 A: 使用文本编辑器

1. **打开文本编辑器**
   - **Windows**: 记事本 (Notepad) 或 VS Code
   - **macOS**: 文本编辑 (TextEdit) 或 VS Code
   - **Linux**: gedit, nano, 或 VS Code

2. **创建新文件**
   - 点击 "文件" → "新建"

3. **复制以下内容** (完整复制,不要修改):

```toml
[plugin]
name = "Hello World Plugin"
description = "A simple hello world plugin for demonstration"
version = "0.1.0"
id = "hello_world"
entry = "plugins.hello_world:HelloWorldPlugin"

[plugin.author]
name = "Your Name"
email = "your.email@example.com"
url = "https://your-website.com"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"
supported = ">=0.1.0,<0.3.0"
untested = ">=0.3.0,<0.4.0"
conflicts = [
    "<0.1.0",
    ">=0.4.0",
]

[plugin_runtime]
enabled = true
auto_start = true

[plugin.store]
enabled = false

[my_settings]
greeting = "Hello"
max_retries = 3
timeout_seconds = 5.0
```

4. **保存文件**
   - 点击 "文件" → "保存"
   - **重要**: 文件名必须是 `plugin.toml` (不是 `plugin.toml.txt`)
   - 保存位置: `N.E.K.O/plugin/plugins/hello_world/plugin.toml`

**Windows 用户注意**:
- 如果使用记事本,保存时:
  - 文件名输入: `plugin.toml`
  - 保存类型选择: "所有文件 (*.*)"
  - 编码选择: "UTF-8"

### 方法 B: 使用命令行创建文件

**Windows (PowerShell)**:
```powershell
# 确保你在 hello_world 目录下
cd C:\Users\YourName\N.E.K.O\plugin\plugins\hello_world

# 创建 plugin.toml 文件
@"
[plugin]
name = "Hello World Plugin"
description = "A simple hello world plugin for demonstration"
version = "0.1.0"
id = "hello_world"
entry = "plugins.hello_world:HelloWorldPlugin"

[plugin.author]
name = "Your Name"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"
supported = ">=0.1.0,<0.3.0"

[plugin_runtime]
enabled = true
auto_start = true

[my_settings]
greeting = "Hello"
"@ | Out-File -FilePath plugin.toml -Encoding UTF8
```

**Linux / macOS (Terminal)**:
```bash
# 确保你在 hello_world 目录下
cd /home/yourname/N.E.K.O/plugin/plugins/hello_world

# 创建 plugin.toml 文件
cat > plugin.toml << 'EOF'
[plugin]
name = "Hello World Plugin"
description = "A simple hello world plugin for demonstration"
version = "0.1.0"
id = "hello_world"
entry = "plugins.hello_world:HelloWorldPlugin"

[plugin.author]
name = "Your Name"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"
supported = ">=0.1.0,<0.3.0"

[plugin_runtime]
enabled = true
auto_start = true

[my_settings]
greeting = "Hello"
EOF
```

### 验证文件创建成功

**使用文件管理器**:
- 在 `hello_world` 文件夹中应该看到 `plugin.toml` 文件
- 文件大小应该约 400-500 字节

---

## 第二步补充: 配置文件详解

现在我们来理解刚才创建的配置文件:

```toml
# ============================================
# 插件基本信息 (必需)
# ============================================
[plugin]
# 插件显示名称
name = "Hello World Plugin"

# 插件描述
description = "A simple hello world plugin for demonstration"

# 插件版本 (遵循语义化版本)
version = "0.1.0"

# 插件唯一标识符 (必须与目录名一致)
# 只能包含字母、数字、下划线和连字符
id = "hello_world"

# 插件入口点 (格式: 模块路径:类名)
# 模块路径相对于 plugin/ 目录
entry = "plugins.hello_world:HelloWorldPlugin"

# ============================================
# 作者信息 (可选但推荐)
# ============================================
[plugin.author]
name = "Your Name"
email = "your.email@example.com"
url = "https://your-website.com"

# ============================================
# SDK 版本兼容性 (必需)
# ============================================
[plugin.sdk]
# 推荐的 SDK 版本范围
recommended = ">=0.1.0,<0.2.0"

# 支持的 SDK 版本范围
supported = ">=0.1.0,<0.3.0"

# 未测试但可能兼容的版本
untested = ">=0.3.0,<0.4.0"

# 已知不兼容的版本
conflicts = [
    "<0.1.0",
    ">=0.4.0",
]

# ============================================
# 运行时配置 (必需)
# ============================================
[plugin_runtime]
# 是否启用插件
enabled = true

# 服务器启动时是否自动启动插件
auto_start = true

# ============================================
# 插件存储配置 (可选)
# ============================================
[plugin.store]
# 是否启用持久化 KV 存储
# 启用后可以在插件中使用 sqlite
enabled = false

# ============================================
# 自定义配置 (可选)
# ============================================
# 你可以添加任意自定义配置节,这一部分不会影响插件的识别
[my_settings]
greeting = "Hello"
max_retries = 3
timeout_seconds = 5.0
```

### 配置字段详解

#### `[plugin]` 节 - 必需字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ✅ | 插件显示名称 |
| `description` | string | ✅ | 插件功能描述 |
| `version` | string | ✅ | 版本号 (语义化版本) |
| `id` | string | ✅ | 唯一标识符,必须与目录名一致 |
| `entry` | string | ✅ | 入口点,格式: `模块路径:类名` |

#### `[plugin.sdk]` 节 - 版本兼容性

使用版本范围语法 (类似 pip):
- `>=0.1.0`: 大于等于 0.1.0
- `<0.2.0`: 小于 0.2.0
- `>=0.1.0,<0.2.0`: 组合条件

#### `[plugin_runtime]` 节 - 运行时行为

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enabled` | boolean | true | 是否启用插件 |
| `auto_start` | boolean | false | 是否自动启动 |

---

## 第三步: 创建插件代码文件

### 方法 A: 使用文本编辑器 (推荐新手)

1. **打开文本编辑器** (同第二步)

2. **创建新文件**
   - 点击 "文件" → "新建"

3. **复制以下完整代码** (不要修改任何内容):

```python
# 最简单的 Hello World 插件 (使用同步函数)
from plugin.sdk.base import NekoPluginBase
from plugin.sdk.decorators import neko_plugin, plugin_entry, worker


@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        # 使用插件自带的 logger (推荐!)
        self.logger.info("Hello World Plugin 已加载!")
    
    @plugin_entry(id="hello")
    @worker(timeout=10.0)
    def hello(self, input_data):
        name = input_data.get("name", "World")
        # 记录日志
        self.logger.info(f"收到问候请求: name={name}")
        return {"message": f"Hello, {name}!"}
```

**代码说明** (只有 18 行!):
- 第 1-2 行: 导入必需的类和装饰器
- 第 6 行: `@neko_plugin` 装饰器标记这是一个插件
- 第 7 行: 插件类,继承 `NekoPluginBase`
- 第 8-10 行: 初始化方法,必须调用 `super().__init__(ctx)`
- 第 10 行: 使用 `self.logger` 记录日志 (**推荐使用 logger 而不是 print**)
- 第 12 行: `@plugin_entry(id="hello")` 装饰器 (**必须提供 id 参数**)
- 第 13 行: `@worker(timeout=10.0)` 装饰器
- 第 14-18 行: `hello` 方法,接收输入,记录日志,返回问候消息

**为什么使用 `self.logger` 而不是 `print`?**

| 功能 | `self.logger` | `print` |
|------|--------------|---------|
| 日志级别 | ✅ 支持 (INFO, WARNING, ERROR) | ❌ 无 |
| 自动保存到文件 | ✅ 是 | ❌ 否 |
| 时间戳 | ✅ 自动添加 | ❌ 无 |
| 格式化 | ✅ 统一格式 | ❌ 随意 |
| 生产环境 | ✅ 适合 | ❌ 不适合 |

**推荐做法**: 始终使用 `self.logger` 记录信息!

**这就是全部!** 使用普通的同步函数,就像写普通 Python 代码一样简单!

> 💡 **提示**: 想了解更多高级功能? 先完成第四步启动插件,然后回到本页底部查看"进阶主题"章节。

4. **保存文件**
   - 点击 "文件" → "保存"
   - **重要**: 文件名必须是 `__init__.py` (两个下划线,init,两个下划线,.py)
   - 保存位置: `N.E.K.O/plugin/plugins/hello_world/__init__.py`

**文件名说明**:
- ✅ 正确: `__init__.py`
- ❌ 错误: `init.py`
- ❌ 错误: `_init_.py`
- ❌ 错误: `__init__.py.txt`

### 方法 B: 使用命令行创建文件

由于代码较长,建议使用文本编辑器。如果必须使用命令行:

**Linux / macOS**:
```bash
# 下载示例代码
curl -o __init__.py https://raw.githubusercontent.com/your-repo/hello_world/__init__.py

# 或者使用 nano 编辑器
nano __init__.py
# 然后粘贴代码,按 Ctrl+X, Y, Enter 保存
```

**Windows**:
```powershell
# 使用 notepad 打开
notepad __init__.py
# 粘贴代码,保存
```

### 验证文件创建成功

**使用文件管理器**:
- 在 `hello_world` 文件夹中应该看到:
  - `plugin.toml` (配置文件)
  - `__init__.py` (代码文件)

**使用命令行**:
```bash
# Windows
dir

# Linux / macOS
ls -lh

# 应该看到两个文件:
# plugin.toml
# __init__.py
```

**最终目录结构**:
```
N.E.K.O/
└── plugin/
    └── plugins/
        └── hello_world/
            ├── __init__.py       ✅ 已创建
            └── plugin.toml       ✅ 已创建
```

---

## 第三步补充: 代码详解

#### 1. 必需的导入

```python
from plugin.sdk.base import NekoPluginBase
from plugin.sdk.decorators import neko_plugin, plugin_entry, lifecycle
from plugin.sdk import ok, err
```

- `NekoPluginBase`: 所有插件的基类
- `@neko_plugin`: 标记插件类的装饰器 (必需)
- `@plugin_entry`: 标记可调用入口点的装饰器
- `@lifecycle`: 标记生命周期钩子的装饰器
- `ok`, `err`: 构造标准响应的辅助函数

#### 2. 插件类定义

```python
@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
```

- 必须使用 `@neko_plugin` 装饰器
- 必须继承 `NekoPluginBase`
- 必须实现 `__init__(self, ctx)` 构造函数
- 必须调用 `super().__init__(ctx)`

#### 3. 上下文对象 (ctx)

`ctx` 提供插件运行时信息:
- `ctx.plugin_id`: 插件ID
- `ctx.version`: 插件版本
- `ctx.config`: 配置对象
- `ctx.push_message()`: 推送消息
- `ctx.now_iso()`: 获取当前时间 (ISO 8601 格式)

#### 4. 生命周期钩子

```python
# 异步生命周期钩子
@lifecycle(id="startup")
async def on_startup(self):
    pass

# 同步生命周期钩子 (推荐加 @worker)
@lifecycle(id="shutdown")
@worker(timeout=5.0)
def on_shutdown(self):
    pass
```

支持的生命周期事件:
- `startup`: 插件启动时
- `shutdown`: 插件关闭时
- `reload`: 插件重载时
- `freeze`: 插件冻结前
- `unfreeze`: 插件恢复后

#### 5. 入口点

```python
# 异步入口点 (推荐)
@plugin_entry(id="my_async_function")  # 必须提供 id
async def my_async_function(self, input_data):
    return ok({"result": "success"})

# 同步入口点 (需要添加 @worker)
@plugin_entry(id="my_sync_function")  # 必须提供 id
@worker(timeout=10.0)
def my_sync_function(self, input_data):
    return ok({"result": "success"})
```

- 使用 `@plugin_entry(id="函数名")` 装饰器标记 (**必须提供 id 参数**)
- `id` 参数通常与函数名相同,用于标识这个入口点
- 可以是异步函数 (`async def`) 或同步函数 (`def`)
- 同步函数**强烈推荐**添加 `@worker(timeout=10.0)` 装饰器
- 接收 `input_data` 参数 (字典)
- 返回字典 (推荐使用 `ok()` 或 `err()`)

---

## 第四步: 启动和测试插件

### 1. 打开命令行/终端

**Windows**:
- 按 `Win + R`
- 输入 `cmd` 或 `powershell`
- 按回车

**macOS**:
- 按 `Cmd + Space`
- 输入 `Terminal`
- 按回车

**Linux**:
- 在应用菜单中找到 "终端"

### 2. 导航到 plugin 目录

**Windows**:
```powershell
# 替换为你的实际路径
cd C:\Users\YourName\N.E.K.O\plugin
```

**Linux / macOS**:
```bash
# 替换为你的实际路径
cd /home/yourname/N.E.K.O/plugin
```



### 3. 启动插件服务器

**标准 Python**:
```bash
# Python 3
python -m plugin.user_plugin_server

# 或者
python3 -m plugin.user_plugin_server
```

**使用 uv** (推荐,更快):
```bash
# 如果已安装 uv
uv run python -m plugin.user_plugin_server
```

**使用 Conda**:
```bash
# 激活 conda 环境
conda activate your_env_name

# 启动服务器
python -m plugin.user_plugin_server
```

**使用 Poetry**:
```bash
# 使用 poetry 运行
poetry run python -m plugin.user_plugin_server
```

**成功启动的标志**:
你应该看到类似以下的输出:
```
2026-01-26 14:16:52 | INFO     | User plugin server starting on 127.0.0.1:48916
2026-01-26 14:16:52 | INFO     | Started server process [15774]
2026-01-26 14:16:52 | INFO     | Waiting for application startup.
2026-01-26 14:16:52.180 | INFO     | Plugin router started
2026-01-26 14:16:52.483 | INFO     | Loading plugins from /home/.../plugin/plugins
2026-01-26 14:16:52.483 | INFO     | Found 2 plugin.toml files: [.../hello_world/plugin.toml, ...]
2026-01-26 14:16:52.484 | INFO     | Plugin ID: hello_world
2026-01-26 14:16:52.497 | INFO     | Plugin hello_world process started (pid: 15802)
2026-01-26 14:16:52 | INFO     | [Proc-hello_world] HelloWorldPlugin initialized!

============================================================
🔐 管理员验证码: XXXX
============================================================
请在请求头中添加: Authorization: Bearer <验证码>
============================================================

2026-01-26 14:16:52.603 | INFO     | Uvicorn running on http://127.0.0.1:48916 (Press CTRL+C to quit)
```

**关键信息**:
- ✅ 看到 "User plugin server starting" - 服务器正在启动
- ✅ 看到 "Loading plugins from" - 正在加载插件
- ✅ 看到 "Plugin ID: hello_world" - 找到你的插件
- ✅ 看到 "HelloWorldPlugin initialized!" - 插件成功初始化
- ✅ 看到管理员验证码 - 用于访问管理端点
- ✅ 看到 "Uvicorn running on http://..." - 服务器运行中

**注意**: 端口号可能不同 (如 48916, 48912 等),这是正常的。

### 4. 保持服务器运行

**重要**: 不要关闭这个命令行窗口!
- 服务器需要一直运行
- 你会在这里看到插件的日志输出
- 要停止服务器,按 `Ctrl + C`

### 5. 检查插件状态

**方法 A: 使用浏览器** (最简单)

1. **打开浏览器** (Chrome, Firefox, Edge 等)

2. **在地址栏输入**:
   ```
   http://127.0.0.1:48912/plugins
   ```

3. **按回车**

4. **你应该看到**:

```json
{
  "plugins": [
    {
      "id": "hello_world",
      "name": "Hello World Plugin",
      "version": "0.1.0",
      "status": "running",
      "enabled": true
    }
  ]
}
```

**方法 B: 使用命令行**

打开**新的**命令行窗口 (不要关闭服务器窗口):

**Windows (PowerShell)**:
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:48912/plugins" | Select-Object -ExpandProperty Content
```

**Linux / macOS**:
```bash
curl http://127.0.0.1:48912/plugins
```

### 6. 测试插件功能

现在我们来调用插件的 `hello` 方法!

**方法 A: 使用在线工具** (最简单)

1. 打开浏览器
2. 访问: `http://127.0.0.1:48912/ui` (如果有前端界面)
3. 或使用 Postman / Insomnia 等 API 测试工具

**方法 B: 使用命令行**

打开**新的**命令行窗口:

**Windows (PowerShell)**:
```powershell
# 创建运行请求
$body = @{
    plugin_id = "hello_world"
    input = @{
        name = "Alice"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:48912/runs" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**Linux / macOS**:
```bash
# 创建运行请求
curl -X POST http://127.0.0.1:48912/runs \
  -H "Content-Type: application/json" \
  -d '{
    "plugin_id": "hello_world",
    "input": {
      "name": "Alice"
    }
  }'
```

**成功的响应**:
```json
{
  "run_id": "run_abc123",
  "status": "pending",
  "run_token": "eyJhbGc...",
  "expires_at": "2026-01-26T15:30:00Z"
}
```

### 7. 查看插件日志

**方法 A: 使用文件管理器**

1. 导航到: `N.E.K.O/plugin/plugins/hello_world/logs/`
2. 找到 `hello_world.log` 文件
3. 双击打开 (用记事本或文本编辑器)
4. 你应该看到插件的运行日志

**方法 B: 使用命令行**

**Windows**:
```powershell
# 查看日志文件
type plugins\hello_world\logs\hello_world.log

# 实时查看日志 (需要安装 Git Bash 或 WSL)
Get-Content plugins\hello_world\logs\hello_world.log -Wait
```

**Linux / macOS**:
```bash
# 查看日志文件
cat plugins/hello_world/logs/hello_world.log

# 实时查看日志
tail -f plugins/hello_world/logs/hello_world.log
```

**日志示例**:
```
2026-01-26 14:16:52 | INFO     | [Proc-hello_world] Plugin file logger initialized: .../hello_world_20260126_141652.log
2026-01-26 14:16:52 | INFO     | [Proc-hello_world] HelloWorldPlugin initialized!
2026-01-26 14:16:52 | INFO     | [Proc-hello_world] Plugin instance created. Mapped entries: ['hello', ...]
```

**说明**:
- `[Proc-hello_world]` 表示这是来自 hello_world 插件进程的日志
- 日志文件会自动创建在 `plugins/hello_world/logs/` 目录下
- 文件名包含时间戳,如 `hello_world_20260126_141652.log`

---

## 进阶主题

### `@plugin_entry` 参数详解

`@plugin_entry` 装饰器支持多个参数,用于定义入口点的元数据:

```python
@plugin_entry(
    id="hello_run",                    # 必需: 入口点唯一标识符
    name="Hello (Run Demo)",           # 可选: 显示名称
    description="HelloWorld demo...",  # 可选: 功能描述
    input_schema={                     # 可选: 输入参数的 JSON Schema
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name to greet",
                "default": "world"
            },
            "sleep_seconds": {
                "type": "number",
                "description": "Simulated work time",
                "default": 0.6
            }
        },
        "required": []
    }
)
@worker(timeout=30.0)
def hello_run(self, name: str = "world", sleep_seconds: float = 0.6, **kwargs):
    return {"message": f"Hello, {name}!"}
```

**参数说明**:

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | str | ✅ | 入口点唯一标识符,通常与函数名相同 |
| `name` | str | ❌ | 显示名称,用于 UI 展示 |
| `description` | str | ❌ | 功能描述,说明这个入口点的作用 |
| `input_schema` | dict | ❌ | 输入参数的 JSON Schema,用于参数验证和文档生成 |
| `kind` | str | ❌ | 入口点类型: "action" (默认), "service" 等 |
| `persist` | bool | ❌ | 执行后是否保存状态 (需启用状态持久化) |

**input_schema 的作用**:
- ✅ 自动生成 API 文档
- ✅ 参数类型验证
- ✅ 提供默认值
- ✅ 前端 UI 自动生成表单

**简单示例 vs 完整示例**:

```python
# 简单示例 (只提供 id)
@plugin_entry(id="hello")
@worker(timeout=10.0)
def hello(self, input_data):
    name = input_data.get("name", "World")
    return {"message": f"Hello, {name}!"}

# 完整示例 (提供所有元数据)
@plugin_entry(
    id="hello",
    name="问候功能",
    description="向指定的人发送问候消息",
    input_schema={
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "要问候的人的名字",
                "default": "World"
            }
        }
    }
)
@worker(timeout=10.0)
def hello(self, name: str = "World", **kwargs):
    return {"message": f"Hello, {name}!"}
```

**推荐做法**:
- 新手: 只提供 `id` 参数即可
- 生产环境: 提供完整的元数据,便于维护和使用

---

### 同步函数 vs 异步函数

**新手推荐: 使用同步函数 + `@worker`**

同步函数就是普通的 Python 函数,更容易理解和编写:

```python
from plugin.sdk.decorators import worker

@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    # ✅ 同步函数 (推荐新手使用)
    @plugin_entry(id="hello")  # 必须提供 id 参数!
    @worker(timeout=10.0)
    def hello(self, input_data):
        name = input_data.get("name", "World")
        # 可以直接写普通代码
        result = f"Hello, {name}!"
        return {"message": result}
    
    # 同步函数可以做任何事情
    @plugin_entry(id="process_file")
    @worker(timeout=30.0)
    def process_file(self, input_data):
        # 读取文件
        with open("data.txt", "r") as f:
            content = f.read()
        # 处理数据
        result = content.upper()
        return {"result": result}
```

**进阶: 使用异步函数**

如果你熟悉 Python 异步编程,可以使用异步函数:

```python
@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    # 异步函数 (适合有异步编程经验的开发者)
    @plugin_entry(id="async_hello")
    async def async_hello(self, input_data):
        name = input_data.get("name", "World")
        # 可以使用 await 调用异步操作
        config = await self.config.get("greeting", default="Hello")
        return {"message": f"{config}, {name}!"}
```

**何时使用同步 vs 异步?**

| 场景 | 推荐 | 原因 |
|------|------|------|
| 新手开发者 | 同步 + `@worker` | 更简单,不需要理解 async/await |
| 文件读写 | 同步 + `@worker` | Python 文件操作是同步的 |
| 数据库查询 (同步库) | 同步 + `@worker` | 如 sqlite3 |
| 网络请求 (requests) | 同步 + `@worker` | requests 是同步库 |
| 需要调用插件 SDK 异步 API | 异步 | 如 `await self.config.get()` |
| 网络请求 (aiohttp) | 异步 | aiohttp 是异步库 |
| 数据库查询 (异步库) | 异步 | 如 asyncpg, motor |

**重要提示**:
- ✅ 同步函数**必须**添加 `@worker(timeout=10.0)` 装饰器
- ✅ `@worker` 让同步函数在线程池中运行,不会阻塞插件
- ✅ 异步函数**不需要** `@worker` 装饰器
- ✅ 不确定用哪个? 选择同步 + `@worker`!

### 生命周期钩子详解

生命周期钩子也支持同步和异步函数:

```python
from plugin.sdk.decorators import lifecycle, worker

@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    # 同步生命周期钩子 (推荐新手)
    @lifecycle(id="startup")
    @worker(timeout=5.0)
    def on_startup(self):
        self.logger.info("插件启动了!")
    
    # 异步生命周期钩子 (进阶)
    @lifecycle(id="shutdown")
    async def on_shutdown(self):
        await self.cleanup_resources()
```

**支持的生命周期事件**:
- `startup`: 插件启动时
- `shutdown`: 插件关闭时
- `reload`: 插件重载时
- `freeze`: 插件冻结前 (保存状态)
- `unfreeze`: 插件从冻结状态恢复后

### 日志功能详解

插件默认提供了 `self.logger`,可以直接使用:

```python
@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        # self.logger 默认可用,输出到控制台
        self.logger.info("插件初始化完成")
        self.logger.warning("这是一个警告")
        self.logger.error("这是一个错误")
```

**日志级别**:
- `self.logger.debug("调试信息")` - 调试级别
- `self.logger.info("普通信息")` - 信息级别 (推荐)
- `self.logger.warning("警告信息")` - 警告级别
- `self.logger.error("错误信息")` - 错误级别
- `self.logger.critical("严重错误")` - 严重错误级别

**启用文件日志** (可选,但推荐):

如果你想将日志保存到文件,可以启用文件日志:

```python
@neko_plugin
class HelloWorldPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        # 启用文件日志 (日志会保存到 plugins/hello_world/logs/)
        self.logger = self.enable_file_logging(log_level="INFO")
        self.logger.info("文件日志已启用!")
```

**文件日志的好处**:
- ✅ 日志自动保存到 `plugins/插件名/logs/` 目录
- ✅ 自动按日期和大小轮转
- ✅ 便于调试和问题排查
- ✅ 生产环境必备

**推荐**: 在 `__init__` 中启用文件日志!

---

## 常见问题

### Q1: 插件没有被识别?

**检查清单**:
- ✅ 插件目录在 `plugin/plugins/` 下
- ✅ 存在 `plugin.toml` 文件
- ✅ 存在 `__init__.py` 文件
- ✅ `plugin.toml` 中的 `id` 与目录名一致
- ✅ `entry` 指向正确的类

### Q2: 插件启动失败?

**检查**:
1. 查看服务器日志: `python -m plugin.user_plugin_server`
2. 查看插件日志: `plugins/hello_world/logs/`
3. 检查 `__init__` 方法是否调用了 `super().__init__(ctx)`
4. 检查是否有语法错误

### Q3: 入口点无法调用?

**检查**:
- ✅ 方法使用了 `@plugin_entry` 装饰器
- ✅ 方法是异步函数 (`async def`)
- ✅ 插件状态为 `running`

### Q4: 配置无法读取?

**检查**:
- ✅ 配置路径正确 (使用点号分隔,如 `my_settings.greeting`)
- ✅ 使用 `await self.config.get()`
- ✅ 配置存在于 `plugin.toml` 中

---

## 完整示例代码

完整的 `hello_world` 插件代码已在上面展示。你可以直接复制使用,或者参考 `plugins/testPlugin/` 获取更多示例。

**关键要点**:
- ✅ `plugin.toml` 配置正确
- ✅ 继承 `NekoPluginBase`
- ✅ 使用 `@neko_plugin` 装饰器
- ✅ 实现 `__init__(self, ctx)`
- ✅ 使用 `@plugin_entry` 定义入口点
- ✅ 使用 `@lifecycle` 处理生命周期事件

祝你开发愉快! 🎉
