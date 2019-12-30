from random import seed
from random import randint
from copy import deepcopy
import numpy as np

from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.compute import Compute


class Host(Compute):
    seed(42)

    # Probability distribution of availability of compute types
    # gpu, compute, batch ToDo: Refactor into DataCenter
    __p_dist_capacity = {
        DataCenter.perf_tier_mnemonic_top(): [0.75, 0.25, 0.00],
        DataCenter.perf_tier_mnemonic_mid(): [0.20, 0.70, 0.10],
        DataCenter.perf_tier_mnemonic_low(): [0.00, 0.20, 0.80]
    }

    # Cores, Memory, performance distribution
    __p_dist_type = {
        Core.gpu_mnemonic(): [[16, 8, 4], [64, 32, 16], [0.1, 0.8, 0.1]],
        Core.compute_mnemonic(): [[8, 4, 2], [265, 128, 64], [0.7, 0.2, 0.1]],
        Core.batch_mnemonic(): [[4, 2, 1], [32, 16, 8], [0.1, 0.8, 0.1]]
    }

    __host_ids = {}

    MAX_HOST_ID = 99999
    LEN_MAX_HOST = len(str(MAX_HOST_ID))
    __all_hosts = {}

    def __init__(self):
        """
        Create a new random host according to the defined probability distributions
        Data Center, Type & capacity.
        """
        self._data_center = DataCenter()
        self._id = self.__gen_host_id()
        self.cost = self._data_center.compute_cost
        _pdc = Host.__p_dist_capacity[self._data_center.performance_tier]
        self._compute_type = Core.core_types()[np.random.choice(np.arange(0, 3), p=_pdc)]
        self._cores, _memory, _dist = Host.__p_dist_type[self.type]
        self._core_count = self._cores[np.random.choice(np.arange(0, 3), p=_dist)]
        self._memory = _memory[np.random.choice(np.arange(0, 3), p=_dist)]
        self.__all_hosts[self.name] = self
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
        return deepcopy(self._compute_type)

    @property
    def core_count(self) -> int:
        return deepcopy(self._core_count)

    @property
    def max_memory(self) -> int:
        return deepcopy(self._memory)

    @classmethod
    def all_hosts(cls) -> list:
        """
        Create a deepcopy list of all hosts created at this point in time.
        :return: A list of Host(s)
        """
        host_list = []
        for k in Host.__all_hosts.keys():
            host_list.append(deepcopy(Host.__all_hosts[k]))
        return host_list

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

    @classmethod
    def __gen_host_id(cls) -> str:
        """
        Generate a random & unique host id in range 0 to 99'999 that has not already been
        allocated.
        :return: Host id as string with leading zeros, string length always = 5
        """
        rnd_host_id = randint(0, Host.MAX_HOST_ID)
        while rnd_host_id not in cls.__host_ids:
            rnd_host_id = randint(0, Host.MAX_HOST_ID)
            cls.__host_ids[rnd_host_id] = True
        return str(rnd_host_id).zfill(Host.LEN_MAX_HOST)


if __name__ == "__main__":
    for i in range(1, 9999):
        x = Host()
    for h in Host.all_hosts():
        print(h)
