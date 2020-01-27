from abc import ABC, abstractmethod
from AIIntuition.journeys.journey5.systemtime import SystemTime


class JException(Exception):
    @abstractmethod
    def as_string(self,
                  sys_time: SystemTime,
                  as_feature: bool = False) -> str:
        """
        The exception rendered as string, if as_feature = True then as a feature vector equivalent for use in AL/ML
        context.
        :param sys_time: System time at while event occurred
        :param as_feature: If true render as feature vector.
        :return: Exception as string
        """
        raise NotImplementedError
