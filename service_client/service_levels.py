from abc import abstractmethod,ABC
from dataclasses import dataclass,field
from datetime import datetime
from typing import Dict
import inspect
from .service_engineer import ServiceEngineerAllocation,ServiceEngineerReport
from .status import ServiceStatus

@dataclass
class ServiceLevelIF(ABC):
    "Interface define different service level"

    __SERVICE_CLASS = {}

    id:str
    ticket_id:str
    started_on:datetime
    updated_on:datetime
    complete_on:datetime
    service_level_status:str
    se_allocation_id:str
    se_allocated:str

    _service_engineer:ServiceEngineerAllocation = field(init=False,default=None)
    _status:ServiceStatus = field(init=False,default=None)
    __BASE_SERVICE:'ServiceLevelIF' = field(init=False)
    
    @property
    def status(self):
        "get status"
        return self._status

    @status.setter
    def status(self,status:ServiceStatus):
        "set status"
        self._status = status


    @property
    def service_engineer(self):
        return self._service_engineers
    

    @staticmethod
    def service_register(klass):
        "decorator:Register all the concrete classes under the service_level interface"
        if inspect.isabstract(klass):
            print(f'WARNING: Skipping the Registration of {klass}: is an abstract class' )
        ServiceLevelIF.__SERVICE_CLASS[klass.__name__.lower()] = klass
        return klass

    @staticmethod
    def base_service_register(klass):
        "decorator:Regis"
        if inspect.isabstract(klass):
            print(f'WARNING: Skipping the Registration of {klass}: is an abstract class' )
        ServiceLevelIF.__SERVICE_CLASS[klass.__name__.lower()] = klass
        ServiceLevelIF.__BASE_SERVICE = klass
        return klass

    @staticmethod
    def get_service_class(name:str)-> 'ServiceLevelIF':
        " get service level classes registered to the service_level interface by giving thier name"
        slname = name.lower()
        service_level = ServiceLevelIF.__SERVICE_CLASS.get(slname,None)
        if not service_level:
            raise ValueError("service requested is not registered")

        return service_level

    @staticmethod
    def get_all_service_class()-> Dict[str,'ServiceLevelIF']:
        "Return all dictionary of the service under the service level interface"

        return ServiceLevelIF.__SERVICE_CLASS

    @staticmethod
    def get_base_service()-> 'ServiceLevelIF':
        "Return base service for the OPEN ticket"

        return ServiceLevelIF.__BASE_SERVICE

    def get_engineer(self):
        "This will return an engineer from the service level"
        self.get_se()


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


 
    def assign_engineer(self,s_e:'ServiceEngineerAllocation'= None):
        "This will update the engineer in the service level"
        if not s_e or not isinstance(s_e,ServiceEngineerAllocation):
            s_e = self.get_engineer()
        self._service_engineer = s_e
        self._status = ServiceStatus.SE_ASSIGNED


class OnlineServiceIF(ServiceLevelIF):
    "Online support abstract"

    @property
    def service_type(self):
        return 'Online'

class OnsiteServiceIF(ServiceLevelIF):
    "Onsite support abstract "

    @property
    def service_type(self):
        return 'Onsite'

@ServiceLevelIF.base_service_register
@dataclass
class L0Online(OnlineServiceIF):
    "LO online support "
    @property
    def service_sub_type(self):
        return 'L0'

    def escalate(self):
        next_service:'L1Online' = ServiceLevelIF.get_service_class('L1Online')
        return next_service(
                    started_on=datetime.now(),
                    updated_on=datetime.now(),
                    complete_on = None,
                    service_level_status='SE_NOT_ASSIGNED',
                    se_allocation_id = None,
                    se_allocated = None
        )

    def complete(self):
        "completed the issue"

    def get_engineer(self):
        "return an engineer id"


@ServiceLevelIF.service_register
@dataclass
class L1Online(OnlineServiceIF):
    "L1 online support "
    @property
    def service_sub_type(self):
        return 'L1'

    def escalate(self):
        next_service = ServiceLevelIF.get_service_class('L2Online')
        return next_service()

    def complete(self):
        "completed the issue"

    def get_engineer(self):
        "return an engineer id"

