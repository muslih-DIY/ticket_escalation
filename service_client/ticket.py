from typing import Dict
from abc import ABC,abstractmethod
from datetime import datetime
from enum import Enum,auto
from dataclasses import dataclass,field
import inspect

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
    remote_support_count:int
    onsite_support_count:int
    current_status:str
    service_level_name:str = None
    _service_level:'ServiceLevelIF' = field(init=False)
    _status:TicketStatus = field(init=False)

    def __post_init__(self):
        try:
            service_level = ServiceLevelIF.get_service_class(self.service_level_name)
            self._service_level = service_level()
        except ValueError:
            self._service_level= None         
        self._status = TicketStatus[self.current_status.upper()]

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

    def assign_service(self):
        "Assign service level to the ticket manually other than escalate"


    def escalate(self):
        "escalate"
        if not self._service_level:
            raise ServiceLevelError('Cannot escalate ticket have no service level assigned(OPEN ticket)')
        self._service_level.escalate()

    def complete(self):
        "complete by SE"
        self._service_level.complete()

    def assign_engineer(self):
        "Assign engineer if not already assigned"
        self.service_level.assign_engineer()

    def reject(self):
        "Reject the ticket from the service level by engineer"
        self.service_level.reject()


class ServiceLevelIF(ABC):
    "Interface define different service level"

    __SERVICE_CLASS= {}

    _SE:'ServiceEngineer' = None
    _status:ServiceStatus = None
    _ticket:Ticket  = None

    @property
    def status(self):
        "get status"
        return self._status

    @status.setter
    def status(self,status:ServiceStatus):
        "set status"
        self._status = status

    @property
    def ticket(self):
        "get ticket"
        return self._ticket

    @ticket.setter
    def ticket(self,ticket:Ticket):
        "set the protected ticket attribute"
        self._ticket = ticket

    @property
    def service_engineer(self):
        return self._SE
    

    @staticmethod
    def service_register(klass):
        "decorator:Register all the concrete classes under the service_level interface"
        if inspect.isabstract(klass):
            print(f'WARNING: Skipping the Registration of {klass}: is an abstract class' )
        ServiceLevelIF.__SERVICE_CLASS[klass.__name__.lower()] = klass
        return klass

    @staticmethod
    def get_service_class(name:str)-> 'ServiceLevelIF':
        " get service level classes registered to the service_level interface by giving thier name"

        service_level = ServiceLevelIF.__SERVICE_CLASS.get(name.lower(),None)

        if not service_level:
            raise ValueError("service requested is not registered")

        return service_level

    @staticmethod
    def get_all_service_class()-> Dict[str,'ServiceLevelIF']:
        "Return all dictionary of the service under the service level interface"

        return ServiceLevelIF.__SERVICE_CLASS


    @property
    @abstractmethod
    def service_type(self):
        "Type of the support onsite online admin"

    @property
    @abstractmethod
    def service_sub_type(self):
        "sub type like LO L1"

    @abstractmethod
    def escalate(self):
        "The escalation of a ticket from it current level"

    @abstractmethod
    def complete(self):
        "This change the state of a ticket at the same service level to complete"

    @abstractmethod
    def get_engineer(self):
        "This will return an engineer from the service level"
        return ServiceEngineer('SE1')


    def assign_engineer(self,s_e:'ServiceEngineer'= None):
        "This will update the engineer in the service level"
        if not s_e or not isinstance(s_e,ServiceEngineer):
            s_e = self.get_engineer()
        self._SE = s_e
        self._status = ServiceStatus.SE_ASSIGNED

@dataclass
class ServiceEngineer:
    id:str
