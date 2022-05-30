# coding:utf-8
import pytest
from common import ddt
import os.path
import requests
from common import fz, readexcel
import allure

curpath = os.path.dirname(os.path.realpath(__file__))

testxlsx = os.path.join(curpath, "testcase.xlsx")



report_path = os.path.join(os.path.dirname(curpath), "report")
reportxlsx = os.path.join(report_path, "result.xlsx")


testdata = readexcel.ExcelUtil(testxlsx).dict_data()
print(testdata)
@pytest.mark.parametrize('data',testdata)

class Test_api:

    @allure.story("扬州接口")
    def test_api(self,data):
        res = fz.send_requests(data)
        # 检查点 checkpoint
        check = data["checkpoint"]
        res_text = res["text"]
        assert check in res_text

if __name__ == "__main__":
    pytest.main()