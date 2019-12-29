from random import seed
from random import randint
from copy import deepcopy
import numpy as np

from AIIntuition.journeys.journey5.country import Country


class Host:
    seed(42)

    # Probability Distribution : Types of host by region
    # High End, Mid Range, Low End
    # Max/Min Mem
    # p dist Mem
    m_type = ['GPU', 'CPU', 'BAT']  # GPU, High End Compute, Low End Compute
    p_dist_capacity = {
        Country.perf_tier_mnemonic_top(): [0.75, 0.25, 0.00],
        Country.perf_tier_mnemonic_mid(): [0.20, 0.70, 0.10],
        Country.perf_tier_mnemonic_low(): [0.00, 0.20, 0.80]
    }
    p_dist_type = {
        'GPU': [[16, 8, 4], [64, 32, 16], [0.1, 0.8, 0.1]],
        'CPU': [[8, 4, 2], [265, 128, 64], [0.7, 0.2, 0.1]],
        'BAT': [[4, 2, 1], [32, 16, 8], [0.1, 0.8, 0.1]]
    }

    host_ids = {}

    MAX_HOST_ID = 99999
    LEN_MAX_HOST = len(str(MAX_HOST_ID))
    host_list = {}

    def __init__(self):
        """
        Create a new random host according to the defined probability distributions
        Country, Type & capacity.
        """
        self._country = Country()
        self._id = self.gen_host_id()
        self.cost = self._country.compute_cost
        _pdc = Host.p_dist_capacity[self._country.performance_tier]
        self._machine_type = Host.m_type[np.random.choice(np.arange(0, 3), p=_pdc)]
        self._cores, _memory, _dist = Host.p_dist_type[self.machine_type]
        self._core_count = self._cores[np.random.choice(np.arange(0, 3), p=_dist)]
        self._memory = _memory[np.random.choice(np.arange(0, 3), p=_dist)]
        self.host_list[self.name] = self
        return

    @property
    def country(self) -> str:
        return self._country.country_mnemonic

    @property
    def name(self) -> str:
        return ''.join((self.country, '_', self._id))

    @property
    def id(self) -> str:
        return self._id

    @property
    def machine_type(self) -> str:
        return self._machine_type

    @property
    def core_count(self) -> int:
        return self._core_count

    @property
    def memory(self) -> int:
        return self._memory

    @classmethod
    def all_hosts(cls) -> list:
        """
        Create a deepcopy list of all hosts created at this point in time.
        :return: A list of Host(s)
        """
        hlist = []
        for k in Host.host_list.keys():
            hlist.append(deepcopy(Host.host_list[k]))
        return hlist

    def __str__(self) -> str:
        """
        Details of the Host as string
        :return: A String containing all details of the host.
        """
        return ''.join(
            (self.name, ':',
             self.machine_type, '-',
             'Core:', str(self.core_count), '-',
             'Mem:', str(self.memory)
             )
        )

    @classmethod
    def gen_host_id(cls) -> str:
        """
        Generate a random & unique host id in range 0 to 99'999 that has not already been
        allocated.
        :return: Host id as string with leading zeros, string length always = 5
        """
        rnd_host_id = randint(0, Host.MAX_HOST_ID)
        while rnd_host_id not in cls.host_ids:
            rnd_host_id = randint(0, Host.MAX_HOST_ID)
            cls.host_ids[rnd_host_id] = True
        return str(rnd_host_id).zfill(Host.LEN_MAX_HOST)


if __name__ == "__main__":
    for i in range(1, 9999):
        x = Host()
    for h in Host.all_hosts():
        print(h.name)
