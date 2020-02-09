
from okex import utils
from okex.swap_api import SwapAPI
from trade.stock.trade_strategy_base import TradeStrategyBase
import logging
import okex.consts as c
from apscheduler.schedulers.blocking import BlockingScheduler

log = logging.getLogger('mydjango')


class TradeStrategySimple(TradeStrategyBase):
    """
        交易策略1:
        挂单买卖20档

    """

    def __init__(self):
        self.__mark_price = 0
        self.__offset = 100
        self.__sw = SwapAPI(c.api_key, c.secret_key, c.passphrase)

        # 该示例代码生成了一个BlockingScheduler调度器，使用了默认的任务存储MemoryJobStore，以及默认的执行器ThreadPoolExecutor，并且最大线程数为10。

        # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
        scheduler = BlockingScheduler()
        # 采用阻塞的方式

        # 采用固定时间间隔（interval）的方式，每隔5秒钟执行一次
        scheduler.add_job(self.__job, 'interval', seconds=5)

        scheduler.start()
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

    def __job(self) -> None:
        """
        清理订单 大于多仓当前价格的订单 小于空仓当前价格的订单
        :return:
        """

        data = self.__sw.get_order_list(6, c.BTC_USDT_SWAP)
        if 'order_info' in data and data['order_info']:
            ids = []
            for d in data['order_info']:
                price = float(d['price'])
                t = int(d['type'])
                if self.__mark_price == 0 or (t == 1 or t == 4) and int(price) > self.__mark_price:
                    ids.append(d['order_id'])
                elif self.__mark_price == 0 or (t == 2 or t == 3) and int(price) < self.__mark_price:
                    ids.append(d['order_id'])

                if len(ids) >= 10:
                    res = self.__sw.revoke_orders(ids=ids, instrument_id=c.BTC_USDT_SWAP)
                    log.info("取消订单{}".format(res))
                    ids = []

            if ids:
                res = self.__sw.revoke_orders(ids=ids, instrument_id=c.BTC_USDT_SWAP)
                log.info("取消订单{}".format(res))
