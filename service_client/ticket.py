from datetime import datetime
from dataclasses import dataclass,field
from .service_levels import ServiceLevelIF
from .carepack import care_pack,get_care_pack
from .status import TicketStatus,ServiceStatus
from .service_api import get_active_service_level

class ServiceLevelError(Exception):
    "Raise any service level exception"


@dataclass
class Ticket():
    "This class deal the ticket escalation"
    ticket_id:str
    customer_id:str
    product_id:str
    complaint_type:str   
    booked_on:datetime
    re_opened_on:datetime
    last_update:datetime
    closed_on:datetime
    resolved_on:datetime
    priority:int
    ticket_status:str
    service_level_id:int
    service_level_name:str
    description:str
    care_pack_id:str

    _service_level:'ServiceLevelIF' = field(init=False)
    _status:TicketStatus = field(init=False)
    _care_pack:care_pack = field(init=False)


    def __post_init__(self):
        self._status = TicketStatus[self.ticket_status.upper()]
        self._care_pack = get_care_pack(self.care_pack_id)
        self._service_level= get_active_service_level(self.ticket_id)


            

    @property
    def service_level(self):
        "return the service_level object"
        return self._service_level

    @service_level.setter
    def service_level(self,service_level:'ServiceLevelIF'):
        "update the service_level"
        self._service_level = service_level
        self._service_level.ticket = self
        self._status = TicketStatus.ASSIGNED
        self._service_level.status = ServiceStatus.SE_NOT_ASSIGNED

    @property
    def status(self):
        "return the status of ticket"
        return self._status

    @status.setter
    def status(self,status:TicketStatus):
        self._status = status

    def close(self):
        "initiate a closing proceedure with the customer"

    def re_open(self):
        "Re open a closed ticket"


    def escalate(self):
        "escalate"
        if not self._service_level:
            raise ServiceLevelError('Cannot escalate ticket have no service level assigned(OPEN ticket)')
        next_service = self._service_level.escalate()
        self.service_level = next_service

    def complete(self):
        "complete by SE"
        self._service_level.complete()

    def assign_engineer(self):
        "Assign engineer if not already assigned"
        self.service_level.assign_engineer()

    def reject(self):
        "Reject the ticket from the service level by engineer"
        self.service_level.reject()


