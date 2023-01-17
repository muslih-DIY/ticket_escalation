import logging
import json
import os
from service_client.ticket import Ticket,TICKET_STATUS

TEST_DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test','data')

    

def get_test_data(filename):
    filepath = os.path.join(TEST_DATA_FOLDER,filename)
    
    with open(filepath) as jsonfile:
        data = json.load(jsonfile)
    return data
    
def get_ticket()->dict:
    return get_test_data('tickets.json')


class TestTicket():

    def open_ticket_close(self):
        ticket_data = get_ticket()['OPEN_TICKET']
        ticket = Ticket(**ticket_data)
        print(ticket.product_id)
        print(ticket.ticket_id)
        print(ticket.customer_id)
        print(ticket.status)
        print(ticket.service_level)




if __name__=='__main__':
    test = TestTicket()
    test.open_ticket_close()