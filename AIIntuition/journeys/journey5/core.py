from copy import deepcopy


class Core:
    __gpu_type = 'GPU'
    __compute_type = 'CPU'
    __batch_type = 'BAT'

    @classmethod
    def gpu_mnemonic(cls):
        return deepcopy(cls.__gpu_type)

    @classmethod
    def compute_mnemonic(cls):
        return deepcopy(cls.__compute_type)

    @classmethod
    def batch_mnemonic(cls):
        return deepcopy(cls.__batch_type)

    @classmethod
    def core_types(cls):
        return deepcopy([cls.__gpu_type,
                         cls.__compute_type,
                         cls.__batch_type
                         ]
                        )
