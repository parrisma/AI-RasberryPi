from copy import deepcopy
import numpy as np
from typing import List

"""
Non instantiable class to capture the characteristics of compute Core types (GPU, CPU etc) 
"""


class Core:
    __gpu_type = 'GPU'
    __compute_type = 'CPU'
    __batch_type = 'BAT'

    __core_equivalency = {
        __gpu_type + __gpu_type: 1.0,
        __gpu_type + __compute_type: 0.25,
        __gpu_type + __batch_type: 0.1,
        __compute_type + __compute_type: 1.0,
        __compute_type + __gpu_type: 1.0,
        __compute_type + __batch_type: 0.5,
        __batch_type + __batch_type: 1.0,
        __batch_type + __compute_type: 2.0,
        __batch_type + __gpu_type: 2.0
    }

    # Cores, distribution
    __p_dist_type = {
        __gpu_type: [[16, 8, 4], [0.1, 0.8, 0.1]],
        __compute_type: [[8, 4, 2], [0.7, 0.2, 0.1]],
        __batch_type: [[4, 2, 1], [0.1, 0.8, 0.1]]
    }

    def __init__(self,
                 p_dist_core_types: List[float]):
        """
        Create a new compute core - the core type is allocated given the supplied probability distribution
        :param p_dist_core_types: a 1 by 3 probability distribution over core_types [gpu, cpu, batch]
        """
        self._core_type = self.core_types()[np.random.choice(np.arange(0, 3), p=p_dist_core_types)]
        _nc, _p_dist = self.__p_dist_type[self._core_type]
        self._core_count = _nc[np.random.choice(np.arange(0, 3), p=_p_dist)]

    @property
    def core_type(self):
        return deepcopy(self._core_type)

    @property
    def num_core(self):
        return deepcopy(self._core_count)

    @classmethod
    def gpu_mnemonic(cls) -> str:
        """
        The three character Mnemonic representing a GPU type core
        :return: Three character String Mnemonic for GPU
        """
        return deepcopy(cls.__gpu_type)

    @classmethod
    def compute_mnemonic(cls) -> str:
        """
        The three character Mnemonic representing a general compute type core
        :return: Three character String Mnemonic for general compute core
        """
        return deepcopy(cls.__compute_type)

    @classmethod
    def batch_mnemonic(cls) -> str:
        """
        The three character Mnemonic representing a batch (low end) type core
        :return: Three character String Mnemonic for batch (low end) type core
        """
        return deepcopy(cls.__batch_type)

    @classmethod
    def core_types(cls):
        return deepcopy([cls.__gpu_type,
                         cls.__compute_type,
                         cls.__batch_type
                         ]
                        )

    @classmethod
    def core_compute_equivalency(cls,
                                 required_compute: int,
                                 required_core_type: str,
                                 given_core_type: str) -> int:
        """
        What is the compute equivalency between the core asked for by a Load and the available core.
        :param required_compute: The raw compute being asked for in the required core type units
        :param required_core_type: The core type required by a Load
        :param given_core_type: The core type available from a Compute source
        :return: The required compute translated into equivalent units of given core type
        """
        mapping = required_core_type + given_core_type
        if mapping not in cls.__core_equivalency:
            raise ValueError('Core equivalency for [' + mapping + '] does not exist')
        return int((cls.__core_equivalency[mapping]) * required_compute)
