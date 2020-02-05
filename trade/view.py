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
        request_client = RequestClient(api_key='yZvYkAzGDiO5NEe4UKfdbHe5vkuenVpCPk7ycTqOeFwZ4vyWk1KJ3JRK0cAHHYLt', secret_key='Ysr9zzHkgbHDeqJ1xHQYWxwenzfaF5hw2haLklIKepIF6CvH5vqY69TXC3v4ZpiH')
        result = request_client.cancel_all_orders(symbol="BTCUSDT")
        PrintBasic.print_obj(result)
    except Exception as e:
        log.error(e)
    return JsonResponse({'msg': 'success'})
