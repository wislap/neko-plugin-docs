# N.E.K.O 插件开发文档

> 完整的 N.E.K.O 插件开发指南

---

## 📚 文档导航

### 入门指南

1. **[快速上手](./quick-start.md)**
   - 创建第一个插件
   - 插件结构和配置
   - 基本功能实现

### 核心概念

2. **插件生命周期**
   - 启动和关闭流程
   - 生命周期钩子
   - 状态管理

3. **SDK API 参考**
   - 基础类和装饰器
   - 配置管理
   - 消息和事件
   - 数据存储

### 高级主题

4. **Run Protocol 集成**
   - 处理运行请求
   - WebSocket 通信
   - 文件上传下载

5. **插件间通信**
   - 调用其他插件
   - 消息总线使用
   - 事件订阅

6. **性能优化**
   - 异步编程
   - 资源管理
   - 性能监控

### 最佳实践

7. **开发规范**
   - 代码风格
   - 错误处理
   - 日志记录

8. **测试和调试**
   - 单元测试
   - 集成测试
   - 调试技巧

9. **部署和发布**
   - 打包插件
   - 版本管理
   - 依赖管理

---

## 🚀 快速开始

```bash
# 1. 创建插件目录
mkdir -p plugin/plugins/my_plugin

# 2. 创建配置文件
cat > plugin/plugins/my_plugin/plugin.toml << EOF
[plugin]
name = "My Plugin"
description = "My first N.E.K.O plugin"
version = "0.1.0"
id = "my_plugin"
entry = "plugins.my_plugin:MyPlugin"

[plugin.author]
name = "Your Name"

[plugin.sdk]
recommended = ">=0.1.0,<0.2.0"

[plugin_runtime]
enabled = true
auto_start = true
EOF

# 3. 创建插件代码
cat > plugin/plugins/my_plugin/__init__.py << EOF
from plugin.sdk.base import NekoPluginBase
from plugin.sdk.decorators import neko_plugin, plugin_entry

@neko_plugin
class MyPlugin(NekoPluginBase):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.logger.info("MyPlugin initialized!")
    
    @plugin_entry
    async def hello(self, input_data):
        return {"message": f"Hello, {input_data.get('name', 'World')}!"}
EOF

# 4. 启动插件服务器
python -m plugin.user_plugin_server
```

---

## 📖 核心概念

### 插件结构

```
my_plugin/
├── __init__.py          # 插件主代码
├── plugin.toml          # 插件配置
├── pyproject.toml       # Python 依赖 (可选)
├── requirements.txt     # Python 依赖 (可选)
└── logs/                # 日志目录 (自动创建)
```

### 插件配置

`plugin.toml` 是插件的核心配置文件,包含:
- 插件元数据 (名称、版本、描述)
- SDK 版本兼容性
- 运行时配置
- 自定义配置项

### 插件类

所有插件必须:
1. 继承 `NekoPluginBase`
2. 使用 `@neko_plugin` 装饰器
3. 实现 `__init__(self, ctx)` 构造函数

### 入口点

使用 `@plugin_entry` 装饰器定义可被外部调用的方法:
```python
@plugin_entry
async def my_function(self, input_data):
    return {"result": "success"}
```

---

## 🔧 开发工具

### 日志记录

```python
# 启用文件日志
self.file_logger = self.enable_file_logging(log_level="INFO")
self.logger = self.file_logger

# 记录日志
self.logger.info("Info message")
self.logger.warning("Warning message")
self.logger.error("Error message")
```

### 配置管理

```python
# 读取配置
value = await self.config.get("my_setting")

# 更新配置
await self.config.set("my_setting", "new_value")

# 获取完整配置
config = await self.config.get_all()
```

### 消息推送

```python
# 推送消息到消息队列
self.ctx.push_message(
    source="my_plugin",
    message_type="info",
    description="Something happened",
    priority=5,
    content="Detailed information"
)
```

---

## 🎯 示例插件

查看 `plugin/plugins/` 目录下的示例插件:
- `testPlugin`: 功能完整的测试插件
- `load_tester`: 性能测试插件

---

## 📝 相关文档

- [端点文档](../endpoint/) - HTTP API 参考
- [Message Plane](../message_plane/) - 消息总线文档
- [SDK 源码](../../sdk/) - SDK 实现代码

---

## 🤝 获取帮助

- 查看示例插件代码
- 阅读 SDK 源码注释
- 参考端点文档了解服务器 API

---

**文档版本**: v1.0  
**最后更新**: 2026-01-26  
**维护者**: N.E.K.O Team
