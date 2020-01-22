from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.OutOfMemoryException import OutOfMemoryException
from AIIntuition.journeys.journey5.FailedToCompleteException import FailedToCompleteException
from AIIntuition.journeys.journey5.log import Log
from AIIntuition.journeys.journey5.event import SchedulerEvent, HostEvent, TaskEvent, FailureEvent
from AIIntuition.journeys.journey5.case import Case
from AIIntuition.journeys.journey5.testcasesetup import TestCaseSetUp
from AIIntuition.journeys.journey5.systemtime import SystemTime


class Scheduler:

    def __init__(self,
                 test_case: Case):
        """
        Instantiate a chosen schedule test case that sets up a schedule environment
        """
        self._num_hosts = None
        self._num_apps = None
        self._policy = None
        self._compute_iter = None

        self._num_hosts, self._num_apps, self._policy, self._compute_iter, self._num_run_days = \
            test_case.set_up()

    def run(self) -> None:
        """
        Run the test case given
        """
        Log.log_event(SchedulerEvent(SystemTime(0, 0), SchedulerEvent.SchedulerEventType.START))

        for day in range(0, self._num_run_days):
            Log.log_event(SchedulerEvent(SystemTime(day, 0), SchedulerEvent.SchedulerEventType.NEW_DAY), str(day + 1))
            for gmt_hour_of_day in range(0, 23):
                sys_time = SystemTime(day, gmt_hour_of_day)
                for c in range(0, self._num_hosts):
                    hst = self.next_compute()
                    for i in range(0, hst.num_associated_task):
                        try:
                            hst.run_next_task(gmt_hour_of_day)
                        except (OutOfMemoryException, FailedToCompleteException) as e:
                            Log.log_event(FailureEvent(sys_time=sys_time, exception=e, compute=e.compute, task=e.task))
                            self._policy.select_optimal_compute(e.task).associate_task(e.task)  # re schedule
            self._log_host_and_task_status(day)
        Log.log_event(SchedulerEvent(SystemTime(self._num_run_days + 1, 0), SchedulerEvent.SchedulerEventType.COMPLETE))
        return

    def _log_host_and_task_status(self,
                                  day: int) -> None:
        """
        Log the current state of all hosts and all of their tasks
        :param day: The current scheduler day
        """
        for h in Host.all_hosts():
            Log.log_event(HostEvent(SystemTime(day, 0), HostEvent.HostEventType.STATUS, h))
            for t in h.all_tasks():
                Log.log_event(TaskEvent(SystemTime(day, 0), TaskEvent.TaskEventType.STATUS, t))

    def next_compute(self) -> Compute:
        """
        Random iteration over all existing compute resources, once all resources have been iterated over
        the random iteration is reset and starts again.
        :return: Compute resource from random (& infinite) iteration.
        """
        return next(self._compute_iter)


if __name__ == "__main__":
    Scheduler(TestCaseSetUp.TestCase.CORE_MISMATCH.value).run()
