from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from typing import List, Tuple
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.util import Util


class EventType(ABC):

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
        lbls = ['Load: ',
                'Profile: ',
                'Pref Core: ',
                'Curr Mem: ',
                'Run Time: ',
                'Time Left: ']

        props = [str(task.id),
                 task.task_type,
                 task.core_type,
                 str(task.current_mem),
                 str(task.run_time),
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
                'Num Loads: ']

        props = [compute.data_center,
                 str(compute.id),
                 compute.type,
                 str(compute.core_count),
                 str(compute.max_memory),
                 Util.to_pct(compute.current_memory, compute.max_memory),
                 str(compute.num_associated_load)]

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
        for t in argv:
            k, v = t
            s = [', '] * len(k)
            f = f + [e for l in list(zip(k, v, s)) for e in l]
        return f

    @classmethod
    def task_and_comp_to_str(cls,
                             preamble: Tuple[List[str], List[str]],
                             task: Task,
                             comp: Compute):
        task_props = EventType.task_properties(task)
        comp_props = EventType.compute_properties(comp)
        as_str = ''.join(EventType.zip_and_separate(preamble, task_props, comp_props))
        return as_str


class AuditEvent(EventType):
    @property
    def id(self) -> int:
        return 1

    def __str__(self) -> str:
        return 'Audit'


class FailureEvent(EventType):
    def __init__(self,
                 task: Task,
                 compute: Compute,
                 exception_class: str):
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)
        self._exception_class = exception_class

    @property
    def id(self) -> int:
        return 2

    def __str__(self) -> str:
        preamble = (['Event'], ['Failure:' + self._exception_class])
        return EventType.task_and_comp_to_str(preamble, self._task, self._compute)


class ExecuteEvent(EventType):

    def __init__(self,
                 task: Task,
                 compute: Compute):
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)

    @property
    def id(self) -> int:
        return 3

    def __str__(self) -> str:
        preamble = (['Event'], ['Execute:'])
        return EventType.task_and_comp_to_str(preamble, self._task, self._compute)


class TaskEvent(EventType):

    def __init__(self,
                 task: Task,
                 compute: Compute):
        self._task = deepcopy(task)
        self._compute = deepcopy(compute)

    @property
    def id(self) -> int:
        return 4

    def __str__(self) -> str:
        task_props = EventType.task_properties(self._task)
        comp_props = EventType.compute_properties(self._compute)
        preamble = ['Event', 'Exception:']
        as_str = ''.join(EventType.zip_and_separate(preamble, *task_props, *comp_props))
        return as_str


class DoneEvent(EventType):

    def __init__(self,
                 task: Task,
                 compute: Compute):
        self._load = deepcopy(task)
        self._compute = deepcopy(compute)

    @property
    def id(self) -> int:
        return 5

    def __str__(self) -> str:
        task_props = EventType.task_properties(self._task)
        comp_props = EventType.compute_properties(self._compute)
        preamble = ['Event', 'Exception:']
        as_str = ''.join(EventType.zip_and_separate(preamble, *task_props, *comp_props))
        return as_str
