from datetime import datetime
from copy import deepcopy
from AIIntuition.journeys.journey5.load import Load
from AIIntuition.journeys.journey5.compute import Compute


class OutOfMemoryException(Exception):
    """
    Raised when an application cannot secure sufficient memory on the host it is running on.
    """

    def __init__(self,
                 load: Load,
                 compute: Compute):
        """
        Record and Out of Memory issue for Load on Compute
        :param load: The load that required more memory than was available & thus failed
        :param compute: The Compute that was unable to supply the required memory
        """
        self._event_time = time = datetime.now().strftime("%H:%M:%S")
        self._load = deepcopy(load)
        self._compute = deepcopy(compute)

    def __str__(self) -> str:
        return ''.join((self._event_time, ':',
                        'Load: ', self._load.id,
                        ' ran out of memory on compute: ',
                        self._compute.id
                        )
                       )

    @property
    def load(self) -> Load:
        return deepcopy(self._load)

    @property
    def compute(self) -> Compute:
        return deepcopy(self._compute)

    @property
    def event_time(self):
        return deepcopy(self._event_time)
