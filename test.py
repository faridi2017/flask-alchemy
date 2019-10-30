import pytest
from run import app

def test_example(client):
    response = client.get("http://192.168.2.54:5000/emp")
    print(response)
    assert response.status_code == 200
