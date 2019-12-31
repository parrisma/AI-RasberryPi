from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.app import App
from AIIntuition.journeys.journey5.infrnditer import InfRndIter
from AIIntuition.journeys.journey5.OutOfMemoryException import OutOfMemoryException


class Scheduler:

    def __init__(self,
                 num_hosts: int,
                 num_apps: int):
        """
        Create the given number of compute hosts and set the max number of concurrent applications.
        :param num_hosts: The number of hosts to create
        :param num_apps: The max number of applications to run
        """
        self.__num_hosts = num_hosts
        self.__num_apps = num_apps

        dc = DataCenter()  # Pick a data centre according to DC distribution
        h = Host(dc)  # Create a Host in the chosen Data Centre
        a1 = App()
        a2 = App()
        h.associate_load(a1)
        h.associate_load(a2)
        self._compute_iter = InfRndIter(Host.all_hosts())

    def run(self,
            num_days: int) -> None:
        """
        Run between zero and the given max number of applications on the hosts for the given number of
        24 hour periods
        :param num_days: The number of 24 hour periods to run for
        """
        for days in range(0, num_days):
            for gmt_hour_of_day in range(0, 23):
                for c in range(0, self.__num_hosts):
                    hst = self.next_compute()
                    for i in range(0, hst.num_associated_load):
                        try:
                            hst.run_next_load(gmt_hour_of_day)
                        except OutOfMemoryException as e:
                            print(e)

    def next_compute(self) -> Compute:
        """
        Random iteration over all existing compute resources, once all resources have been iterated over
        the random iteration is reset and starts again.
        :return: Compute resource from random (& infinite) iteration.
        """
        return next(self._compute_iter)


if __name__ == "__main__":
    s = Scheduler(1, 2)
    s.run(1)
    print('Done')
