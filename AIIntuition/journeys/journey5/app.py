from random import seed
from copy import deepcopy
from typing import List
import math
import numpy as np

from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.load import Load
from AIIntuition.journeys.journey5.AppOutOfMemoryException import AppOutOfMemoryException


class App(Load):
    seed(42)

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
        self.__id = Load.gen_id(self)
        self.__max_mem_demand = self.__memory_asks[np.random.choice(np.arange(0, 7), p=self.__psidt_memory_demand)]
        self.__memory_volatility = np.random.uniform(0, 0.1)
        self.__core_demand = Core.core_types()[np.random.choice(np.arange(0, 3), p=self.__pdist_compute_core_demand)]
        self.__core_volatility = np.random.uniform(0, 0.25)
        lt = np.random.choice(np.arange(0, 4), p=self.__pdist_loads)
        self.__load_type = Load.load_types()[lt]
        self.__load_profile = Load.load_profiles()[self.__load_type]
        self.__run_time_ask = np.ceil(np.random.uniform(0.0, 72.0))
        # Properties that change during execution
        self.__run_time_in_elapse_hours = None
        self.__core_load = None
        self.__compute_deficit = None
        self.__current_mem = None
        self.__reset()

    def __reset(self) -> None:
        """
        Set the application to it's initial launch state
        :return:
        """
        self.__run_time_in_elapse_hours = self.__run_time_ask
        self.__core_load = 1  # np.ceil(np.random.uniform(0.0, 4.0))
        self.__compute_deficit = 0
        self.__current_mem = 1
        return

    @property
    def id(self) -> str:
        return deepcopy(self.__id)

    @property
    def load_type(self) -> str:
        return deepcopy(self.__load_type)

    @property
    def core_type(self) -> str:
        return deepcopy(self.__core_demand)

    def resource_demand(self,
                        hour_of_day: int) -> List:
        """
        Return the amount of memory and compute needed given the hour of the day.
        Zero Compute => Application has successfully completed
        :param hour_of_day: Local time - hour of day as integer 0 - 23
        :return: List: Compute Demand & Memory Demand for given hour of day
        """
        compute_demand = self.__compute_demand(hour_of_day)
        memory_demand = self.__memory_demand(hour_of_day)
        return [compute_demand, memory_demand]

    @classmethod
    def all_apps(cls) -> list:
        """
        Create a deepcopy list of all Applications created at this point in time.
        :return: A list of App(s)
        """
        app_list = []
        for k in App.__all_loads.keys():
            app_list.append(deepcopy(App.__all_loads[k]))
        return app_list

    def execute(self,
                hour_of_day: int,
                available_mem: int,
                available_compute: int) -> list:
        """
        Run a compute cycle of the application.
        :param hour_of_day: The hour of day (local time)
        :param available_mem: The memory available to the App
        :param available_compute: The compute capacity available to the App
        :return: List: Compute Demand & Memory Demand for given hour of day
        :except: AppOutOfMemoryException if application needs more memory than available.
        """
        compute_demand = self.__compute_demand(hour_of_day)
        memory_demand = self.__memory_demand(hour_of_day)

        self.__run_time_in_elapse_hours -= 1
        if memory_demand > available_mem:
            raise AppOutOfMemoryException(self.id)
        self.__compute_deficit += min(0, compute_demand - available_compute)
        return [compute_demand, memory_demand]

    def __memory_demand(self,
                        hour_of_day: int) -> int:
        """
        Given the hour of the day what is the memory demand of the App.
        :param hour_of_day:
        :return: Memory demand in GB
        """
        new_mem = self.__max_mem_demand * self.__load_profile[hour_of_day]
        new_mem *= (1 + np.random.uniform(-self.__memory_volatility, +self.__memory_volatility))
        new_mem = math.ceil(new_mem)
        new_mem = min(new_mem, self.__max_mem_demand)
        new_mem = max(new_mem, 0)
        self.__current_mem = new_mem
        return new_mem

    def __compute_demand(self,
                         hour_of_day: int) -> int:
        """
        What is the total compute demand given the hour of the day.
        :param hour_of_day: hour_of_day: Local time - hour of day as integer 0 - 23
        :return: Compute demand as integer (units * 1 hour) - where 1 unit = 1 x GPU, Compute etc
        """
        compute_demand = (self.__core_load * self.__load_profile[hour_of_day]) + self.__compute_deficit
        return int(np.ceil(compute_demand))

    def __str__(self):
        return ''.join((self.id, ': ',
                        'load: ', self.load_type , ': ',
                        'cores: ', self.core_type, ': ',
                        'Mem(Max,Curr):',
                        str(self.__max_mem_demand), ',',
                        str(self.__current_mem), ',',
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
