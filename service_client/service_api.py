"""
interface with the service apis

create ticket
update ticket
select ticket

select service level engineers


"""
from datetime import datetime
import requests
from .service_levels import ServiceLevelIF

def get_ticket_details(ticket_id:str)-> dict:
    "get information of ticket from service server api"
    return {}


def get_ticket(ticket_id:str):
    "Return a ticket object"
    from .ticket import Ticket
    ticket_details = get_ticket_details(ticket_id)
    return Ticket(**ticket_details)





def get_service_details(ticket_id):
    return {
        'service_name':"L0Online",
        "id":"SL123",
        "ticket_id":'T321',
        "started_on":datetime.now(),
        "updated_on":datetime.now(),
        "complete_on":datetime.now(),
        "service_level_status":"",
        "se_allocation_id":"SE342",
        "se_allocated":'SA3213'
    }

def get_active_service_level(service_id:str)-> ServiceLevelIF:
    "Return the active service_status_of the ticket"
    service_level_details = get_service_details(service_id)
    service_name = service_level_details.pop('service_level_name')
    return ServiceLevelIF.get_service_class(service_name)(**service_level_details)
    