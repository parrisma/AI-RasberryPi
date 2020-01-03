from abc import ABC, abstractclassmethod, abstractmethod
from typing import Tuple
from collections.abc import Iterable
from AIIntuition.journeys.journey5.policy import Policy


class Case(ABC):
    @classmethod
    @abstractmethod
    def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :return:
            The number of hosts created
            The number of applications created
            The Host Selection Policy used by the scheduler
            The Host iterator used by the scheduler
            The number of 24 hour periods to run the schedule simulation for
        """
        raise NotImplementedError
