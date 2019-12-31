from random import seed
from copy import deepcopy
from typing import List
import math
import numpy as np

from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.load import Load


class App(Load):
    __pdist_compute_core_demand = [0.2, 0.6, 0.2]
    __memory_asks = [128, 64, 32, 16, 8, 2, 1]
    __psidt_memory_demand = [0.05, 0.1, 0.25, 0.3, 0.15, 0.1, 0.05, ]
    __pdist_loads = [.25, .25, .25, .25]

    def __init__(self):
        """
        Create an application with a profile according to the prob distribution of demand
        for Core Type, Memory and expected load profile
        :return:
        """
        self._id = Load.gen_id(self)
        self._max_mem_demand = self.__memory_asks[np.random.choice(np.arange(0, 7), p=self.__psidt_memory_demand)]
        self._memory_volatility = np.random.uniform(0, 0.1)
        self._core_demand = Core.core_types()[np.random.choice(np.arange(0, 3), p=self.__pdist_compute_core_demand)]
        self._core_volatility = np.random.uniform(0, 0.25)
        lt = np.random.choice(np.arange(0, 4), p=self.__pdist_loads)
        self._load_type = Load.load_types()[lt]
        self._load_profile = Load.load_profiles()[self._load_type]
        self._run_time_ask = np.ceil(np.random.uniform(0.0, 72.0))
        # Properties that change during execution
        self._run_time_in_elapse_hours = None
        self._core_load = None
        self._compute_deficit = None
        self._current_mem = None
        self._current_comp = None
        self._failed = None
        self._fail_reason = None
        self._reset()

    def _reset(self) -> None:
        """
        Set the application to it's initial launch state
        :return:
        """
        self._run_time_in_elapse_hours = self._run_time_ask
        self._core_load = 1  # Unitary for starters
        self._compute_deficit = 0
        self._current_mem = 0
        self._current_comp = 0
        self._failed = False
        self._fail_reason = None
        return

    @property
    def id(self) -> str:
        return deepcopy(self._id)

    @property
    def load_type(self) -> str:
        return deepcopy(self._load_type)

    @property
    def core_type(self) -> str:
        return deepcopy(self._core_demand)

    @property
    def done(self) -> bool:
        """
        Is the current load finished processing
        :return: True if Load has finished processing, else False
        """
        return self._run_time_in_elapse_hours == 0

    @property
    def failed(self) -> bool:
        """
        Is the current load in a failed state
        :return: True if Load has failed during processing, else False
        """
        return deepcopy(self._failed)

    @property
    def current_mem(self) -> int:
        """
        The current memory utilisation of the Load on the Compute resource it is running on
        :return: The amount of memory in MG (int)
        """
        return deepcopy(self._current_mem)

    @property
    def current_compute(self) -> int:
        """
        The current compute demand of the Load on the Compute resource it is running on
        :return: The amount of compute
        """
        return deepcopy(self._current_comp)

    # ToDo: return immutable tuple not a list
    def resource_demand(self,
                        hour_of_day: int) -> List[int]:
        """
        Return the amount of memory and compute needed given the hour of the day.
        :param hour_of_day: Local time - hour of day as integer 0 - 23
        :return: List: Compute Demand, Current Compute, Core Type, Memory Demand for given hour of day
        & current mem utilisation
        """
        compute_demand = self.__compute_demand(hour_of_day)
        memory_demand = self.__memory_demand(hour_of_day)
        return [compute_demand,
                self.current_compute,
                self.core_type,
                memory_demand,
                self.current_mem
                ]

    def load_failure(self,
                     reason: Exception = None) -> None:
        """
        Set the load to failre state
        :param reason: Optional Exception that explains the failre cause.
        :return:
        """
        self._failed = True
        self._fail_reason = reason
        return

    @property
    def failure_reason(self) -> Exception:
        """
        If the load is in a failed state and a reason exception was given, return the failure exception - None if the
        load is not in a failure state
        :return: The exception, if the node is in a failure state and a reason exception was given.
        """
        if not self._failed:
            r = None
        else:
            r = self._fail_reason
        return r

    def execute(self,
                hour_of_day: int,
                available_compute: int) -> None:
        """
        Run a compute cycle of the application.
        :param hour_of_day: The hour of day (local time)
        :param available_compute: The compute capacity available to the App
        """
        if not self.done:
            self._run_time_in_elapse_hours -= 1
            self._compute_deficit += min(0, self.__compute_demand(hour_of_day) - available_compute)
        return

    def __memory_demand(self,
                        hour_of_day: int) -> int:
        """
        Given the hour of the day what is the memory demand of the App.
        :param hour_of_day:
        :return: Memory demand in GB
        """
        new_mem = self._max_mem_demand * self._load_profile[hour_of_day]
        new_mem *= (1 + np.random.uniform(-self._memory_volatility, +self._memory_volatility))
        new_mem = math.ceil(new_mem)
        new_mem = min(new_mem, self._max_mem_demand)
        new_mem = max(new_mem, 0)
        self._current_mem = new_mem
        return new_mem

    def __compute_demand(self,
                         hour_of_day: int) -> int:
        """
        What is the total compute demand given the hour of the day.
        :param hour_of_day: hour_of_day: Local time - hour of day as integer 0 - 23
        :return: Compute demand as integer (units * 1 hour) - where 1 unit = 1 x GPU, Compute etc
        """
        compute_demand = (self._core_load * self._load_profile[hour_of_day]) + self._compute_deficit
        return int(np.ceil(compute_demand))

    def __str__(self):
        return ''.join((self.id, ': ',
                        'load: ', self.load_type, ': ',
                        'cores: ', self.core_type, ': ',
                        'Mem(Max,Curr):',
                        str(self._max_mem_demand), ',',
                        str(self._current_mem), ',',
                        )
                       )


if __name__ == "__main__":
    app = None
    for i in range(1, 100):
        app = App()
    for a in Load.loads():
        print(a)
    for h in range(0, 23):
        app.execute(h, 1000, 1000)
        print(app)
