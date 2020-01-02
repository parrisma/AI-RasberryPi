from datetime import datetime
from copy import deepcopy
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.errorcode import ErrorCode
from AIIntuition.journeys.journey5.log import Log
from AIIntuition.journeys.journey5.event import FailureEvent


class FailedToCompleteException(Exception):
    """
    Raised when an application has a compute deficit when it runs out of compute cycles.
    """

    def __init__(self,
                 task: Task,
                 compute: Compute):
        """
        Record a task incomplete issue for Load on Compute
        :param task: The task that required more compute than was available & thus failed
        :param compute: The Compute that was unable to supply the required compute
        """
        self._event_time = time = datetime.now().strftime("%H:%M:%S")
        self._task = task
        self._compute = compute
        self._error_code = ErrorCode.FAILED_TO_COMPLETE

    def __str__(self) -> str:
        log_msg = Log.log_message(FailureEvent(self.__class__.__name__, self._task, self._compute))
        return log_msg

    @property
    def task(self) -> Task:
        return self._task

    @property
    def compute(self) -> Compute:
        return self._compute

    @property
    def event_time(self) -> str:
        return deepcopy(self._event_time)

    @property
    def error_code(self) -> int:
        return self._error_code.value
