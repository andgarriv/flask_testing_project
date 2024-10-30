from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos MariaDB
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Definición del modelo de Tarea
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'done': self.done
        }


# Ruta para obtener la lista de tareas (versión HTML)
@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)


# Ruta para obtener la lista de tareas en JSON (API)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify({'tasks': [task.to_dict() for task in tasks]})


# Ruta para crear una nueva tarea desde un formulario HTML
@app.route('/add_task', methods=['POST'])
def add_task_html():
    title = request.form.get('title')
    if not title:
        return "El título es necesario", 400
    new_task = Task(title=title, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task_list'))


# Ruta para crear una nueva tarea (API JSON)
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'El título es necesario'}), 400
    new_task = Task(title=request.json['title'], done=False)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


if __name__ == '__main__':
    # Crear las tablas en la base de datos si no existen
    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=5000, debug=True)