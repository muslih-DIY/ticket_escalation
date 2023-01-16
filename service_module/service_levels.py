from abc import abstractmethod
from enum import Enum,auto
from typing import Optional,Dict
from .ticket import ServiceLevelIF


    
class OnlineServiceIF(ServiceLevelIF):

    @property
    def service_type(self):
        return 'Online'
    
    
class OnsiteServiceIF(ServiceLevelIF):

    @property
    def service_type(self):
        return 'Onsite'
    

@ServiceLevelIF.service_register
class Online_L0(OnlineServiceIF):

    @property
    def service_sub_type(self):
        return 'L0'

    def escalate(self):
        sl = ServiceLevelIF.get_service_class('Online_L0')
        return sl
