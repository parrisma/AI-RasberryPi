from random import seed
from copy import deepcopy
import numpy as np

from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.memory import Memory
from AIIntuition.journeys.journey5.compute import Compute


class Host(Compute):
    def __init__(self,
                 data_center: DataCenter):
        """
        Create a new random host according to the defined probability distributions
        Data Center, Type & capacity.
        """
        self._data_center = data_center
        self._id = Compute.gen_compute_id(self)
        self._core = Core(self._data_center.core_p_dist)
        self._memory = Memory(self._core)
        return

    @property
    def data_center(self) -> str:
        return self._data_center.country_mnemonic

    @property
    def name(self) -> str:
        return ''.join((self.data_center, '_', self._id))

    @property
    def id(self) -> str:
        return deepcopy(self._id)

    @property
    def type(self) -> str:
        return deepcopy(self._core.core_type)

    @property
    def core_count(self) -> int:
        return deepcopy(self._core.num_core)

    @property
    def max_memory(self) -> int:
        return deepcopy(self._memory.size)

    def __str__(self) -> str:
        """
        Details of the Host as string
        :return: A String containing all details of the host.
        """
        return ''.join(
            (self.name, ':',
             self.type, '-',
             'Core:', str(self.core_count), '-',
             'Mem:', str(self.max_memory)
             )
        )


if __name__ == "__main__":
    for i in range(0, 100):
        c = DataCenter()
        h = Host(c)
        print(h)
