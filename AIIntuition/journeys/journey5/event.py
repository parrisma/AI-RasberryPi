from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Tuple
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.util import Util
from enum import Enum, unique


class Event(ABC):
    @unique
    class EventType(Enum):
        AUDIT = 0
        HOST = 1
        TASK = 2
        FAIL = 3

        def __str__(self):
            return self.value

    __empty_props = ([], [])

    @property
    @abstractmethod
    def id(self) -> int:
        """
        The unique id of the event type
        :return: Event Type Id
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """
        The string name of the event type
        :return: Event Name as string
        """
        raise NotImplementedError

    @classmethod
    def task_properties(cls,
                        task: Task) -> Tuple[List, List]:
        """
        Extract all relevant properties from given task for event reporting
        :param task: the task object subject of the event
        :return: List of task property labels, List of corresponding task property values as string
        """
        lbls = ['Task: ',
                'Profile: ',
                'Pref Core: ',
                'Load Factor: ',
                'Curr Mem: ',
                'Run Time: ',
                'Deficit: ',
                'Cost: ',
                'Time Left: ']

        props = [str(task.id),
                 str(task.task_type),
                 str(task.core_type),
                 str(task.load_factor),
                 str(task.current_mem),
                 str(task.run_time),
                 cls._flt(task.compute_deficit),
                 cls._flt(task.cost),
                 str(task.curr_run_time)]

        return lbls, props

    @classmethod
    def compute_properties(cls,
                           compute: Compute) -> Tuple[List, List]:
        """
        Extract all relevant properties from given compute for event reporting
        :param compute: the compute object subject of the event
        :return: List of compute property labels, List of corresponding compute property values as string
        """
        lbls = ['DC: ',
                'Host: ',
                'Type: ',
                'cores: ',
                'Mem: ',
                'Mem Util %: ',
                'Comp: ',
                'Comp Util %: ',
                'Num Tasks: ']

        props = [compute.data_center,
                 str(compute.id),
                 str(compute.type),
                 str(compute.core_count),
                 str(compute.max_memory),
                 Util.to_pct(compute.current_memory, compute.max_memory),
                 str(compute.max_compute),
                 Util.to_pct(compute.current_compute, compute.max_compute),
                 str(compute.num_associated_task)]

        return lbls, props

    @classmethod
    def exception_properties(cls,
                             exception: Exception) -> Tuple[List, List]:
        """
        Extract all relevant properties from given exception for event reporting
        :param exception: the exception object subject of the event
        :return: List of compute property labels, List of corresponding exception property values as string
        """
        lbls = ['Error: ']
        props = [str(exception)]

        return lbls, props

    @classmethod
    def zip_and_separate(cls,
                         *argv,
                         separator: str = ', '):
        """
        Take an arbitrary set of paris of lists of the form List[Labels], List[Corresponding Values] and zip
        them into a single
        :param argv: List[List[keys 1], List[Values 1],List[keys 2], List[Values 2], ...]
        :param separator: separator to add after each key value pair in the final list
        :return: List[ key1.1, value1.1, Sep, key1.2, value1.2, Sep, .. Key1.n, value1.n, Sep, Key2.1, Value2.1, Sep ..]
        """
        f = []
        for tupl in argv:
            ky, vl = tupl
            s = [separator] * len(ky)
            f = f + [e for l in list(zip(ky, vl, s)) for e in l]  # Flatten out the tuples
        return f

    @classmethod
    def task_and_comp_to_str(cls,
                             preamble: Tuple[List[str], List[str]],
                             task: Task = None,
                             comp: Compute = None,
                             exception: Exception = None):
        task_props = cls.__empty_props
        if task is not None:
            task_props = Event.task_properties(task)
        comp_props = cls.__empty_props
        if comp is not None:
            comp_props = Event.compute_properties(comp)
        exception_props = cls.__empty_props
        if exception is not None:
            exception_props = Event.exception_properties(exception)

        as_str = ''.join(Event.zip_and_separate(preamble, task_props, comp_props, exception_props))
        return as_str

    @classmethod
    def _flt(cls, x: float) -> str:
        return '{:.4f}'.format(x * 1.0)


class FailureEvent(Event):
    def __init__(self,
                 exception: Exception,
                 task: Task = None,
                 compute: Compute = None):
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception_class = exception.__class__.__name__
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.FAIL

    def __str__(self) -> str:
        preamble = (['Event: '], ['Failure-' + self._exception_class])
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception)


class SchedulerEvent(Event):
    class SchedulerEventType(Enum):
        START = 'Start'
        COMPLETE = 'Complete'
        NEW_DAY = 'New Day'

    def __init__(self,
                 host_event_type: SchedulerEventType):
        self._scheduler_event_type = host_event_type

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.HOST

    def __str__(self) -> str:
        preamble = ([self.__class__.__name__ + ':'], [self._scheduler_event_type.value])
        return Event.task_and_comp_to_str(preamble)


class HostEvent(Event):
    class HostEventType(Enum):
        INSTANTIATE = 'Instantiate'
        DONE = 'Done'
        EXECUTE = 'Execute'
        ASSOCIATE = 'Associate'
        DISASSOCIATE = 'Disassociate'
        STATUS = 'Status'

    def __init__(self,
                 host_event_type: HostEventType,
                 compute: Compute,
                 task: Task = None,
                 exception: Exception = None):
        self._host_event_type = host_event_type
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.HOST

    def __str__(self) -> str:
        preamble = ([self.__class__.__name__ + ':'], [self._host_event_type.value])
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception)


class TaskEvent(Event):
    class TaskEventType(Enum):
        STATUS = 'Status'

    def __init__(self,
                 task_event_type: TaskEventType,
                 task: Task,
                 compute: Compute = None,
                 exception: Exception = None):
        self._task_event_type = task_event_type
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception = exception

    @property
    def id(self) -> Event.EventType:
        return Event.EventType.TASK

    def __str__(self) -> str:
        preamble = ([self.__class__.__name__ + ':'], [self._task_event_type.value])
        return Event.task_and_comp_to_str(preamble, self._task, self._compute, self._exception)
