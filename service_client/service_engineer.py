
from dataclasses import dataclass,field
from datetime import datetime

@dataclass
class ServiceEngineerAllocation:
    id:str
    service_engineer_id:str    
    ticket_id:str
    allocated_on:datetime
    accepted_on:str
    allocation_status:str
    completed_on:datetime
    report_id:str = None

    _report:'ServiceEngineerReport' = field(init=False,default=None)    

@dataclass
class ServiceEngineerReport:
    id:str
    reported_on:datetime
    updated_on:datetime
    ticket_id:str
    service_level_id:str
    se_allocation_id:str
    issue_identified:str = ''
    solutions:str = ''
    reccomendation:str = ''


def get_se_detail(service_type,service_sub_type,product_id,customer_id,complaint_label)-> dict:
    "get the information of service engineers"
    return 
