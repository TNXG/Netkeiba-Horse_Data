# coding=utf-8
import time
import json

from flask import Flask, request

from core.getdata.index import gethorsedata

app = Flask(__name__)


# 设置响应头
@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["content-type"] = "application/json;charset=utf-8"
    response.headers["source"] = "Preliminary Rodesisland Terminal System(PRTS)"
    return response


# 设置全局404返回信息
@app.errorhandler(404)
def err404(exc):
    data = {"code": "404", "msg": "404 Not found", "time": str(int(time.time()))}
    return json.dumps(data, ensure_ascii=False)


@app.route("/")
def root():
    data = {"code": "200", "msg": "Welcome to Netkeiba Horse Data", "time": str(int(time.time()))}
    return json.dumps(data, ensure_ascii=False)


@app.route("/get/")
# 获取id的数据
def netkeiba_getdata():
    ids = request.args.get('id')
    if ids is None:
        data = {"code": "403", "msg": "Missing required parameter id", "time": str(int(time.time()))}
        return json.dumps(data, ensure_ascii=False)
    if not ids.isdigit():
        data = {"code": "403", "msg": "id is required and must be a number", "time": str(int(time.time()))}
        return json.dumps(data, ensure_ascii=False)
    return gethorsedata(ids)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
