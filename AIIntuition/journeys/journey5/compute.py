from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from random import randint
from AIIntuition.journeys.journey5.load import Load

"""
Abstract Base Class for anything that can supply compute capability.  
"""


class Compute(ABC):
    __compute_ids = {}
    MAX_COMPUTE_ID = 99999
    LEN_MAX_COMPUTE = len(str(MAX_COMPUTE_ID))

    __all_computes = {}

    @property
    @abstractmethod
    def data_center(self) -> str:
        """
        The Mnemonic of the Data Center where the compute resource is located
        :return: Data Center Mnemonic
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The Unique compute resource name
        :return: Compute resource name
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The unique numerical id of the resource
        :return: The Unique id as a string padded with leading Zeros
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> str:
        """
        The Mnemonic (Core) of the type of compute resource e.g. GPU capability
        :return: The machine type Mnemonic
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_count(self) -> int:
        """
        The number of compute cores of the given type for this compute resource
        :return: The number of compute cores
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_memory(self) -> int:
        """
        The maximum amount of memory of the given compute resource
        :return: The max memory available in MB
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def num_associated_load(self) -> int:
        """
        The number of Loads currently associated with this Compute
        :return: The number of associated loads.
        """
        raise NotImplementedError

    @abstractmethod
    def associate_load(self,
                       load: Load) -> None:
        """
        Associate the given load with this host such that the host will execute the load during it's run cycle.
        :param load: The Load to associate with the Host
        """
        raise NotImplementedError

    @abstractmethod
    def run_next_load(self,
                      hour_of_day: int) -> None:
        """
        Randomly pick a load from the list of associated and run it - eventually all loads will be run. It is possible
        that loads will not all be run an equal number of times.
        :param hour_of_day: The current (local time) hour of the day
        """
        raise NotImplementedError

    @classmethod
    def __register(cls,
                   id_to_register: str,
                   inst: 'Compute') -> None:
        cls.__all_computes[id_to_register] = inst
        return

    @classmethod
    def gen_compute_id(cls,
                       inst: 'Compute') -> str:
        """
        Generate a random & unique compute id in range 0 to MAX_COMPUTE_ID that has not already been
        allocated.
        :return: Compute id as string with leading zeros, string length always = LEN_MAX_COMPUTE
        """
        rnd_host_id = randint(0, cls.MAX_COMPUTE_ID)
        while rnd_host_id not in cls.__compute_ids:
            rnd_host_id = randint(0, cls.MAX_COMPUTE_ID)
            cls.__compute_ids[rnd_host_id] = True
        _cid = str(rnd_host_id).zfill(cls.LEN_MAX_COMPUTE)
        cls.__register(_cid, inst)
        return _cid

    @classmethod
    def all_computes(cls) -> list:
        """
        Create a deepcopy list of all hosts created at this point in time.
        :return: A list of Host(s)
        """
        compute_list = []
        for k in cls.__all_computes.keys():
            compute_list.append(deepcopy(cls.__all_computes[k]))
        return compute_list
