# coding=utf-8
import time

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from core.getdata.index import gethorsedata


app = FastAPI(docs_url=None)

# 设置全局的cors返回头


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response


# 设置全局404返回信息
@app.exception_handler(404)
async def err404(request, exc):
    return JSONResponse(
        status_code=404,
        content={"code": "404", "msg": "404 Not found",
                 "time": str(int(time.time()))})


@app.get("/")
async def root():
    return JSONResponse(
        status_code=200,
        content={"code": "200",
                 "msg": "Welcome to Netkeiba Horse Data",
                 "time": str(int(time.time()))})


@app.get("/get/")
# 获取id的数据
async def netkeiba_getdata(request: Request):
    ids = request.query_params.get('id')
    if ids is None:
        return JSONResponse(status_code=403, content={"code": "403", "msg": "Missing required parameter id",
                                                      "time": str(int(time.time()))})
    if ids is None or not ids.isdigit():
        return JSONResponse(
            status_code=403,
            content={"code": "403", "msg": "id is required and must be a number", "time": str(int(time.time()))})
    return Response(content=gethorsedata(ids), media_type="application/json")

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', proxy_headers=True,
                reload=True, forwarded_allow_ips='*')
