import ssl
import sys

import websocket
import logging
import json

from trade.stock.trade_strategy_simple import TradeStrategySimple

"""

    apiKey 57b9858d-f489-41a0-91b9-b926742b30be
    secretKey 61792E270589F5ACEE74259EE584FFA6

"""
log = logging.Logger("auto.net")
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

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


websocket.enableTrace(True)
websocket.WebSocketApp("wss://stream.binancefuture.com/ws/btcusdt@markPrice",
                       None,
                       on_open,
                       on_message,
                       on_error) \
    .run_forever(sslopt={"check_hostname": False, "cert_reqs": ssl.CERT_NONE})
