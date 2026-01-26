# 配置管理端点

> 配置管理端点提供完整的插件配置 CRUD 操作,支持基础配置、Profile 配置、TOML 格式转换等

---

## 概述

配置管理端点提供了强大的配置管理功能:
- 基础配置的读取和更新
- Profile 配置管理(多环境配置)
- TOML 格式与配置对象的相互转换
- 配置安全验证(禁止修改关键字段)

所有端点都需要管理员认证。

---

## 1. 获取插件配置端点

> 配置管理端点提供了完整的插件配置 CRUD 操作,支持基础配置、Profile 配置、TOML 格式转换等

### 6.1 获取插件配置端点

#### `GET /plugin/{plugin_id}/config`

**功能**: 获取插件的完整配置 (包括 base + active profile 叠加后的结果)

**路径参数**:
- `plugin_id`: 插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin": {
    "id": "plugin1",
    "name": "示例插件",
    "version": "1.0.0",
    "entry": "main.py",
    "description": "这是一个示例插件"
  },
  "config": {
    "key1": "value1"
  }
}
```

**实现细节**:
- 调用 `load_plugin_config()` 加载配置
- 返回 base 配置与 active profile 合并后的结果

**使用场景**:
- 获取插件当前生效的配置
- 配置编辑器数据源

**代码位置**: `user_plugin_server.py:928-944`

---

### 6.2 获取插件配置 TOML 原文端点

#### `GET /plugin/{plugin_id}/config/toml`

**功能**: 获取插件配置的 TOML 原文

**路径参数**:
- `plugin_id`: 插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "toml": "[plugin]\nid = \"plugin1\"\nname = \"示例插件\"\n..."
}
```

**实现细节**:
- 调用 `load_plugin_config_toml()` 读取 TOML 文件
- 返回原始 TOML 文本

**使用场景**:
- TOML 编辑器数据源
- 配置文件导出

**代码位置**: `user_plugin_server.py:947-964`

---

### 6.3 更新插件配置端点

#### `PUT /plugin/{plugin_id}/config`

**功能**: 更新插件配置 (完全替换)

**路径参数**:
- `plugin_id`: 插件ID

**请求体**:
```json
{
  "config": {
    "plugin": {
      "name": "新名称",
      "description": "新描述"
    },
    "config": {
      "key1": "new_value"
    }
  }
}
```

**认证要求**: **需要管理员验证码** (Bearer Token)

**安全限制**:
- **禁止修改** `plugin.id` (插件ID)
- **禁止修改** `plugin.entry` (入口点)
- 验证字段类型和格式
- 防止注入攻击

**响应格式**:
```json
{
  "success": true,
  "message": "Configuration updated successfully"
}
```

**实现细节**:
- 调用 `validate_config_updates()` 验证安全性
- 调用 `replace_plugin_config()` 执行更新
- 递归检查嵌套字典中的禁止字段

**错误处理**:
- 400: 尝试修改禁止字段或格式错误
- 500: 更新失败

**使用场景**:
- 配置编辑器保存
- 批量配置更新

**代码位置**: `user_plugin_server.py:1198-1220`

---

### 6.4 解析 TOML 为配置对象端点

#### `POST /plugin/{plugin_id}/config/parse_toml`

**功能**: 解析 TOML 文本为配置对象 (不落盘,仅用于预览)

**路径参数**:
- `plugin_id`: 插件ID

**请求体**:
```json
{
  "toml": "[plugin]\nid = \"plugin1\"\n..."
}
```

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "config": {
    "plugin": {
      "id": "plugin1"
    }
  }
}
```

**实现细节**:
- 调用 `parse_toml_to_config()` 解析 TOML
- 不写入文件系统
- 用于实时预览

**使用场景**:
- TOML 编辑器实时预览
- 配置验证

**代码位置**: `user_plugin_server.py:1223-1241`

---

### 6.5 渲染配置对象为 TOML 端点

#### `POST /plugin/{plugin_id}/config/render_toml`

**功能**: 将配置对象渲染为 TOML 文本 (不落盘,仅用于预览)

**路径参数**:
- `plugin_id`: 插件ID

**请求体**:
```json
{
  "config": {
    "plugin": {
      "id": "plugin1",
      "name": "示例插件"
    }
  }
}
```

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "toml": "[plugin]\nid = \"plugin1\"\nname = \"示例插件\"\n"
}
```

**实现细节**:
- 调用 `render_config_to_toml()` 渲染 TOML
- 不写入文件系统
- 用于实时预览

**使用场景**:
- 配置编辑器切换视图
- TOML 格式预览

**代码位置**: `user_plugin_server.py:1244-1262`

---

### 6.6 更新插件配置 TOML 端点

#### `PUT /plugin/{plugin_id}/config/toml`

**功能**: 使用 TOML 原文覆盖更新插件配置

**路径参数**:
- `plugin_id`: 插件ID

**请求体**:
```json
{
  "toml": "[plugin]\nid = \"plugin1\"\nname = \"新名称\"\n..."
}
```

**认证要求**: **需要管理员验证码** (Bearer Token)

**安全限制**:
- 后端会解析 TOML 并验证
- **禁止修改** `plugin.id` 和 `plugin.entry`

**响应格式**:
```json
{
  "success": true,
  "message": "TOML configuration updated successfully"
}
```

**实现细节**:
- 调用 `update_plugin_config_toml()` 执行更新
- 解析 TOML 后进行安全验证
- 写入 `plugin.toml` 文件

**使用场景**:
- TOML 编辑器保存
- 配置文件导入

**代码位置**: `user_plugin_server.py:1265-1283`

---

### 6.7 获取插件基础配置端点

#### `GET /plugin/{plugin_id}/config/base`

**功能**: 获取插件的基础配置 (仅 plugin.toml,不包含 profile 叠加)

**路径参数**:
- `plugin_id`: 插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "plugin": {
    "id": "plugin1",
    "name": "示例插件",
    "version": "1.0.0"
  }
}
```

**实现细节**:
- 调用 `load_plugin_base_config()` 加载基础配置
- 只读取 `plugin.toml`,不合并 profile

**使用场景**:
- 查看原始配置
- Profile 编辑参考

**代码位置**: `user_plugin_server.py:1286-1304`

---

### 6.8 获取插件 Profiles 状态端点

#### `GET /plugin/{plugin_id}/config/profiles`

**功能**: 获取插件所有 profile 的状态信息

**路径参数**:
- `plugin_id`: 插件ID

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "active": "production",
  "profiles": {
    "production": {
      "exists": true,
      "path": "/path/to/production.toml"
    },
    "development": {
      "exists": true,
      "path": "/path/to/development.toml"
    }
  }
}
```

**字段说明**:
- `active`: 当前激活的 profile 名称
- `profiles`: profile 映射
  - `exists`: 文件是否存在
  - `path`: 文件路径

**实现细节**:
- 调用 `get_plugin_profiles_state()` 获取状态
- 读取 `profiles.toml` 文件
- 检查每个 profile 文件的存在性

**使用场景**:
- Profile 管理界面
- 查看可用的 profile

**代码位置**: `user_plugin_server.py:1307-1325`

---

### 6.9 获取指定 Profile 配置端点

#### `GET /plugin/{plugin_id}/config/profiles/{profile_name}`

**功能**: 获取指定 profile 的配置内容

**路径参数**:
- `plugin_id`: 插件ID
- `profile_name`: profile 名称

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "config": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

**实现细节**:
- 调用 `get_plugin_profile_config()` 读取 profile
- 解析 profile TOML 文件

**使用场景**:
- Profile 编辑器数据源
- 查看 profile 配置

**代码位置**: `user_plugin_server.py:1328-1346`

---

### 6.10 创建/更新 Profile 配置端点

#### `PUT /plugin/{plugin_id}/config/profiles/{profile_name}`

**功能**: 创建或更新指定 profile 的配置

**路径参数**:
- `plugin_id`: 插件ID
- `profile_name`: profile 名称

**请求体**:
```json
{
  "config": {
    "key1": "value1"
  },
  "make_active": true
}
```

**认证要求**: **需要管理员验证码** (Bearer Token)

**安全限制**:
- **禁止在 profile 中定义顶层 `[plugin]` 段**
- Profile 只能包含配置覆盖,不能修改插件元数据

**响应格式**:
```json
{
  "success": true,
  "message": "Profile created/updated successfully",
  "active": true
}
```

**实现细节**:
- 调用 `upsert_plugin_profile_config()` 创建/更新
- 自动维护 `profiles.toml` 文件
- 可选设置为激活 profile

**使用场景**:
- Profile 编辑器保存
- 创建新的配置环境

**代码位置**: `user_plugin_server.py:1349-1378`

---

### 6.11 删除 Profile 配置端点

#### `DELETE /plugin/{plugin_id}/config/profiles/{profile_name}`

**功能**: 删除指定 profile 的配置映射

**路径参数**:
- `plugin_id`: 插件ID
- `profile_name`: profile 名称

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "success": true,
  "message": "Profile deleted successfully"
}
```

**实现细节**:
- 调用 `delete_plugin_profile_config()` 删除映射
- 从 `profiles.toml` 中移除记录
- 不会强制删除 profile 文件本身

**使用场景**:
- Profile 管理
- 清理无用配置

**代码位置**: `user_plugin_server.py:1381-1399`

---

### 6.12 激活 Profile 端点

#### `POST /plugin/{plugin_id}/config/profiles/{profile_name}/activate`

**功能**: 设置指定 profile 为当前激活的 profile

**路径参数**:
- `plugin_id`: 插件ID
- `profile_name`: profile 名称

**认证要求**: **需要管理员验证码** (Bearer Token)

**响应格式**:
```json
{
  "success": true,
  "message": "Profile activated successfully",
  "active": "production"
}
```

**实现细节**:
- 调用 `set_plugin_active_profile()` 设置激活
- 更新 `profiles.toml` 中的 `active` 字段

**使用场景**:
- 切换配置环境
- 部署时切换 profile

**代码位置**: `user_plugin_server.py:1402-1420`

---


---

## 总结

配置管理端点共 **12个**,全部需要管理员认证:
- 基础配置: `/plugin/{id}/config`, `/plugin/{id}/config/toml`, `/plugin/{id}/config/base`
- Profile 管理: `/plugin/{id}/config/profiles`, `/plugin/{id}/config/profiles/{name}`, 等
- TOML 转换: `/plugin/{id}/config/parse_toml`, `/plugin/{id}/config/render_toml`

提供了完整的配置管理功能,支持多环境部署和安全的配置更新。
