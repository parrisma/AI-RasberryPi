from random import seed
from copy import deepcopy
import numpy as np


class DataCenter:
    seed(42)
    __name_i = 0
    __p_dist_i = 1
    __compute_cost_i = 2
    __performance_tier_i = 3
    __region_i = 4

    __top_tier_mnemonic = 'TOP'
    __low_tier_mnemonic = 'LOW'
    __mid_tier_mnemonic = 'MID'

    __rgn_europe = 'Europe'
    __rgn_north_america = 'North America'
    __rgn_asia_pac = 'Asia Pacific'

    __countries = {
        # Mnemonic (key) : name, probability of host in region, compute cost, tier, region
        "USA": ['United States', 0.2, 0.6, __mid_tier_mnemonic, __rgn_north_america],
        "GBR": ['Great Britain', 0.2, 0.6, __mid_tier_mnemonic, __rgn_europe],
        "AUS": ['Australia', 0.1, 0.95, __low_tier_mnemonic, __rgn_asia_pac],
        "POL": ['Poland', 0.05, 0.8, __low_tier_mnemonic, __rgn_europe],
        "ISL": ['Iceland', 0.4, 0.5, __top_tier_mnemonic, __rgn_europe],
        "HKG": ['Hong Kong', 0.05, 0.95, __low_tier_mnemonic, __rgn_asia_pac]
    }

    __mnemonics = deepcopy(list(__countries.keys()))
    __sorted_mnemonics = sorted(__mnemonics)  # return a copy
    __p_dist = list(map(lambda x: x[1], __countries.values()))

    def __init__(self):
        """
        A country selected according to the country selection probability distribution
        """
        self.mnemonic = DataCenter.__mnemonics[np.random.choice(np.arange(0, 6), p=DataCenter.__p_dist)]

    @classmethod
    def country_mnemonics(cls):
        """
        The list of Country Mnemonics
        :return: An alphabetical list of three character country mnemonics
        """
        return cls.__sorted_mnemonics

    @property
    def country_mnemonic(self):
        """
        The country Mnemonic
        :return: the three character Mnemonic for the country
        """
        return self.mnemonic

    @property
    def country_name(self):
        """
        The long name of the country
        :return: A string of the long name of the country
        """
        return (self.__countries[self.mnemonic])[self.__name_i]

    @property
    def compute_cost(self):
        """
        The compute cost for country in range 0 to 1
        :return: A decimal in range 0 to 1 - where 1 = max unit compute cost
        """
        return (self.__countries[self.mnemonic])[self.__compute_cost_i]

    @property
    def performance_tier(self):
        """
        The performance tier of the country Top, Mid, Low
        :return: A String Mnemonic of the performance tier
        """
        return (self.__countries[self.mnemonic])[self.__performance_tier_i]

    @property
    def region(self):
        """
        The performance tier of the country Top, Mid, Low
        :return: A String Mnemonic of the performance tier
        """
        return (self.__countries[self.mnemonic])[self.__region_i]

    @classmethod
    def perf_tier_mnemonic_top(cls):
        return cls.__top_tier_mnemonic

    @classmethod
    def perf_tier_mnemonic_mid(cls):
        return cls.__mid_tier_mnemonic

    @classmethod
    def perf_tier_mnemonic_low(cls):
        return cls.__low_tier_mnemonic

    def __str__(self):
        """
        Details of the Country as string
        :return: A String containing all details of the country.
        """
        return ''.join(
            (self.country_mnemonic, ':',
             self.country_name, '-',
             'Cost:', str(self.compute_cost), '-',
             self.performance_tier, '-',
             self.region
             )
        )


if __name__ == "__main__":
    for i in range(0, 100):
        c = DataCenter()
        print(c)
