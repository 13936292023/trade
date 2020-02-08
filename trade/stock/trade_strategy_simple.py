import hashlib
import time

from okex import utils
from okex.swap_api import SwapAPI
from trade.stock.trade_strategy_base import TradeStrategyBase
import logging
import okex.consts as c

log = logging.getLogger('mydjango')


class TradeStrategySimple(TradeStrategyBase):
    """
        交易策略1:
        挂单买卖20档

    """

    def __init__(self):
        self.__mark_price = 0
        self.__offset = 0
        self.__sw = SwapAPI(c.api_key, c.secret_key, c.passphrase)
        return

    def buy_strategy(self, int_curr_price):
        long, short = [], []
        if self.__mark_price == 0:
            long, short = [b for b in range(int_curr_price - 10 - self.__offset, int_curr_price - self.__offset)], \
                          [b for b in range(int_curr_price + self.__offset, int_curr_price + 10 + self.__offset)]
        elif self.__mark_price > int_curr_price:
            long = [a for a in range(int_curr_price - self.__offset, self.__mark_price - self.__offset)]
        elif self.__mark_price < int_curr_price:
            short = [a for a in range(self.__mark_price + 1 + self.__offset, int_curr_price + 1 + self.__offset)]

        self.__mark_price = int_curr_price

        return long, short

    def sell_strategy(self, data):
        """
        查询用户持仓 盈利数量 是否需要平仓
        :return:
        """
        order = []
        if data:
            for d in data:
                if d['instrument_id'] == c.BTC_USDT_SWAP:
                    for h in d['holding']:
                        la = float(h['last'])
                        ac = float(h['avg_cost'])
                        po = float(h['position']) * 0.0001
                        if h['side'] == 'long':
                            ot, p, i = 3, la + 1, (la - ac) * po
                        else:
                            ot, p, i = 4, la, (ac - la) * po
                        if i >= 0.01:
                            order.append(
                                {"order_type": "1", "client_oid": utils.create_id(), "price": int(p),
                                 "size": h['avail_position'],
                                 "type": ot,
                                 "match_price": "0"})
        if order:
            data = self.__sw.take_orders(order, 'BTC-USDT-SWAP')
            log.info("-order {} response info :{}".format(order, data))
        return
