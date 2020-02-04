from django.http.response import JsonResponse

from trade.http import http_data
from trade.stock.stock_trade_orders import StockTradeOrders
from trade.stock.trade_loop_back import TradeLoopBack
from trade.stock.trade_strategy_simple import TradeStrategySimple


def index(request):
    data = {'msg': 'success'}
    return JsonResponse(data)


def start(request):
    http_data.HttpData()
    data = http_data.HttpData.trades()
    trade_days = StockTradeOrders(data)
    print(trade_days)

    trade_loop_back = TradeLoopBack(trade_days, TradeStrategySimple())
    trade_loop_back.execute_trade()

    data = {'msg': 'success'}
    return JsonResponse(data)
