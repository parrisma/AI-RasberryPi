from abc import ABC, abstractclassmethod, abstractmethod
from typing import Tuple
from collections.abc import Iterable
from AIIntuition.journeys.journey5.policy import Policy


class Case(ABC):
    @classmethod
    @abstractmethod
    def set_up(cls,
               num_hosts: int,
               num_apps: int) -> Tuple[Policy, Iterable]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :param num_hosts: The number of Hosts to create in the environment
        :param num_apps:  The number of App to create in the environment.
        :return: The Host Selection Policy used by the scheduler, The Host iterator used by the scheduler
        """
        raise NotImplementedError
