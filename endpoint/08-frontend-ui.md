# 前端UI端点

> 前端UI端点提供管理界面的访问和静态资源服务

---

## 概述

前端UI端点用于访问 Web 管理界面:
- SPA 应用入口
- 静态资源服务(JS、CSS、图片等)
- History API fallback 支持

所有端点都无需认证。

---

## 1. 前端首页端点

### 8.1 前端首页端点

#### `GET /ui`
#### `GET /ui/`

**功能**: 返回前端管理界面的首页

**认证要求**: 无

**响应**: HTML 页面 (index.html)

**响应头**:
- `Cache-Control`: `no-store, no-cache, must-revalidate, max-age=0`
- `Pragma`: `no-cache`
- `Expires`: `0`

**实现细节**:
- 返回 `frontend/exported/index.html`
- 禁用缓存,确保总是获取最新版本
- 文件不存在时返回 404

**使用场景**:
- 访问管理界面
- SPA 应用入口

**代码位置**: `user_plugin_server.py:594-611`

---

### 8.2 前端静态资源端点

#### `StaticFiles /ui/assets`

**功能**: 提供前端静态资源 (JS, CSS, 图片等)

**认证要求**: 无

**缓存策略**:
- `Cache-Control`: `public, max-age=31536000, immutable`
- 长期缓存,提高加载性能

**实现细节**:
- 使用 FastAPI 的 `StaticFiles` 挂载
- 资源路径: `frontend/exported/assets/`
- 自动处理 MIME 类型

**使用场景**:
- 加载前端 JS/CSS 文件
- 加载图片和字体资源

**代码位置**: `user_plugin_server.py:234-238, 246-248`

---

### 8.3 前端 SPA 路由端点

#### `GET /ui/{full_path:path}`

**功能**: 处理前端 SPA 的所有路由 (History API fallback)

**路径参数**:
- `full_path`: 任意路径

**认证要求**: 无

**实现细节**:
- 如果路径对应的文件存在,返回该文件
- 如果文件不存在,返回 `index.html` (SPA fallback)
- HTML 文件禁用缓存
- 防止路径遍历攻击

**使用场景**:
- 支持前端路由刷新
- SPA 应用路由处理
- 例如: `/ui/plugins/plugin1` 刷新时仍能正常工作

**代码位置**: `user_plugin_server.py:614-653`

---


---

## 总结

前端UI端点共 **3个**,全部无需认证:
- `/ui`, `/ui/`: SPA 应用入口
- `/ui/assets`: 静态资源服务
- `/ui/{path}`: SPA 路由 fallback

提供了完整的 Web 管理界面访问,支持前端路由刷新。访问地址: `http://127.0.0.1:48912/ui`
