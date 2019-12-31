from abc import ABC, abstractclassmethod, abstractmethod


class EventType(ABC):

    @property
    @abstractmethod
    def id(self) -> str:
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


class AuditEvent(EventType):
    @property
    def id(self) -> str:
        return 1

    def __str__(self) -> str:
        return 'Audit'


class FailureEvent(EventType):
    @property
    def id(self) -> str:
        return 2

    def __str__(self) -> str:
        return 'Failure'
