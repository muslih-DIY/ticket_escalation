
from dataclasses import dataclass

@dataclass
class care_pack:
    id:str
    active:bool
    total_remote_support:int
    availed_remote_support:int
    total_onsite_support:int
    availed_onsite_spport:int


def get_care_pack(pack_id:str)->care_pack:

    return care_pack(
        id=pack_id,
        active=True,
        total_onsite_support=10,
        total_remote_support=20,
        availed_onsite_spport=1,
        availed_remote_support=5
    )

