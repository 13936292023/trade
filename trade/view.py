import logging

from django.http.response import JsonResponse

from binance_f import RequestClient
from binance_f.base.printobject import PrintBasic
from trade.http.net1 import SocketThread

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
    try:
        request_client = RequestClient(api_key='vmPUZE6mv9SD5VNHk4HlWFsOr6aKE2zvsw0MuIgwCIPy6utIco14y7Ju91duEh8A', secret_key='NhqPtmdSJYdKjVHjA7PZj4Mge3R5YNiP1e3UZjInClVN65XAbvqqM6A7H5fATj0j')
        result = request_client.cancel_all_orders(symbol="BTCUSDT")
        PrintBasic.print_obj(result)
    except Exception as e:
        log.error(e)
    return JsonResponse({'msg': 'success'})
