import requests

BASE_URL = 'http://127.0.0.1:5000'
tasks = []


def test_create_task():
    new_task = {
        'title': 'Nova tarefa',
        'description': 'Descrição da nova tarefa'
    }
    response = requests.post(f'{BASE_URL}/tasks', json=new_task)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])


def test_get_tasks():
    response = requests.get(f'{BASE_URL}/tasks')
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total" in response_json


def test_get_task():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert task_id == response_json['id']


def test_update_task():
    if tasks:
        task_id = tasks[0]
        payload = {
            'title': 'Tarefa atualizada',
            'description': 'Descrição da tarefa atualizada',
            'completed': True
        }
        response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)

        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

        # Nova requisição para verificar se a tarefa foi atualizada
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200
        response_json = response.json()
        assert payload['title'] == response_json['title']
        assert payload['description'] == response_json['description']
        assert payload['completed'] == response_json['completed']


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 200

        # Nova requisição para verificar se a tarefa foi removida
        response = requests.get(f'{BASE_URL}/tasks/{task_id}')
        assert response.status_code == 404
