
import json
import os
from service_client.ticket import (
    Ticket,ServiceLevelIF,
    TicketStatus,ServiceStatus,
    ServiceLevelError
    )
from service_client.service_engineer import (
    ServiceEngineerAllocation,ServiceEngineerReport)
from service_client import service_levels as sl
import pytest
from pytest import MonkeyPatch
from service_client import service_api


def test_open_ticket(get_tickets,monkeypatch):
    "test creation of ticket"
    get_ticket_from_test_dir = lambda x : get_tickets['OPEN_TICKET']

    monkeypatch.setattr(service_api,"get_ticket_details",get_ticket_from_test_dir)
    # ticket_data = get_tickets['OPEN_TICKET']
    # ticket = Ticket(**ticket_data)
    ticket = service_api.get_ticket('123')
    print(ticket)
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None
    assert ticket.customer_id
    assert ticket.product_id

def test_assign_service_level_to_open_ticket(get_tickets,monkeypatch):
    "open ticket escalation"
    get_ticket_from_test_dir = lambda x : get_tickets['OPEN_TICKET']

    monkeypatch.setattr(service_api,"get_ticket_details",get_ticket_from_test_dir)

    ticket = service_api.get_ticket('123')
    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None
    ticket.service_level = ServiceLevelIF.get_a_new_service_level('l1online',ticket.ticket_id)
    assert isinstance(ticket.service_level,sl.L1Online)
    assert ticket.status == TicketStatus.ASSIGNED
    assert ticket.service_level.status == ServiceStatus.SE_NOT_ASSIGNED
    ticket.service_level.assign_engineer()
    assert ticket.service_level.status == ServiceStatus.SE_ASSIGNED

def test_escalation_of_a_open_ticket(get_tickets,monkeypatch):
    "Cannot escalate a OPEN ticket/ no service _level assigned"

    get_ticket_from_test_dir = lambda x : get_tickets['OPEN_TICKET']
    monkeypatch.setattr(service_api,"get_ticket_details",get_ticket_from_test_dir)
    ticket = service_api.get_ticket('123')

    assert ticket.status == TicketStatus.OPEN
    assert ticket.service_level is None

    with pytest.raises(ServiceLevelError):
        ticket.escalate()

def test_assigned_ticket(get_tickets,get_service_level,monkeypatch):
    "get and validate a assigned ticket"
    get_ticket_from_test_dir = lambda x : get_tickets['LO_ONLINE']
    get_service_details_test_dir = lambda id : get_service_level[id]
    monkeypatch.setattr(service_api,"get_ticket_details",get_ticket_from_test_dir)
    monkeypatch.setattr(service_api,"get_service_details",get_service_details_test_dir)
    ticket = service_api.get_ticket('123')    


def test_escalation_of_assigned_ticket(get_tickets,get_service_level,monkeypatch):
    "Cannot escalate a assigned ticket/ no service _level assigned"
    # ticket_data = get_tickets['LO_ONLINE']
    # ticket = Ticket(**ticket_data)
    get_ticket_from_test_dir = lambda x : get_tickets['LO_ONLINE']
    get_service_details_test_dir = lambda id : get_service_level[id]
    monkeypatch.setattr(service_api,"get_ticket_details",get_ticket_from_test_dir)
    monkeypatch.setattr(service_api,"get_service_details",get_service_details_test_dir)
    ticket = service_api.get_ticket('123')
    assert ticket.status == TicketStatus.ASSIGNED
    assert isinstance(ticket.service_level,sl.L0Online)
    ticket.escalate()
    assert isinstance(ticket.service_level,sl.L1Online)
    assert ticket.status == TicketStatus.ASSIGNED
    assert ticket.service_level.status == ServiceStatus.SE_NOT_ASSIGNED