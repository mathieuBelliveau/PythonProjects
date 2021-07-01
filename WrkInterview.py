from datetime import datetime
from decimal import Decimal
from enum import IntEnum
import functools
from pprint import pprint
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)

# Some types that are used by the function. No bugs in these.

CountryID = str


class JobType(IntEnum):
    NORMAL = 1
    VERIFICATION = 2


class TypeInfo(NamedTuple):
    job_type: JobType
    job_count: int
    lower_base_value: Decimal
    upper_base_value: Decimal


class JobGroup(NamedTuple):
    id: int
    name: str
    can_complete: bool
    type_info: List[TypeInfo]


# There are 4 bugs in the `display_job_groups` function.
# 1 is an easy bug. The other 3 are logic errors that will not raise any exceptions, but
# will produce invalid output.
def display_job_groups(job_groups: List[JobGroup],
                       country_id: CountryID,
                       now: datetime = datetime.now()) -> List[Dict[str, Any]]:
    """Converts a Job Group to a template format. Adjusts for COL."""
    scale_payout = functools.partial(get_payout,
                                     country_id=country_id,
                                     as_of=now)
    result = []
    for group in job_groups:#goes through the job_groups list and grabs first three vars
        group_view: Dict[str, Any] = {
            "gid": group.id,
            "name": group.name,
            "qualified": group.can_complete,
        }
        
        
        if group.can_complete:#Error 1
          #result.append(group_view)
          for type_info in group.type_info:#go through the group item's TypeInfo
              if type_info.job_type == JobType.NORMAL: #if it's a normal job
                  group_view["count"] = type_info.job_count
                  group_view["upper_worth"] = scale_payout(type_info.upper_base_value)
                  group_view["lower_worth"] = scale_payout(type_info.lower_base_value)
              elif type_info.job_type == JobType.VERIFICATION:#verifying
                  group_view["vcount"] = type_info.job_count#verification count
                  group_view["upper_vworth"] = scale_payout(type_info.upper_base_value)#Error 3
                  group_view["lower_vworth"] = scale_payout(type_info.lower_base_value)

          result.append(group_view)

    return result#error 2

# Stubs for the functions used by display_job_groups. No bugs here.
def get_payout(base_value: Decimal, country_id: CountryID, as_of: datetime) -> Decimal:
    return base_value * 100


# Actual tests
job_groups = [
    JobGroup(id=2,
             name="job 2",
             can_complete=True,
             type_info=[
                TypeInfo(job_type=JobType.NORMAL,
                         job_count=12,
                         upper_base_value=Decimal(6),
                         lower_base_value=Decimal(5)),
                TypeInfo(job_type=JobType.VERIFICATION,
                         job_count=7,
                         upper_base_value=Decimal(7),
                         lower_base_value=Decimal(6)),
             ]),
    JobGroup(id=7,
             name="job 7",
             can_complete=False,
             type_info=[
                TypeInfo(job_type=JobType.NORMAL,
                         job_count=2,
                         upper_base_value=Decimal(16),
                         lower_base_value=Decimal(15)),
                TypeInfo(job_type=JobType.VERIFICATION,
                         job_count=5,
                         upper_base_value=Decimal(22),
                         lower_base_value=Decimal(20)),
             ]),
]
pprint(display_job_groups(job_groups, country_id="JP"))