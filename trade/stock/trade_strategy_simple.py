import numpy

from trade.stock.trade_strategy_base import TradeStrategyBase
import logging

log = logging.getLogger('mydjango')


class TradeStrategySimple(TradeStrategyBase):
    """
        交易策略1:
        挂单买卖20档

    """

    def __init__(self):
        # 平仓数量
        self.__close_position = 20
        # 当前价格
        self.__curr_price = 0
        # 多仓 空仓 数量
        self.__more_price = numpy.empty([0, 0])
        self.__empty_price = numpy.empty([0, 0])
        # 购买单位数量
        self.__unit_count = 0.01
        self.__profit = 0

    def buy_strategy(self, int_curr_price):
        """
            购买策略
                初始价格 买卖20张挂单
        :param int_curr_price:
        :return:
        """
        if self.__curr_price == 0:
            log.info("初始交易价格")
        elif int_curr_price >= self.__curr_price + 1:
            self.__empty_price = numpy.append(self.__empty_price,
                                              [a for a in range(self.__curr_price, int_curr_price, )])
            log.info("{}->{}卖出空仓+{},当前空仓持有{},盈亏{}".format(self.__curr_price, int_curr_price, self.__unit_count,
                                                          len(self.__empty_price),
                                                          self.__calculation_profit(self.__curr_price,
                                                                                    self.__empty_price.mean(),
                                                                                    len(self.__empty_price))))
        elif int_curr_price <= self.__curr_price - 1:
            self.__more_price = numpy.append(self.__more_price,
                                             [a for a in range(int_curr_price + 1, self.__curr_price + 1)])
            log.info("{}->{}买入多仓+{},当前多仓持有{},盈亏{}".format(self.__curr_price, int_curr_price, self.__unit_count,
                                                          len(self.__more_price),
                                                          self.__calculation_profit(self.__more_price.mean(),
                                                                                    self.__curr_price,
                                                                                    len(self.__more_price))))

        self.__curr_price = int_curr_price

    def sell_strategy(self):
        if len(self.__more_price) >= self.__close_position:
            profit = self.__calculation_profit(self.__more_price.mean(), self.__curr_price,
                                               len(self.__more_price))
            if profit > 1:
                self.__profit += profit
                self.__more_price = numpy.empty([0, 0])
                log.info("平仓多仓{},价格{},实现盈亏{}".format(self.__more_price, self.__curr_price, self.__profit))

        if len(self.__empty_price) >= self.__close_position:
            profit = self.__calculation_profit(self.__curr_price, self.__empty_price.mean(),
                                               len(self.__empty_price))
            if profit > 1:
                self.__profit += profit
                self.__empty_price = numpy.empty([0, 0])
                log.info("平仓空仓{},价格{},实现盈亏{}".format(self.__empty_price, self.__curr_price, self.__profit))

    def __calculation_profit(self, sell, buy, count):
        """
           # （卖价 - 买价） * 订单数量 * 每单数量
        """
        return (sell - buy) * count * self.__unit_count

    def __str__(self):
        a = self.__calculation_profit(self.__curr_price, self.__more_price.mean(), len(self.__more_price))
        b = self.__calculation_profit(self.__empty_price.mean(), self.__curr_price, len(self.__empty_price))
        return "当前价格={} 已经实现盈亏:{} 多仓：,持有数量={},盈亏{}。空仓：,持有数量={},盈亏{}".format(self.__curr_price,
                                                                            self.__profit,
                                                                            len(self.__more_price),
                                                                            a,
                                                                            len(self.__empty_price),
                                                                            b, )
