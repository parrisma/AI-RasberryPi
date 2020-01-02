from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from typing import List
from typing import Dict
from random import randint

"""
Abstract Base Class for anything that can be considered a compute load e.g. an Application.
"""


class Task(ABC):
    __MAX_TASK_ID = 999999
    __LEN_MAX_TASK = len(str(__MAX_TASK_ID))
    __task_ids = {}
    __all_tasks = {}

    __task_flat = [0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33,
                   0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33]
    __task_st_ed = [0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.8, 0.9, 1, 0.9, 0.7,
                    0.3, 0.2, 0.1]
    __task_mid = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                  0.1, 0.1, 0.1]
    __task_saw = [0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4,
                  0.6, 0.9, 0.1, 0.1]

    __flat_s = 'Flat'
    __st_ed_s = 'Sod-Eod'
    __midday_s = 'Midday'
    __saw_s = 'Saw'

    __activity_types_l = [__flat_s, __st_ed_s, __midday_s, __saw_s]
    __activity = {
        __flat_s: __task_flat,
        __st_ed_s: __task_st_ed,
        __midday_s: __task_mid,
        __saw_s: __task_saw
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
    def task_type(self) -> str:
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
    def run_time(self) -> int:
        """
        The total number of hours the load has to run for
        :return: The total runtime in hours
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def curr_run_time(self) -> int:
        """
        The number of hours the load has been running for
        :return: The current runtime in hours (0 => load done)
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
    def current_compute(self) -> float:
        """
        The current compute demand of the Load on the Compute resource it is running on
        :return: The amount of compute
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def effective_compute(self) -> float:
        """
        The effective compute demand of the Load on the Compute resource it is running on. This can be greater or
        less then the current_compute if the compute is being supplied by a non preferred core type
        :return: The amount of compute
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def compute_deficit(self) -> float:
        """
        The number of compute cycles behind the task is based on demand and the number of executions
        :return: The amount of compute deficit
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
    def task_failure(self,
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
                local_hour_of_day: int,
                available_mem: int,
                available_compute: int,
                compute_efficacy) -> None:
        """
        Run a compute cycle of the application.
        :param local_hour_of_day: The hour of day (local time)
        :param available_mem: The memory allocated to
        :param available_compute: The compute capacity available to the App
        :param compute_efficacy: The translation applied if requirec core type not available on associated compute
        """
        raise NotImplementedError

    @classmethod
    def activity_types(cls) -> List[str]:
        """
        List of types of load profile over a 24 hour period
        :return: List of load types as string
        """
        return deepcopy(cls.__activity_types_l)

    @classmethod
    def activity_profiles(cls) -> Dict[str, List[float]]:
        """
        Dictionary of load profiles
        :return: Dictionary of load profiles keyed by load type
        """
        return deepcopy(cls.__activity)

    @classmethod
    def loads(cls) -> List['Task']:
        """
        List of currently registered loads
        :return: List of registered Loads
        """
        return deepcopy(list(cls.__all_tasks.values()))

    @classmethod
    def __register(cls,
                   id_to_register: str,
                   inst: 'Task') -> None:
        cls.__all_tasks[id_to_register] = inst
        return

    @classmethod
    def gen_id(cls,
               inst: 'Task') -> str:
        """
        Generate a random & unique host id in range 0 to Load.MAX_LOAD_ID that has not already been
        allocated.
        :return: Host id as string with leading zeros, string length always = 5
        """
        rnd_app_id = randint(0, cls.__MAX_TASK_ID)
        while rnd_app_id not in cls.__task_ids:
            rnd_app_id = randint(0, cls.__MAX_TASK_ID)
            cls.__task_ids[rnd_app_id] = True
        _id = str(rnd_app_id).zfill(cls.__LEN_MAX_TASK)
        cls.__register(_id, inst)
        return deepcopy(_id)

    @classmethod
    def all_tasks(cls) -> list:
        """
        Create a deepcopy list of all Loads created at this point in time.
        :return: A list of Loads
        """
        task_list = []
        for k in cls.__all_tasks.keys():
            task_list.append(deepcopy(cls.__all_tasks[k]))
        return task_list