import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert 'Comprar pan' in response.get_data(as_text=True)

def test_create_task(client):
    response = client.post('/tasks', json={'title': 'Aprender testing'})
    assert response.status_code == 201
    assert 'Aprender testing' in response.get_data(as_text=True)

def test_create_task_without_title(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'El título es necesario'

def test_task_list_updates(client):
    response = client.post('/tasks', json={'title': 'Otra nueva tarea'})
    assert response.status_code == 201

    response = client.get('/tasks')
    assert 'Otra nueva tarea' in response.get_data(as_text=True)
