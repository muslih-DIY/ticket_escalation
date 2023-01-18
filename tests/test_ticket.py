
import json
import os
from service_client.ticket import (
    Ticket,ServiceLevelIF,
    TicketStatus,ServiceStatus,
    ServiceLevelError
    )
from service_client import service_levels as sl
import pytest

def test_open_ticket_close(get_tickets):
    "test creation of ticket"
    ticket_data = get_tickets['OPEN_TICKET']
    ticket = Ticket(**ticket_data)
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None
    assert ticket.customer_id
    assert ticket.product_id

def test_assign_service_level_to_open_ticket(get_tickets):
    "open ticket escalation"
    ticket_data = get_tickets['OPEN_TICKET']
    ticket = Ticket(**ticket_data)
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None
    ticket.service_level = ServiceLevelIF.get_service_class('onlineL1')()
    assert isinstance(ticket.service_level,sl.Onlinel1)
    assert ticket.status == TicketStatus.ASSIGNED
    assert ticket.service_level.status == ServiceStatus.SE_NOT_ASSIGNED
    ticket.service_level.assign_engineer()
    assert ticket.service_level.status == ServiceStatus.SE_ASSIGNED

def test_escalation_of_a_open_ticket(get_tickets):
    "Cannot escalate a OPEN ticket/ no service _level assigned"
    ticket_data = get_tickets['OPEN_TICKET']
    ticket = Ticket(**ticket_data)
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None

    with pytest.raises(ServiceLevelError):
        ticket.escalate()
