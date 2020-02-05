import http.client
import ssl
import json
import logging

log = logging.getLogger('mydjango')
context = ssl._create_default_https_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
BASE_URL = "testnet.binancefuture.com"
GET = "GET"
PING_URL = "/fapi/v1/ping"
STATUS_OK = 200
EX_CHANG_INFO_URL = "/fapi/v1/exchangeInfo"
DEPTH_URL = "/fapi/v1/depth"


class HttpData:
    @staticmethod
    def __get_data(url):
        conn = http.client.HTTPSConnection(BASE_URL, context=context)
        conn.request(GET, url)
        response = conn.getresponse()
        return json.loads(response.read())

    @staticmethod
    def ping_server():
        conn = http.client.HTTPSConnection(BASE_URL, context=context)
        conn.request(GET, PING_URL)
        response = conn.getresponse()
        if response.status != STATUS_OK:
            raise Exception("http request error")

    @staticmethod
    def ex_change_info():
        """
        获取交易规则和交易对
        :return:
        """
        return HttpData.__get_data(EX_CHANG_INFO_URL)

    @staticmethod
    def depth():
        """
        获取交易深度
        :return:
        """
        return HttpData.__get_data(DEPTH_URL + "?symbol=BTCUSDT&limit=100")

    @staticmethod
    def trades():
        return HttpData.__get_data("/fapi/v1/trades?symbol=BTCUSDT&limit=100")
