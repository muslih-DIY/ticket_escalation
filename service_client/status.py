from enum import Enum,auto

class TicketStatus(Enum):
    "different possible status of ticket"
    OPEN = auto()           # ticket not assigned any service level
    ASSIGNED = auto()       # ticket assigned a service level
    CLOSED = auto()         # ticket closed
    RESOLVED = auto()       # issue resolved
    INPROGRESS = auto()     # SL and SE Assigned Work in progress



class ServiceStatus(Enum):
    "different possible status of service _level"
    SE_NOT_ASSIGNED = auto()     # SE not assigned
    SE_ASSIGNED = auto()         # SE assigned
    COMPLETED = auto()
    ACCEPTED = auto()
    INPROGRESS = auto()
