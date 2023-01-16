
import json
import os
from service_module.ticket import TicketStatus,Ticket


def test_open_ticket_close(get_ticket):
    "test creation of ticket"
    ticket_data = get_ticket['OPEN_TICKET']
    ticket = Ticket(**ticket_data)
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None
    assert ticket.customer_id
    assert ticket.product_id
