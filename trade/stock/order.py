import hashlib
import logging
import time
import uuid

from okex.swap_api import SwapAPI
import okex.consts as c

swapApi = SwapAPI(c.api_key, c.secret_key, c.passphrase)
log = logging.getLogger('mydjango')


def create_order(long, short):
    """
    [{"order_type":"0","client_oid": "E213","price": "5","size": "2","type": "1","match_price": "0"},
    {"order_type":"0","client_oid": "243","price": "2","size": "3","type": "2","match_price": "1"}]
    :param long:
    :param short:
    :return:
    """
    order_data = []
    for a in long:
        order_data.append(
            {"order_type": "1", "client_oid": create_id(), "price": a, "size": "1", "type": "1",
             "match_price": "0"}
        )
    for a in short:
        order_data.append(
            {"order_type": "1", "client_oid": create_id(), "price": a, "size": "1", "type": "2",
             "match_price": "0"}
        )
    if len(order_data) > 0:
        data = swapApi.take_orders(order_data, 'BTC-USDT-SWAP')
        log.info("+order {} response info :{}".format(order_data, data))


def create_id():
    m = hashlib.md5(str(time.perf_counter()).encode('utf-8'))
    return m.hexdigest()
