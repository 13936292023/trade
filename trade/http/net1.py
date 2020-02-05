import ssl
import sys
import threading

import websocket
import logging
import json

from trade.stock.trade_strategy_simple import TradeStrategySimple

log = logging.getLogger('mydjango')
"""

    apiKey 57b9858d-f489-41a0-91b9-b926742b30be
    secretKey 61792E270589F5ACEE74259EE584FFA6

"""

ts = TradeStrategySimple()


def on_message(ws, data):
    obj = json.loads(data)
    if obj['e'] == 'aggTrade':
        price = float(obj['p'])
        ts.buy_strategy(int(price))
        ts.sell_strategy()


def on_error(ws, data):
    logging.error(data)


def on_close():
    log.info("### closed ###")


def on_open(ws):
    log.info("### open ###")
    ws.send(
        "{\"method\": \"SUBSCRIBE\",\"params\":"
        "[\"btcusdt@aggTrade\"]"
        ",\"id\": 1}")


class SocketThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        websocket.enableTrace(True)
        websocket.WebSocketApp("wss://stream.binancefuture.com/ws/btcusdt@aggTrade",
                               None,
                               on_open,
                               on_message,
                               on_error) \
            .run_forever(sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
