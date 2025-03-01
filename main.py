from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Секретный ключ для работы с сессиями

# Списки для хранения данных
users = []  # Список зарегистрированных пользователей
profiles = []  # Список анкет

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы регистрации
        name = request.form.get('name')
        direction = request.form.get('direction')
        subject = request.form.get('subject')
        age = request.form.get('age')
        description = request.form.get('description')
        work_place = request.form.get('work_place')
        education = request.form.get('education')
        password = request.form.get('password')

        # Проверяем, существует ли пользователь с таким именем
        if any(user['name'] == name for user in users):
            return "Пользователь с таким именем уже существует!"

        # Добавляем нового пользователя
        users.append({
            'name': name,
            'password': password
        })

        # Добавляем анкету в список profiles
        profiles.append({
            'name': name,
            'direction': direction,
            'subject': subject,
            'age': age,
            'description': description,
            'work_place': work_place,
            'education': education,
            'password': password
        })

        # Автоматически входим после регистрации
        session['name'] = name
        return redirect(url_for('show_profiles'))  # Перенаправляем на страницу profiles.html

    return render_template('register.html')

@app.route('/profiles')
def show_profiles():
    # Страница для отображения всех анкет
    return render_template('profiles.html', profiles=profiles)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
