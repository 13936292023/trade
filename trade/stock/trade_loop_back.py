class TradeLoopBack(object):
    """
        交易回测系统
    """

    def __init__(self, trade_days, trade_strategy):
        """
        使用前面封装的StockTradeDays类和本节编写的交易策略类
        TradeStrategyBase类初始化交易系统
        :param trade_days: StockTradeDays交易数据序列
        :param trade_strategy: TradeStrategyBase交易策略
        """
        self.trade_days = trade_days
        self.trade_strategy = trade_strategy
        # 交易盈亏结果序列
        self.profit_array = []

    def execute_trade(self):
        """
        执行交易回测
        :return:
        """
        for ind, day in enumerate(self.trade_days):
            """
            以时间驱动，完成交易回测
            """
            # if self.trade_strategy.keep_stock_day > 0:
            #     # 如果有持有股票，加入交易盈亏结果序列
            #     self.profit_array.append(day.change)
            # hasattr: 用来查询对象有没有实现某个方法
            if hasattr(self.trade_strategy, 'buy_strategy'):
                # 买入策略执行
                self.trade_strategy.buy_strategy(ind, day, self.trade_days)

            if hasattr(self.trade_strategy, 'sell_strategy'):
                # 卖出策略执行
                self.trade_strategy.sell_strategy(ind, day, self.trade_days)

        print(self.trade_strategy)
