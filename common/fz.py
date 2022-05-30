# coding:utf-8
import json
import os
import requests

from common.readexcel import ExcelUtil


def send_requests(testdata):
    '''封装requests请求'''
    method = testdata["method"]
    url = testdata["url"]
    # url后面的params参数

    # 请求头部headers
    try:
        headers = eval(testdata["headers"])
        print("请求头部：%s" % headers)
    except:
        headers = None
    # post请求body类型


    test_nub = testdata['id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))



    try:
        bodydata = eval(testdata["body"])
        print(bodydata)
    except:
        bodydata = {}


    res = {}   # 接受返回数据


    r = requests.request(method=method,url=url,data=json.dumps(bodydata),headers=headers)
    print("页面返回信息：%s" % r.content.decode("utf-8"))
    res['id'] = testdata['id']
    res['rowNum'] = testdata['rowNum']

    res["statuscode"] = str(r.status_code)  # 状态码转成str
    res["text"] = r.content.decode("utf-8")
    res["times"] = str(r.elapsed.total_seconds())
    print(res["times"])
    # 接口请求时间转str
    if res["statuscode"] != "200":
        res["error"] = res["text"]
        print(res["text"])
    else:
        res["error"] = ""
    res["msg"] = ""
    if testdata["checkpoint"] in res["text"]:
        res["result"] = "pass"
        print("用例测试结果:   %s---->%s" % (test_nub, res["result"])+'\n\n')
    else:
        res["result"] = "fail"
    return res




if __name__ == "__main__":
    data = ExcelUtil("testcase.xlsx").dict_data()
    s = requests.session()
    res = send_requests(data[0])

