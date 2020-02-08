import logging
import time

from django.http.response import JsonResponse

from binance_f import RequestClient
from binance_f.base.printobject import PrintBasic
from okex import utils
from okex.swap_api import SwapAPI
from trade.http import net
from trade.http.net import SocketThread

log = logging.getLogger('mydjango')


def index(request):
    data = {'msg': 'success'}
    log.info(data)
    return JsonResponse(data)


def start(request):
    SocketThread().start()
    data = {'msg': 'success'}
    return JsonResponse(data)


def cancel(request):
    data = sw.get_order_list('0', c.BTC_USDT_SWAP)
    if 'order_info' in data and data['order_info']:
        result = sw.revoke_orders(ids=[o['order_id'] for o in data['order_info']], instrument_id=c.BTC_USDT_SWAP)
        return JsonResponse({'data': data, 'result': result})
    return JsonResponse(data)


import okex.consts as c

sw = SwapAPI(c.api_key, c.secret_key, c.passphrase)


def t(request):
    data = [
        {
            'holding': [
                {
                    'avail_position': '0',
                    'avg_cost': '9817.0',
                    'last': '9841.2',
                    'leverage': '100.00',
                    'liquidation_price': '0.0',
                    'maint_margin_ratio': '0.0050',
                    'margin': '0.00',
                    'position': '1',
                    'realized_pnl': '0.00',
                    'settled_pnl': '0.00',
                    'settlement_price': '9817.0',
                    'side': 'short',
                    'timestamp': '2020-02-08T14:09:00.557Z'
                }
            ],
            'instrument_id': 'BTC-USDT-SWAP',
            'margin_mode': 'crossed',
            'timestamp': '2020-02-08T14:09:00.557Z'
        }
    ]
    return JsonResponse(sw.get_order_list('0', c.BTC_USDT_SWAP))
