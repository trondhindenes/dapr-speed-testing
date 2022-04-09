import httpx
from loguru import logger

_httpx_client = None


async def _doit(call, *args, **kwargs):
    global _httpx_client
    if not _httpx_client:
        logger.info("initializing http client")
        _httpx_client = await httpx.AsyncClient().__aenter__()
    if call == "get":
        return await _httpx_client.get(*args, **kwargs)
    elif call == "post":
        return await _httpx_client.post(*args, **kwargs)
    elif call == "patch":
        return await _httpx_client.patch(*args, **kwargs)
    elif call == "delete":
        return await _httpx_client.delete(*args, **kwargs)
    else:
        raise ValueError("method not supported")


async def http_get(*args, **kwargs):
    return await _doit("get", *args, **kwargs)


async def http_post(*args, **kwargs):
    return await _doit("post", *args, **kwargs)


async def http_patch(*args, **kwargs):
    return await _doit("patch", *args, **kwargs)


async def http_delete(*args, **kwargs):
    return await _doit("delete", *args, **kwargs)
