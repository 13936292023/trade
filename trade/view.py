import logging

from django.http.response import JsonResponse

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
