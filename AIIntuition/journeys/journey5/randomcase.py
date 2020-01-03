from typing import Tuple
from collections.abc import Iterable
from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.app import App
from AIIntuition.journeys.journey5.infrnditer import InfRndIter
from AIIntuition.journeys.journey5.policy import Policy
from AIIntuition.journeys.journey5.randompolicy import RandomPolicy
from AIIntuition.journeys.journey5.case import Case


class RandomCase(Case):
    """
    This class sets up the data centres, Hosts & Apps for a full scale case, where all items are
    created randomly and if applicable according to the defined probability distributions of the type
    """

    @classmethod
    def set_up(cls,
               num_hosts: int,
               num_apps: int) -> Tuple[Policy, Iterable]:
        """
        Set-up a Random environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :param num_hosts: The number of Hosts to create in the environment
        :param num_apps:  The number of App to create in the environment.
        :return: The Host Selection Policy used by the scheduler, The Host iterator used by the scheduler
        """
        policy = RandomPolicy()  # Host selected at random

        for country_code in DataCenter.country_codes():
            _ = DataCenter(country_code)

        for i in range(0, num_hosts):
            dc = DataCenter.next_data_center_by_p_dist()  # Pick a data centre according to DC distribution
            _ = Host(dc)  # Create a Host in the chosen Data Centre

        for i in range(0, num_apps):
            App()  # Create a new random app

        app_list = App.all_tasks()
        for app in app_list:
            hst = policy.select_optimal_compute(app)
            hst.associate_task(app)

        compute_iter = InfRndIter(Host.all_hosts())

        return policy, compute_iter
