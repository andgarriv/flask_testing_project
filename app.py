from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(__name__)

# Lista inicial de tareas (guardada en memoria)
tasks = [
    {'id': 1, 'title': 'Comprar pan', 'done': False},
    {'id': 2, 'title': 'Estudiar Python', 'done': False}
]

# Ruta para obtener la lista de tareas (versión HTML)
@app.route('/')
def task_list():
    return render_template('tasks.html', tasks=tasks)

# Ruta para obtener la lista de tareas en JSON (API)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Ruta para crear una nueva tarea desde un formulario HTML
@app.route('/add_task', methods=['POST'])
def add_task_html():
    title = request.form.get('title')
    if not title:
        return "El título es necesario", 400
    task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': title,
        'done': False
    }
    tasks.append(task)
    return redirect(url_for('task_list'))

# Ruta para crear una nueva tarea (API JSON)
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'El título es necesario'}), 400
    task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': request.json['title'],
        'done': False
    }
    tasks.append(task)
    return jsonify(task), 201

if __name__ == '__main__':
    app.run(debug=True)