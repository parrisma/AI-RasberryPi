from abc import ABC, abstractclassmethod, abstractmethod

"""
Abstract Base Class for anything that can supply compute capability.  
"""


class Compute(ABC):

    @property
    @abstractmethod
    def data_center(self) -> str:
        """
        The Mnemonic of the Data Center where the compute resource is located
        :return: Data Center Mnemonic
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """
        The Unique compute resource name
        :return: Compute resource name
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The unique numerical id of the resource
        :return: The Unique id as a string padded with leading Zeros
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def type(self) -> str:
        """
        The Mnemonic (Core) of the type of compute resource e.g. GPU capability
        :return: The machine type Mnemonic
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_count(self) -> int:
        """
        The number of compute cores of the given type for this compute resource
        :return: The number of compute cores
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def max_memory(self) -> int:
        """
        The maximum amount of memory of the given compute resource
        :return: The max memory available in MB
        """
        raise NotImplementedError
