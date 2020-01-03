from typing import Tuple
from collections.abc import Iterable
from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.app import App
from AIIntuition.journeys.journey5.infrnditer import InfRndIter
from AIIntuition.journeys.journey5.policy import Policy
from AIIntuition.journeys.journey5.randompolicy import RandomPolicy
from AIIntuition.journeys.journey5.case import Case
from AIIntuition.journeys.journey5.fixedtaskprofile import FixedTaskProfile
from AIIntuition.journeys.journey5.fixedhostprofile import FixedHostProfile
from AIIntuition.journeys.journey5.fixedcoreprofile import FixedCoreProfile
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.core import Core


class OneDCCase(Case):
    """
    In the test we create a single data center
    created randomly and if applicable according to the defined probability distributions of the type
    """

    @classmethod
    def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :return:
            The number of hosts created
            The number of applications created
            The Host Selection Policy used by the scheduler
            The Host iterator used by the scheduler
            The number of 24 hour periods to run the schedule simulation for
        """
        policy = RandomPolicy()  # Host selected at random

        dc = DataCenter(DataCenter.CountryCode.ICELAND)  # Create a single DC Only.
        fhp = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=2)), mem=16)
        _ = Host(dc, fhp)  # Create a single host

        ftp = FixedTaskProfile(max_mem=4,
                               mem_vol=0,
                               cpu_type=CPUType.GENERAL,
                               load_profile=Task.LoadProfile.SAW_TOOTH,
                               run_time=72)

        for i in range(0, 1):
            App(ftp)  # Create a new random app

        app_list = App.all_tasks()
        for app in app_list:
            hst = policy.select_optimal_compute(app)
            hst.associate_task(app)

        compute_iter = InfRndIter(Host.all_hosts())

        return 1, 1, policy, compute_iter, 5
