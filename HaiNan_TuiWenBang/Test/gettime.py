import time
import requests


def getBeijinTime():
    try:
        # 设置头信息，没有访问会错误400！！！
        hea = {'User-Agent': 'Mozilla/5.0'}
        # 设置访问地址，我们分析到的；
        url = r'http://time1909.beijing-time.org/time.asp'
        # 用requests get这个地址，带头信息的；
        r = requests.get(url=url, headers=hea)
        # 检查返回的通讯代码，200是正确返回；
        if r.status_code == 200:
            # 定义result变量存放返回的信息源码；
            result = r.text

            data = result.split(";")
            # ======================================================
            # 以下是数据文本处理：切割、取长度，最最基础的东西就不描述了；
            year = data[1][len("nyear") + 3: len(data[1])]
            month = data[2][len("nmonth") + 3: len(data[2])]
            day = data[3][len("nday") + 3: len(data[3])]
            print(year,month,day)
    except:
        return (-1)

