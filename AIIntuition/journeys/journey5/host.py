from copy import deepcopy
from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.memory import Memory
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.infrnditer import InfRndIter
from AIIntuition.journeys.journey5.OutOfMemoryException import OutOfMemoryException
from AIIntuition.journeys.journey5.log import Log
from AIIntuition.journeys.journey5.eventtype import AuditEvent, ExecuteEvent, DoneEvent
from AIIntuition.journeys.journey5.util import Util


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
        self._memory_available = Memory(self._core)
        self._loads = {}
        self._inf_load_iter = None  # The infinite iterate to use when running associated loads.
        self._curr_mem = 0
        self._curr_comp = 0
        Log.log_event(AuditEvent(), 'Host instantiated:', self)
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
        return deepcopy(self._memory_available.size)

    @property
    def current_memory(self) -> int:
        """
        The current memory utilisation
        :return: The current memory utilisation in MB
        """
        return deepcopy(self._curr_mem)

    def associate_load(self,
                       load: Task) -> None:
        """
        Associate the given load with this host such that the host will execute the load during it's run
        cycle.
        :param load: The Load to associate with the Host
        """
        self._loads[load.id] = load
        self.__update_inf_iter()
        Log.log_event(AuditEvent(), 'Load:', load, 'associated with host:', self)
        return

    def disassociate_load(self,
                          load: Task) -> None:
        """
        Associate the given load with this host such that the host will execute the load during it's run
        cycle.
        :param load: The Load to associate with the Host
        """
        if load.id not in self._loads:
            raise ValueError(load.id + ' is not associated with host :' + self.id)

        del self._loads[load.id]
        self.__update_inf_iter()

        return

    @property
    def num_associated_load(self) -> int:
        """
        The number of Loads currently associated with this Compute
        :return: The number of associated loads.
        """
        return len(self._loads)

    def run_next_load(self,
                      gmt_hour_of_day: int) -> None:
        """
        Randomly pick a load from the list of associated and run it - eventually all loads will be run. It is possible
        that loads will not all be run an equal number of times.
        :param gmt_hour_of_day: The gmt hour of day at which the load is being executed
        """
        local_hour_of_day = self._data_center.local_hour_of_day(gmt_hour_of_day)

        if len(self._loads) == 0:
            print("No loads to run on Host:" + self.id)
            return

        # Get next (random) load to run
        ltr = self.__next_load_to_execute()

        if ltr.done:
            self.disassociate_load(ltr)
            Log.log_event(DoneEvent(ltr, self))
        else:
            # Get current & required demand
            cd, cc, ct, md, cm = ltr.resource_demand(local_hour_of_day)
            self._curr_comp = max(0, self._curr_comp - cc)  # Pay back current compute use
            self._curr_mem = max(0, self._curr_mem - cm)  # Pay back current mem use

            # Check memory which is finite & fail the load if insufficient memory is available
            if self._curr_mem + md > self._memory_available.size:
                e = OutOfMemoryException(ltr, self)
                ltr.task_failure(e)
                self.disassociate_load(ltr)
                raise e

            self._curr_mem += md
            ltr.execute(local_hour_of_day, int(1e6))
            Log.log_event(ExecuteEvent(ltr, self), '')
        return

    def __update_inf_iter(self) -> None:
        """
        Update the infinite iterator to reflect change to the associated loads.
        """
        self._inf_load_iter = InfRndIter(list(self._loads.keys()))
        return

    def __next_load_to_execute(self) -> Task:
        """
        The random next associated load to execute
        :return: The Load to execute
        """
        return self._loads[next(self._inf_load_iter)]

    @classmethod
    def all_hosts(cls) -> list:
        """
        Create a deepcopy list of all loads (Hosts) created at this point in time.
        :return: A list of App(s)
        """
        host_list = []
        all_comp = Compute.all_computes()
        for comp in all_comp:
            if isinstance(comp, Host):
                host_list.append(deepcopy(comp))
        return host_list

    def all_loads(self) -> list:
        """
        Create a deepcopy list of all Loads associated with the host at this point in time
        :return: A list of loads
        """
        load_list = []
        for k in self._loads.keys():
            load_list.append(deepcopy(self._loads[k]))
        return load_list

    def __str__(self) -> str:
        """
        Details of the Host as string
        :return: A String containing all details of the host.
        """
        return ''.join(
            (self.name, ':',
             self.type, '-',
             'Core:', str(self.core_count), '-',
             'Mem:', str(self.max_memory), '-Mem Util:',
             Util.to_pct(self._curr_mem, self.max_memory), '% '
             )
        )


if __name__ == "__main__":
    for i in range(0, 100):
        c = DataCenter()
        h = Host(c)
        print(h)
