import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'

# Главная страница
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Добавление задачи
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Отметка задачи как выполненной
@app.route('/complete/<int:id>')
def complete(id):
    task = Task.query.get(id)
    if task:
        task.done = not task.done
        db.session.commit()
    return redirect(url_for('index'))

# Удаление задачи
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Создание папки instance, если её нет
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with app.app_context():
        db.create_all()  # Создаём базу данных при первом запуске

    # Запуск Flask с портом и хостом, которые нужны для Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
