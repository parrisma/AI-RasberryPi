from datetime import datetime
from copy import deepcopy


class AppOutOfMemoryException(Exception):
    """
    Raised when an application cannot secure sufficient memory on the host it is running on.
    """

    def __init__(self,
                 app_id: str):
        self.__event_time = time = datetime.now().strftime("%H:%M:%S")
        self.__app = app_id

    def __str__(self) -> str:
        return ''.join((self.event_time, ':',
                        self.application,
                        ' - ran out of memory'
                        )
                       )

    @property
    def application(self) -> str:
        return deepcopy(self.__app)

    @property
    def event_time(self):
        return deepcopy(self.__event_time)
