from copy import deepcopy


class SystemTime:
    """
    Time, day of year and GMT hour of day.
    """

    def __init__(self,
                 day_of_year: int,
                 hour_of_day: int):
        self._day_of_year = day_of_year
        self._hour_of_day = hour_of_day
        return

    @property
    def day_of_year(self):
        return deepcopy(self._day_of_year)

    @property
    def hour_of_day(self):
        return deepcopy(self._hour_of_day)
