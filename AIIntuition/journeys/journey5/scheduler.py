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
    _start_hour = 0
    _end_hour = 24
    _start_day = 0

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
        st = SystemTime(self._start_day, self._start_hour)
        Log.log_event(st, SchedulerEvent(st, SchedulerEvent.SchedulerEventType.START))

        for day in range(0, self._num_run_days):
            st = SystemTime(day, self._start_hour)
            Log.log_event(st, SchedulerEvent(st, SchedulerEvent.SchedulerEventType.NEW_DAY))
            for gmt_hour_of_day in range(self._start_hour, self._end_hour):
                sys_time = SystemTime(day, gmt_hour_of_day)
                for c in range(0, self._num_hosts):
                    hst = self.next_compute()
                    for i in range(0, hst.num_associated_task):
                        try:
                            hst.run_next_task(sys_time=sys_time)
                        except (OutOfMemoryException, FailedToCompleteException) as e:
                            Log.log_event(sys_time, FailureEvent(sys_time, exception=e, compute=e.compute, task=e.task))
                            self._policy.select_optimal_compute(e.task).associate_task(sys_time, e.task)  # re schedule
            self._log_host_and_task_status(st)
        st = SystemTime(self._num_run_days + 1, 0)
        Log.log_event(st, SchedulerEvent(st, SchedulerEvent.SchedulerEventType.COMPLETE))
        return

    @staticmethod
    def _log_host_and_task_status(sys_time: SystemTime) -> None:
        """
        Log the current state of all hosts and all of their tasks
        :param sys_time: The current system time.
        :param day: The current scheduler day
        """
        for h in Host.all_hosts():
            Log.log_event(sys_time, HostEvent(sys_time, HostEvent.HostEventType.STATUS, h))
            for t in h.all_tasks():
                Log.log_event(sys_time, TaskEvent(sys_time, TaskEvent.TaskEventType.STATUS, t))

    def next_compute(self) -> Compute:
        """
        Random iteration over all existing compute resources, once all resources have been iterated over
        the random iteration is reset and starts again.
        :return: Compute resource from random (& infinite) iteration.
        """
        return next(self._compute_iter)


if __name__ == "__main__":
    Scheduler(TestCaseSetUp.TestCase.CORE_MISMATCH.value).run()
