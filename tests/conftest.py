import pytest
import json
import pathlib
import os

TEST_DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data')

    

def get_test_data(filename)->dict:
    filepath = os.path.join(TEST_DATA_FOLDER,filename)
    
    with open(filepath) as jsonfile:
        data = json.load(jsonfile)
    return data

@pytest.fixture    
def get_ticket()->dict:
    data:dict = get_test_data('tickets.json')
    return data