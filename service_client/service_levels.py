from abc import abstractmethod
from enum import Enum,auto
from typing import Optional,Dict
from .ticket import ServiceLevelIF,ServiceEngineer

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

@ServiceLevelIF.service_register
class Onlinel0(OnlineServiceIF):
    "LO online support "
    @property
    def service_sub_type(self):
        return 'L0'

    def escalate(self):
        next_service = ServiceLevelIF.get_service_class('Onlinel0')
        self._ticket.service_level = next_service

    def complete(self):
        "completed the issue"

    def get_engineer(self):
        "return an engineer id"

    # def assign_engineer(self,se:ServiceEngineer):
    #     "assign"
        

@ServiceLevelIF.service_register
class Onlinel1(OnlineServiceIF):
    "L1 online support "
    @property
    def service_sub_type(self):
        return 'L1'

    def escalate(self):
        next_service = ServiceLevelIF.get_service_class('Onlinel2')
        self._ticket.service_level = next_service

    def complete(self):
        "completed the issue"

    def get_engineer(self):
        "return an engineer id"

    # def assign_engineer(self,se:ServiceEngineer):
    #     self._SE = se
        