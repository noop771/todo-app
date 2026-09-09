# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Task

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ============================================================
# РЕГИСТРАЦИЯ
# ============================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('register.html', error='Заполните все поля')

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Пользователь уже существует')

        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# ============================================================
# ВХОД
# ============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        return render_template('login.html', error='Неверный логин или пароль')

    return render_template('login.html')

# ============================================================
# ГЛАВНАЯ СТРАНИЦА (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)
# ============================================================
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ============================================================
# ВЫХОД
# ============================================================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ============================================================
# API: ПОЛУЧИТЬ ЗАДАЧИ
# ============================================================
@app.route('/api/tasks')
@login_required
def api_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{'id': t.id, 'text': t.text} for t in tasks])

# ============================================================
# API: ДОБАВИТЬ ЗАДАЧУ
# ============================================================
@app.route('/api/add', methods=['POST'])
@login_required
def api_add():
    data = request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'Текст задачи не может быть пустым'}), 400

    task = Task(text=text, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()

    return jsonify({'ok': True, 'task': {'id': task.id, 'text': task.text}})

# ============================================================
# API: УДАЛИТЬ ЗАДАЧУ
# ============================================================
@app.route('/api/delete/<int:task_id>', methods=['POST'])
@login_required
def api_delete(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()

    if not task:
        return jsonify({'error': 'Задача не найдена'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'ok': True})

# ============================================================
# СОЗДАНИЕ ТАБЛИЦ БАЗЫ ДАННЫХ (ПРИ ПЕРВОМ ЗАПУСКЕ)
# ============================================================
with app.app_context():
    db.create_all()

# ============================================================
# ЗАПУСК СЕРВЕРА
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)