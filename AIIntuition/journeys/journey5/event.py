from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Tuple, Callable
from AIIntuition.journeys.journey5.eventlabels import EventLabels
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.util import Util
from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.seqmap import SeqMap
from AIIntuition.journeys.journey5.caseproperty import CaseProperty
from AIIntuition.journeys.journey5.case import Case
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

    _empty_props = ([], [])

    _seqm_dc = SeqMap(seq_name='Data Centers')
    _seqm_comp = SeqMap(seq_name='Computes')
    _seqm_coret = SeqMap(seq_name='Core Types')
    _seqm_ncore = SeqMap(seq_name='Number of Cores')
    _seqm_memc = SeqMap(seq_name='Memory Size')
    _seqm_compm = SeqMap(seq_name='Max Compute')

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
                        task: Task,
                        as_feature_vector: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given task for event reporting
        :param task: the task object subject of the event
        :param as_feature_vector: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of task property labels, List of corresponding task property values as string
        """
        labels = EventLabels.task_labels(as_feature_vector)

        props = [str(task.id),
                 str(task.task_type),
                 str(task.core_type),
                 str(task.load_factor),
                 str(task.current_mem),
                 str(task.run_time),
                 cls._flt(task.compute_deficit),
                 cls._flt(task.cost),
                 str(task.curr_run_time)]

        return labels, props

    @classmethod
    def compute_properties(cls,
                           compute: Compute,
                           as_feature: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given compute for event reporting
        :param compute: the compute object subject of the event
        :param as_feature: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of compute property labels, List of corresponding compute property values as string
        """
        labels = EventLabels.host_labels(as_feature)

        props = [cls._render(cls._seqm_dc, str, compute.data_center, as_feature),
                 cls._render(cls._seqm_comp, str, compute.id, as_feature),
                 cls._render(cls._seqm_coret, str, compute.type, as_feature),
                 cls._render(cls._seqm_ncore, str, compute.core_count, as_feature),
                 cls._render(cls._seqm_memc, str, compute.max_memory, as_feature),
                 cls._render(str, str, Util.to_pct(compute.current_memory, compute.max_memory), as_feature),
                 cls._render(cls._seqm_compm, str, compute.max_compute, as_feature),
                 cls._render(str, str, Util.to_pct(compute.current_compute, compute.max_compute), as_feature),
                 cls._render(str, str, compute.num_associated_task, as_feature)]

        return labels, props

    @classmethod
    def exception_properties(cls,
                             exception: Exception,
                             as_feature_vector: bool = False) -> Tuple[List, List]:
        """
        Extract all relevant properties from given exception for event reporting
        :param exception: the exception object subject of the event
        :param as_feature_vector: return the properties in feature vector form - One Hot, Normalised etc
        :return: List of compute property labels, List of corresponding exception property values as string
        """
        labels = EventLabels.exception_labels(as_feature_vector)
        props = [str(exception)]

        return labels, props

    @classmethod
    def _render(cls,
                render_func_norm: Callable,
                render_func_feature: Callable,
                value: object,
                as_feature: bool):
        """
        Render the given values as a normal event log or as feature (vector)
        :param render_func_norm: Callable to render value as normal log entry
        :param render_func_feature: Callable to render value as a feature vector item
        :param value: the value to render
        :param as_feature: Render values as feature vector item if true else render as normal log entry
        :return: The rendered value as return by the called render Callable.
        """
        if as_feature:
            return render_func_feature(value)
        else:
            return render_func_norm(value)

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
        task_props = cls._empty_props
        if task is not None:
            task_props = Event.task_properties(task)
        comp_props = cls._empty_props
        if comp is not None:
            comp_props = Event.compute_properties(comp)
        exception_props = cls._empty_props
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
