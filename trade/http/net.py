import ssl
import threading
import time
import websocket
import logging
import json

from okex import utils, consts as c
from okex.swap_api import SwapAPI
from trade.stock import order
from trade.stock.trade_strategy_simple import TradeStrategySimple

log = logging.getLogger('mydjango')
ts = TradeStrategySimple()
swapApi = SwapAPI(c.api_key, c.secret_key, c.passphrase)


def on_message(ws, data):
    obj = json.loads(utils.inflate_data(data))
    if 'table' in obj:
        if obj['table'] == 'swap/trade':
            for a in obj['data']:
                price = float(a['price'])
                long, short = ts.buy_strategy(int(price))
                log.info("mark:{},long : {},short:{}".format(price, long, short))
                order.create_order(long, short)
        elif obj['table'] == 'swap/position':
            log.info(obj)
            ts.sell_strategy(obj['data'])
    elif 'event' in obj:
        if obj['event'] == 'login' and obj['success'] is True:
            ws.send(
                "{\"op\": \"subscribe\", \"args\": [\"swap/mark_price:BTC-USDT-SWAP\", "
                "\"swap/trade:BTC-USDT-SWAP\",\"swap/position:BTC-USDT-SWAP\",\"swap/order:BTC-USDT-SWAP\"]}")


def on_error(ws, data):
    logging.error(data)


def on_close():
    log.info("### closed ###")


def on_open(ws):
    log.info("### open ###")
    t = int(time.time())
    s = utils.signature(t, 'GET', '/users/self/verify', '', c.secret_key)
    log.info("sign={}".format(s))
    ws.send(
        "{\"op\":\"login\",\"args\":[\"79c60697-6c2d-487d-9694-220dcbfd9e61\",\"zhangsong110\",\"" + str(t) +
        "\",\"" + str(s, encoding='utf-8') + "\"]}")


class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        websocket.enableTrace(True)
        websocket.WebSocketApp("ws://47.56.128.21:38043/ws/v3",
                               None,
                               on_open,
                               on_message,
                               on_error) \
            .run_forever(sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
