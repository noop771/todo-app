// static/js/script.js

async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }
        const tasks = await response.json();
        renderTasks(tasks);
    } catch (error) {
        console.error('Ошибка загрузки задач:', error);
    }
}

function renderTasks(tasks) {
    const list = document.getElementById('taskList');

    if (!tasks || tasks.length === 0) {
        list.innerHTML = '<div id="emptyMsg">✨ Пока нет задач. Добавьте первую!</div>';
        return;
    }

    list.innerHTML = '';
    tasks.forEach(task => {
        const div = document.createElement('div');
        div.className = 'task-item';
        div.id = 'task-' + task.id;
        div.innerHTML = `
            <span class="task-text">${task.text}</span>
            <div class="task-actions">
                <button class="btn-done" onclick="deleteTask(${task.id})">✔ Готово</button>
                <button class="btn-delete" onclick="forceDelete(${task.id})">✖ Удалить</button>
            </div>
        `;
        list.appendChild(div);
    });
}

document.getElementById('addBtn').onclick = async function() {
    const input = document.getElementById('taskInput');
    const text = input.value.trim();

    if (!text) {
        alert('Введите текст задачи!');
        return;
    }

    try {
        const response = await fetch('/api/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: text})
        });

        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }

        input.value = '';
        loadTasks();
    } catch (error) {
        console.error('Ошибка добавления задачи:', error);
        alert('Не удалось добавить задачу.');
    }
};

async function deleteTask(taskId) {
    const el = document.getElementById('task-' + taskId);
    if (!el) return;

    el.classList.add('removing');

    setTimeout(async () => {
        try {
            const response = await fetch('/api/delete/' + taskId, {method: 'POST'});
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            loadTasks();
        } catch (error) {
            console.error('Ошибка удаления задачи:', error);
        }
    }, 400);
}

async function forceDelete(taskId) {
    try {
        const response = await fetch('/api/delete/' + taskId, {method: 'POST'});
        if (response.status === 401) {
            window.location.href = '/login';
            return;
        }
        loadTasks();
    } catch (error) {
        console.error('Ошибка удаления задачи:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadTasks);