# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Имя файла для хранения задач
TASKS_FILE = 'tasks.json'

# Функция загрузки задач из файла
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []  # Если файла нет - возвращаем пустой список

# Функция сохранения задач в файл
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# Главная страница - показывает интерфейс
@app.route('/')
def index():
    return render_template('index.html')

# API: получить все задачи (используется JavaScript)
@app.route('/api/tasks')
def api_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

# API: добавить задачу
@app.route('/api/add', methods=['POST'])
def api_add():
    data = request.get_json()
    new_task = {
        'id': max([t['id'] for t in load_tasks()], default=0) + 1,
        'text': data.get('text', '')
    }
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify({'ok': True})

# API: удалить задачу по id
@app.route('/api/delete/<int:task_id>', methods=['POST'])
def api_delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)