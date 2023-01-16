from typing import Optional,Dict
from abc import ABC,abstractmethod
from datetime import datetime
from enum import Enum,auto
from dataclasses import dataclass,field
import inspect

class TICKET_STATUS(Enum):
    OPEN = auto()           # ticket not assigned any service level
    ASSIGNED = auto()       # ticket assigned a service level
    CLOSED = auto()         # ticket closed
    RESOLVED = auto()       # issue resolved 
    INPROGRESS = auto()


class Service_Status(Enum):
    UNASSIGNED = auto()
    COMPLETED = auto()
    ACCEPTED = auto()
    ASSIGNED = auto()
    INPROGRESS = auto()
    


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
    status:str
    service_level:str
    _service_level:'ServiceLevelIF' = field(init=False)
    _status:TICKET_STATUS = field(init=False)
    def __post__init__(self):
        self._service_level = ServiceLevelIF.get_service_class(self.service_level)
        self._status = TICKET_STATUS[self.status.upper()]

    def close(self):
        "initiate a closing proceedure with the customer"
    
    def re_open(self):
        "Re open a closed ticket"

    def assign_service(self):
        "Assign service level to the ticket manually other than escalate"


    def escalate(self):
        self.service_level.escalate()

    def complete(self):
        self.service_level.complete()

    def assign_engineer(self):
        "Assign engineer if not already assigned"
        self.service_level.assign_engineer()

    def reject(self):
        "Reject the ticket from the service level by engineer"
        self.service_level.reject()



class ServiceLevelIF(ABC):
    "Interface define different service level"
     
    __SERVICE_CLASS= {}

    _engineer_id:str
    _status:Service_Status
    _ticket:Ticket


    
    def service_register(klass):

        if inspect.isabstract(klass):
            print(f'WARNING: Skipping the Registration of {klass}: is an abstract class' )
        ServiceLevelIF.__SERVICE_CLASS[klass.__name__] = klass
        return klass

    def get_service_class(name:str)-> 'ServiceLevelIF':
        service_level = ServiceLevelIF.__SERVICE_CLASS.get(name,None)
        
        if not service_level:
            raise ValueError("service requested is not registered")
        
        return service_level
    
    def get_all_service_class()-> Dict[str,'ServiceLevelIF']:
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

    @abstractmethod
    def assign_engineer(self,engineer_id:str=None):
        "This will update the engineer in the service level"






