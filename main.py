from flask import Flask, render_template, request, redirect, url_for, session
from test import BD

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Секретный ключ для работы с сессиями

# Списки для хранения данных
users = []  # Список зарегистрированных пользователей
profiles = []  # Список анкет
ID = 0
data_base = BD()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register(ID=0):
    if request.method == 'POST':

        # Получаем данные из формы регистрации
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        direction = request.form.get('direction')
        subject = request.form.get('subject')
        experience = request.form.get('experience')
        description = request.form.get('description')

        # Проверяем, существует ли пользователь с таким именем
        if any(user['username'] == username for user in users):
            return "Пользователь с таким именем уже существует!"

        data_base.insert(ID, name, direction, subject, subject, experience, description) #функция, вносящая нового учителя в БД (иднекс, имя, направление, предмет, опыт работы, описание)
        ID += 1
        # Добавляем нового пользователя
        users.append({
            'username': username,
            'password': password
        })

        # Добавляем анкету в список profiles
        profiles.append({
            'username': username,
            'name': name,
            'direction': direction,
            'subject': subject,
            'experience': experience,
            'description': description
        })

        # Автоматически входим после регистрации
        session['username'] = username
        return redirect(url_for('show_profiles'))  # Перенаправляем на страницу profiles.html

    return render_template('register.html')

@app.route('/profiles')
def show_profiles():
    # Страница для отображения всех анкет
    return render_template('profiles.html', profiles=profiles)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0')
