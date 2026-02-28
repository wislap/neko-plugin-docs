# API 客户端插件

演示异步 HTTP 客户端、批量并发请求。

## __init__.py

```python
import asyncio
from typing import Optional, Dict
import aiohttp
from plugin.sdk import (
    NekoPluginBase, neko_plugin, plugin_entry, lifecycle, ok, fail,
)


@neko_plugin
class APIClientPlugin(NekoPluginBase):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url = "https://api.example.com"

    @lifecycle(id="startup")
    async def startup(self, **_):
        self.session = aiohttp.ClientSession()

    @lifecycle(id="shutdown")
    async def shutdown(self, **_):
        if self.session:
            await self.session.close()

    @plugin_entry()
    async def fetch(self, endpoint: str, method: str = "GET", params: Optional[Dict] = None, **_):
        if not self.session:
            return fail(message="Session not initialized")

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        self.report_status({"status": "fetching", "url": url})

        try:
            async with self.session.request(method, url, params=params) as resp:
                if resp.status >= 400:
                    return fail(message=f"HTTP {resp.status}", code=resp.status)
                data = await resp.json()
                return ok(data={"status": resp.status, "data": data})
        except aiohttp.ClientError as e:
            return fail(message=str(e))

    @plugin_entry()
    async def batch_fetch(self, endpoints: list, concurrent: int = 3, **_):
        semaphore = asyncio.Semaphore(concurrent)

        async def fetch_one(ep: str):
            async with semaphore:
                return await self.fetch(endpoint=ep)

        tasks = [fetch_one(ep) for ep in endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        success = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
        return ok(data={
            "total": len(endpoints),
            "success": success,
            "failed": len(endpoints) - success,
        })
```
