from typing import Tuple
from collections.abc import Iterable
from AIIntuition.journeys.journey5.datacenter import DataCenter
from AIIntuition.journeys.journey5.host import Host
from AIIntuition.journeys.journey5.app import App
from AIIntuition.journeys.journey5.infrnditer import InfRndIter
from AIIntuition.journeys.journey5.policy import Policy
from AIIntuition.journeys.journey5.seqpolicy import SequentialPolicy
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
        num_host = 2
        num_app = 1
        num_run_days = 3

        dc = DataCenter(DataCenter.CountryCode.ICELAND)  # Create a single DC Only.

        fhp1 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=2)), mem=16)
        h1 = Host(dc, fhp1)  # Create first low spec host

        fhp2 = FixedHostProfile(core=Core(FixedCoreProfile(core_type=CPUType.GENERAL, core_count=16)), mem=256)
        h2 = Host(dc, fhp2)  # Create another high spec host

        policy = SequentialPolicy(h1, h2)

        ftp = FixedTaskProfile(max_mem=4,
                               mem_vol=0,
                               cpu_type=CPUType.GENERAL,
                               load_factor=5,
                               load_profile=Task.LoadProfile.SAW_TOOTH,
                               run_time=30)

        app1 = App(ftp)  # Create a new app in line with task policy
        policy.select_optimal_compute(app1).associate_task(app1)

        compute_iter = InfRndIter(Host.all_hosts())

        return num_host, num_app, policy, compute_iter, num_run_days
