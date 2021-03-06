import six
from abc import ABCMeta, abstractmethod


class TradeStrategyBase(six.with_metaclass(ABCMeta, object)):
    """
        交易策略抽象基类
    """

    @abstractmethod
    def buy_strategy(self, *args, **kwargs):
        # 买入策略基类
        pass

    @abstractmethod
    def sell_strategy(self, *args, **kwargs):
        # 卖出策略基类
        pass
