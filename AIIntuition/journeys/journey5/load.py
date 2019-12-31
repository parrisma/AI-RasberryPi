from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from typing import List
from typing import Dict
from random import randint

"""
Abstract Base Class for anything that can be considered a compute load e.g. an Application.
"""


class Load(ABC):
    __MAX_LOAD_ID = 999999
    __LEN_MAX_LOAD = len(str(__MAX_LOAD_ID))
    __load_ids = {}
    __all_loads = {}

    __load_flat = [0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33,
                   0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33]
    __load_st_ed = [0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.8, 0.9, 1, 0.9, 0.7,
                    0.3, 0.2, 0.1]
    __load_mid = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                  0.1, 0.1, 0.1]
    __load_saw = [0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4,
                  0.6, 0.9, 0.1, 0.1]

    __flat_s = 'Flat'
    __st_ed_s = 'Sod-Eod'
    __midday_s = 'Midday'
    __saw_s = 'Saw'

    __load_types_l = [__flat_s, __st_ed_s, __midday_s, __saw_s]
    __loads = {
        __flat_s: __load_flat,
        __st_ed_s: __load_st_ed,
        __midday_s: __load_mid,
        __saw_s: __load_saw
    }

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The unique id of the Load.
        :return: Id as string that is unique for all loads.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def load_type(self) -> str:
        """
        The type of load profile the load exhibits
        :return: String name of the load profile (in set returned by Load.load_types())
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_type(self) -> str:
        """
        The preferred type of compute Core required by the Load (on of set returned by Core.core_types())
        :return: String name of the load profile (in set returned by load_types())
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def current_mem(self) -> int:
        """
        The current memory utilisation of the Load on the Compute resource it is running on
        :return: The amount of memory in MG (int)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Is the current load finished processing
        :return: True if Load has finished processing, else False
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def failed(self) -> bool:
        """
        Is the current load in a failed state
        :return: True if Load has failed during processing, else False
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def current_mem(self) -> int:
        """
        The current memory utilisation of the Load on the Compute resource it is running on
        :return: The amount of memory in MG (int)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def current_compute(self) -> int:
        """
        The current compute demand of the Load on the Compute resource it is running on
        :return: The amount of compute
        """
        raise NotImplementedError

    @abstractmethod
    def resource_demand(self,
                        hour_of_day: int) -> List[int]:
        """
        Return the amount of memory and compute needed given the hour of the day.
        :param hour_of_day: Local time - hour of day as integer 0 - 23
        :return: List: Compute Demand, Current Compute, Core Type, Memory Demand for given hour of day
        & current mem utilisation
        """
        raise NotImplementedError

    @abstractmethod
    def load_failure(self,
                     reason: Exception = None) -> None:
        """
        Set the load to failre state
        :param reason: Optional Exception that explains the failre cause.
        :return:
        """

    @property
    @abstractmethod
    def failure_reason(self) -> Exception:
        """
        If the load is in a failed state and a reason exception was given, return the failure exception - None if the
        load is not in a failure state
        :return: The exception, if the node is in a failure state and a reason exception was given.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self,
                hour_of_day: int,
                available_compute: int) -> None:
        """
        Run a compute cycle of the application.
        :param hour_of_day: The hour of day (local time)
        :param available_compute: The compute capacity available to the App
        """
        raise NotImplementedError

    @classmethod
    def load_types(cls) -> List[str]:
        """
        List of types of load profile over a 24 hour period
        :return: List of load types as string
        """
        return deepcopy(cls.__load_types_l)

    @classmethod
    def load_profiles(cls) -> Dict[str, List[float]]:
        """
        Dictionary of load profiles
        :return: Dictionary of load profiles keyed by load type
        """
        return deepcopy(cls.__loads)

    @classmethod
    def loads(cls) -> List['Load']:
        """
        List of currently registered loads
        :return: List of registered Loads
        """
        return deepcopy(list(cls.__all_loads.values()))

    @classmethod
    def __register(cls,
                   id_to_register: str,
                   inst: 'Load') -> None:
        cls.__all_loads[id_to_register] = inst
        return

    @classmethod
    def gen_id(cls,
               inst: 'Load') -> str:
        """
        Generate a random & unique host id in range 0 to Load.MAX_LOAD_ID that has not already been
        allocated.
        :return: Host id as string with leading zeros, string length always = 5
        """
        rnd_app_id = randint(0, cls.__MAX_LOAD_ID)
        while rnd_app_id not in cls.__load_ids:
            rnd_app_id = randint(0, cls.__MAX_LOAD_ID)
            cls.__load_ids[rnd_app_id] = True
        _id = str(rnd_app_id).zfill(cls.__LEN_MAX_LOAD)
        cls.__register(_id, inst)
        return deepcopy(_id)

    @classmethod
    def all_loads(cls) -> list:
        """
        Create a deepcopy list of all Loads created at this point in time.
        :return: A list of Loads
        """
        load_list = []
        for k in cls.__all_loads.keys():
            load_list.append(deepcopy(cls.__all_loads[k]))
        return load_list
