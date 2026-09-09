// static/js/script.js

// === ОСНОВНАЯ ЛОГИКА ПРИЛОЖЕНИЯ ===

// Функция загрузки задач с сервера
async function loadTasks() {
    const response = await fetch('/api/tasks');
    const tasks = await response.json();
    renderTasks(tasks);
}

// Функция отображения задач
function renderTasks(tasks) {
    const list = document.getElementById('taskList');
    
    // Если задач нет — показываем сообщение
    if (tasks.length === 0) {
        list.innerHTML = '<div id="emptyMsg">✨ Пока нет задач. Добавьте первую!</div>';
        return;
    }

    // Очищаем список и добавляем каждую задачу
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

// Функция добавления задачи
document.getElementById('addBtn').onclick = async function() {
    const input = document.getElementById('taskInput');
    const text = input.value.trim();
    
    if (!text) {
        alert('Введите текст задачи!');
        return;
    }

    // Отправляем на сервер
    await fetch('/api/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: text})
    });

    input.value = '';  // Очищаем поле ввода
    loadTasks();       // Перезагружаем список с сервера
};

// Функция удаления с анимацией (кнопка "Готово")
async function deleteTask(taskId) {
    const el = document.getElementById('task-' + taskId);
    if (!el) return;

    // Запускаем анимацию исчезновения
    el.classList.add('removing');

    // Ждём 400 мс (пока анимация закончится) и удаляем
    setTimeout(async () => {
        await fetch('/api/delete/' + taskId, {method: 'POST'});
        loadTasks(); // Обновляем список
    }, 400);
}

// Функция немедленного удаления (кнопка "Удалить")
async function forceDelete(taskId) {
    // Сразу удаляем на сервере
    await fetch('/api/delete/' + taskId, {method: 'POST'});
    loadTasks(); // Обновляем список
}

// Загружаем задачи при загрузке страницы
loadTasks();