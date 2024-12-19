!pip install flask

from flask import Flask
import sqlite3
from google.colab import output
import threading
import socket
import os 

# Создание Flask-приложения
app = Flask(__name__)

# Создание и заполнение базы данных
def create_database():
    # Удаляем старый файл базы данных если он существует (была проблема с повторным запуском, файл постоянно был поврежден - решила его просто перезаписывать)
    if os.path.exists('gifts.db'):
        os.remove('gifts.db')
    
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    
    # Удаляем таблицу если она существует
    cursor.execute('DROP TABLE IF EXISTS gifts')
    
    # Создание таблицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gift TEXT NOT NULL,
            price INTEGER NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Заполнение таблицы данными
    gifts_data = [
        ('Иванов Иван', 'Часы', 5000, 'куплен'),
        ('Петрова Анна', 'Книга', 1000, 'не куплен'),
        ('Сидоров Петр', 'Телефон', 15000, 'куплен'),
        ('Козлова Мария', 'Сумка', 3000, 'не куплен'),
        ('Морозов Андрей', 'Планшет', 20000, 'куплен'),
        ('Волкова Елена', 'Духи', 4000, 'куплен'),
        ('Соколов Дмитрий', 'Кошелек', 2000, 'не куплен'),
        ('Попова Ольга', 'Шарф', 1500, 'куплен'),
        ('Новиков Артем', 'Перчатки', 1000, 'не куплен'),
        ('Федорова Ирина', 'Ноутбук', 45000, 'куплен')
    ]
    
    cursor.executemany('INSERT INTO gifts (name, gift, price, status) VALUES (?, ?, ?, ?)', gifts_data)
    conn.commit()
    conn.close()

# Декоратор, который обрабатывает GET-запрос к корневому URL '/'
@app.route('/')
def index():
    # Получаем данные из базы
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    #SELECT-запрос
    cursor.execute('SELECT name, gift, price, status FROM gifts')
    gifts = cursor.fetchall()
    conn.close()

    # Создаем HTML
    html = '''
    <html>
    <head>
        <title>Список подарков</title>
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            h1 {
                color: #333;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>Список подарков</h1>
        <table>
            <tr>
                <th>ФИО</th>
                <th>Подарок</th>
                <th>Стоимость</th>
                <th>Статус</th>
            </tr>
    '''
    
    for gift in gifts:
        html += f'''
            <tr>
                <td>{gift[0]}</td>
                <td>{gift[1]}</td>
                <td>{gift[2]}</td>
                <td>{gift[3]}</td>
            </tr>
        '''
    
    html += '''
        </table>
    </body>
    </html>
    '''
    
    return html

# Создаем и заполняем базу данных
create_database()

# Запускаем сервер в отдельном потоке
def run_server():
    app.run(port=8000)

server_thread = threading.Thread(target=run_server)
server_thread.start()

# Открываем порт для доступа
output.serve_kernel_port_as_iframe(8000)
