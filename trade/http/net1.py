import ssl
import sys
import threading
import zlib

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


def inflate(data):
    decompress = zlib.decompressobj(
        -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated


def on_message(ws, data):
    obj = json.loads(inflate(data))
    if obj['table'] == 'swap/trade':
        for a in obj['data']:
            price = float(a['price'])
            ts.buy_strategy(int(price))
            ts.sell_strategy()


def on_error(ws, data):
    logging.error(data)


def on_close():
    log.info("### closed ###")


def on_open(ws):
    log.info("### open ###")
    ws.send(
        "{\"op\": \"subscribe\", \"args\": [\"swap/mark_price:BTC-USDT-SWAP\", \"swap/trade:BTC-USDT-SWAP\"]}")


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
