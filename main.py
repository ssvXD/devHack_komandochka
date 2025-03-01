from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

from test import BD

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для работы с сессиями

# Настройки для загрузки файлов
UPLOAD_FOLDER = 'static/uploads'  # Папка для сохранения изображений
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Разрешенные расширения файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Списки для хранения данных + база данных
users = []  # Список зарегистрированных пользователей
data_base = BD()
profiles = data_base.get() # Список анкет преподавателей

# Функция для проверки расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', profiles=profiles)

@app.route('/register', methods=['GET', 'POST'])
def register(ID=0):
    if request.method == 'POST':
        # Получаем данные из формы регистрации
        name = request.form.get('name')
        direction = request.form.get('direction')
        subject = request.form.get('subject')
        age = request.form.get('age')
        experience = request.form.get('experience')
        work_place = request.form.get('work_place')
        education = request.form.get('education')
        description = request.form.get('description')
        password = request.form.get('password')

        # Проверяем, существует ли пользователь с таким именем
        if any(user['name'] == name for user in users):
            return "Пользователь с таким именем уже существует!"

        # Обрабатываем загруженное изображение
        if 'photo' not in request.files:
            return "Фотография не загружена!"
        photo = request.files['photo']
        if photo.filename == '':
            return "Файл не выбран!"
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)  # Безопасное имя файла
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)  # Сохраняем файл на сервере
        else:
            return "Недопустимый формат файла!"

        # Добавляем нового пользователя
        users.append({
            'name': name,
            'password': password
        })
        data_base.insert(ID, name, direction, subject, age, experience, work_place, education, description, password)
        ID+=1
        # Добавляем анкету в список profiles
        profiles.append({
            'name': name,
            'direction': direction,
            'subject': subject,
            'age': age,
            'experience': experience,
            'work_place': work_place,
            'education': education,
            'description': description,
            'photo': photo_path  # Сохраняем путь к изображению
        })
    
        # Автоматически входим после регистрации
        session['name'] = name
        return redirect(url_for('index'))  # Перенаправляем на главную страницу

    return render_template('register.html')

@app.route('/profiles')
def show_profiles():
    # Страница для отображения всех анкет
    return render_template('profiles.html', profiles=profiles)

if __name__ == '__main__':
    # Создаем папку для загрузок, если она не существует
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(port=8080, host='0.0.0.0')
