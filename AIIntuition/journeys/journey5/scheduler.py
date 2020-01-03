from enum import Enum
from functools import partial
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.OutOfMemoryException import OutOfMemoryException
from AIIntuition.journeys.journey5.FailedToCompleteException import FailedToCompleteException
from AIIntuition.journeys.journey5.log import Log
from AIIntuition.journeys.journey5.event import SchedulerEvent, HostEvent, TaskEvent
from AIIntuition.journeys.journey5.randomcase import RandomCase
from AIIntuition.journeys.journey5.onedccase import OneDCCase


class Scheduler:
    class TestCases(Enum):
        RANDOM = partial(RandomCase.set_up)
        ONEDC = partial(OneDCCase.set_up)

    def __init__(self):
        """
        Instantiate a chosen schedule test case that sets up a schedule environment
        """
        self._num_hosts = None
        self._num_apps = None
        self._policy = None
        self._compute_iter = None

        self._num_hosts, self._num_apps, self._policy, self._compute_iter, self._num_run_days = \
            Scheduler.TestCases.ONEDC.value()

    def run(self) -> None:
        """
        Run between zero and the given max number of applications on the hosts for the given number of
        24 hour periods
        :param num_days: The number of 24 hour periods to run for
        """
        Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.START))

        for day in range(0, self._num_run_days):
            Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.NEW_DAY), str(day + 1))
            for gmt_hour_of_day in range(0, 23):
                for c in range(0, self._num_hosts):
                    hst = self.next_compute()
                    for i in range(0, hst.num_associated_task):
                        try:
                            hst.run_next_task(gmt_hour_of_day)
                        except (OutOfMemoryException, FailedToCompleteException) as e:
                            print(e)
                            self._policy.select_optimal_compute(e.task).associate_task(e.task)  # re schedule
            for h in Host.all_hosts():
                Log.log_event(HostEvent(HostEvent.HostEventType.STATUS, h))
                for t in h.all_tasks():
                    Log.log_event(TaskEvent(TaskEvent.TaskEventType.STATUS, t))
        Log.log_event(SchedulerEvent(SchedulerEvent.SchedulerEventType.COMPLETE),
                      "Scheduler done after allotted run time ")
        return

    def next_compute(self) -> Compute:
        """
        Random iteration over all existing compute resources, once all resources have been iterated over
        the random iteration is reset and starts again.
        :return: Compute resource from random (& infinite) iteration.
        """
        return next(self._compute_iter)


if __name__ == "__main__":
    Scheduler().run()
