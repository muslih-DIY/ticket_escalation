
import json
import os
from service_module.ticket import Ticket,TICKET_STATUS



def test_open_ticket_close(get_ticket):
    ticket_data = get_ticket['OPEN_TICKET']
    Ticket()
    assert ticket_data
