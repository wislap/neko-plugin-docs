# 响应格式

N.E.K.O 插件系统使用统一的响应格式。SDK 提供 `ok()` 和 `fail()` 辅助函数。

## ok() — 成功响应

```python
from plugin.sdk import ok

# 基本用法
return ok(data={"message": "Hello!"})

# 带消息
return ok(data={"count": 42}, message="处理完成")
```

返回格式：

```json
{
  "success": true,
  "code": 0,
  "data": {"message": "Hello!"},
  "message": "",
  "error": null,
  "time": "2024-01-01T00:00:00Z"
}
```

## fail() — 失败响应

```python
from plugin.sdk import fail

# 基本用法
return fail(message="参数无效")

# 指定错误码
return fail(message="未找到", code=404)

# 带数据
return fail(message="验证失败", code=400, data={"field": "name"})
```

返回格式：

```json
{
  "success": false,
  "code": 400,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "参数无效"
  },
  "time": "2024-01-01T00:00:00Z"
}
```

## 直接返回字典

插件入口也可以直接返回字典，系统会自动用 `ok()` 包装：

```python
@plugin_entry()
def greet(self, name: str = "World"):
    return {"message": f"Hello, {name}!"}
    # 自动变成 ok(data={"message": "Hello, World!"})
```

## ErrorCode

`ErrorCode` 是与 HTTP 状态码对齐的整数枚举：

```python
from plugin.sdk import ErrorCode
```

| 常量 | 值 | 说明 |
|------|-----|------|
| `SUCCESS` | `0` | 成功 |
| `BAD_REQUEST` | `400` | 请求无效 |
| `UNAUTHORIZED` | `401` | 未授权 |
| `FORBIDDEN` | `403` | 禁止访问 |
| `NOT_FOUND` | `404` | 未找到 |
| `TIMEOUT` | `408` | 超时 |
| `CONFLICT` | `409` | 冲突 |
| `VALIDATION_ERROR` | `422` | 验证错误 |
| `EXECUTION_ERROR` | `500` | 执行错误 |
| `NOT_IMPLEMENTED` | `501` | 未实现 |
| `SERVICE_UNAVAILABLE` | `503` | 服务不可用 |

## Result 类型（函数式风格）

SDK 也提供了 `Ok` / `Err` 用于函数式错误处理：

```python
from plugin._types import Ok, Err, Result

async def fetch_user(id: int) -> Result:
    if id <= 0:
        return Err(ValueError("invalid id"))
    return Ok({"id": id, "name": "Alice"})

# 使用 match/case (Python 3.10+)
match await fetch_user(1):
    case Ok(user):
        print(user["name"])
    case Err(e):
        print(f"Error: {e}")
```

:::{note}
`ok()` / `fail()` 返回字典（用于插件入口点响应）；`Ok` / `Err` 返回对象（用于内部函数式错误处理）。两者用途不同。
:::
