from flask import Flask, request, jsonify
from models.task import Task
from uuid import uuid4

app = Flask(__name__)

tasks = []


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(id=uuid4(), title=data['title'], description=data.get('description', ''))
    tasks.append(new_task)
    return jsonify({'message': 'Nova tarefa criada com sucesso!', 'id': new_task.id})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]

    output = {
        'tasks': task_list,
        'total': len(task_list)
    }
    return jsonify(output)


@app.route('/tasks/<uuid:id>', methods=['GET'])
def get_task(id):
    task = list(filter(lambda t: t.id == id, tasks))
    if len(task) == 1:
        return jsonify(task[0].to_dict())
    return jsonify({'message': 'Tarefa não encontrada.'}), 404


@app.route('/tasks/<uuid:id>', methods=['PUT'])
def update_task(id):
    task = list(filter(lambda t: t.id == id, tasks))

    if len(task) != 1:
        return jsonify({'message': 'Tarefa não encontrada.'}), 404

    data = request.get_json()
    task[0].title = data['title']
    task[0].description = data['description']
    task[0].completed = data['completed']
    return jsonify({'message': 'Tarefa atualizada com sucesso!'})


@app.route('/tasks/<uuid:id>', methods=['DELETE'])
def delete_task(id):
    task = list(filter(lambda t: t.id == id, tasks))

    if len(task) != 1:
        return jsonify({'message': 'Tarefa não encontrada.'}), 404

    tasks.remove(task[0])
    return jsonify({'message': 'Tarefa removida com sucesso!'})


if __name__ == '__main__':
    app.run(debug=True)
