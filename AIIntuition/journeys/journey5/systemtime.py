from copy import deepcopy
from AIIntuition.journeys.journey5.globsym import GlobSym


class SystemTime:
    """
    Time, day of year and hour of day.
    """

    def __init__(self,
                 day_of_year: int,
                 hour_of_day: int):
        self._day_of_year = day_of_year
        self._hour_of_day = hour_of_day
        return

    def as_str(self,
               as_feature: bool):
        if as_feature:
            return str(self.day_of_year) + GlobSym.separator() + str(self.hour_of_day)
        return 'Sys Day: ' + str(self.day_of_year) + ' Sys Hour: ' + str(self.hour_of_day)

    @property
    def day_of_year(self):
        return deepcopy(self._day_of_year)

    @property
    def hour_of_day(self):
        return deepcopy(self._hour_of_day)
