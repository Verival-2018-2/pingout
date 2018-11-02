from uuid import uuid4
import json
from .schemas import assert_valid_schema, get_pingout_schema, get_wrong_pingout_schema, \
                     create_file_ping, failure_create_file_ping
from datetime import datetime, timedelta
import sys                     
                     


def test_return_200_on_root(client):
    """ Return status code 200 on root url"""
    response = client.get('/')
    assert response.status_code == 200


def test_create_pingout(client):
    """ Return status code 200 on root url"""
    response = client.post('/create-pingout')
    assert response.status_code == 201    


def test_ping(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    response = client.post('/' + post_data['uuid'] + '/ping')
    assert response.status_code == 201


def test_failure_ping(client):
    response = client.post('/' + "1234" + "/ping" )
    get_data = json.loads(response.data)    

    assert response.status_code == 400
    assert assert_valid_schema(get_data, get_wrong_pingout_schema) == None


def test_get_pings(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    response = client.get('/' + post_data['uuid'] )
    get_data = json.loads(response.data)    

    assert response.status_code == 200
    assert assert_valid_schema(get_data, get_pingout_schema) == None


def test_failure_get_pings(client):
    response = client.get('/' + '1234' )
    get_data = json.loads(response.data)    

    assert response.status_code == 400
    assert assert_valid_schema(get_data, get_wrong_pingout_schema) == None


def test_export_range_csv(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    ping = client.post('/' + post_data['uuid'] + '/ping')
    initial_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    final_date = datetime.today().strftime('%Y-%m-%d')
    response = client.get('/' + post_data['uuid'] + '/filter?initial_date=' + initial_date + '&final_date=' + final_date)
    get_data = json.loads(response.data)

    assert response.status_code == 200
    assert assert_valid_schema(get_data, create_file_ping) == None

def test_failure_export_range_csv(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    initial_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    final_date = datetime.today().strftime('%Y-%m-%d')
    response = client.get('/' + post_data['uuid'] + '/filter?initial_date=' + initial_date + '&final_date=' + final_date)
    get_data = json.loads(response.data)

    assert response.status_code == 400
    assert assert_valid_schema(get_data, failure_create_file_ping) == None


def test_export_specific_csv(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    date = datetime.today().strftime('%Y-%m-%d')    

    ping = client.post('/' + post_data['uuid'] + '/ping')
    response = client.get('/' + post_data['uuid'] + '/filter_specific?date=' + date)
    get_data = json.loads(response.data)

    assert response.status_code == 200
    assert assert_valid_schema(get_data, create_file_ping) == None

def test_failure_export_specific_csv(client):
    res = client.post('/create-pingout')
    post_data = json.loads(res.data)
    date = datetime.today().strftime('%Y-%m-%d')
    response = client.get('/' + post_data['uuid'] + '/filter_specific?date=' + date)
    get_data = json.loads(response.data)

    assert response.status_code == 400
    assert assert_valid_schema(get_data, failure_create_file_ping) == None