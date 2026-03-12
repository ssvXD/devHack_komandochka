from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename
from test import BD, Account

# Импортируем Pillow, но обрабатываем случай его отсутствия
try:
    from PIL import Image, ImageDraw
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("Pillow не установлен, изображение по умолчанию не будет создано автоматически.")

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Создаём папку для загрузок, если её нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Создаём изображение по умолчанию (img.png), если его нет
def create_default_image():
    default_path = os.path.join(app.config['UPLOAD_FOLDER'], 'img.png')
    if not os.path.exists(default_path):
        if PILLOW_AVAILABLE:
            img = Image.new('RGB', (200, 200), color='gray')
            d = ImageDraw.Draw(img)
            d.text((10, 10), "Нет фото", fill='white')
            img.save(default_path)
        else:
            # Если Pillow нет, просто создаём пустой файл (пользователь позже заменит)
            with open(default_path, 'wb') as f:
                f.write(b'')

create_default_image()

data_base = BD()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    profiles = data_base.get()
    return render_template('index.html', profiles=profiles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные
        name = request.form.get('name', '').strip()
        direction = request.form.get('direction', '').strip()
        subject = request.form.get('subject', '').strip()
        age = request.form.get('age', '0')
        experience = request.form.get('experience', '0')
        work_place = request.form.get('work_place', '').strip()
        phone = request.form.get('phone', '').strip()
        education = request.form.get('education', '').strip()
        description = request.form.get('description', '').strip() or ''
        password = request.form.get('password', '').strip()

        # Проверка обязательных полей
        if not all([name, direction, subject, work_place, phone, education, password]):
            flash('Заполните все обязательные поля!')
            return render_template('register.html', form_data=request.form)

        # Проверка возраста и опыта
        try:
            age = int(age)
            experience = int(experience)
            if age < 0 or experience < 0:
                flash('Возраст и опыт не могут быть отрицательными!')
                return render_template('register.html', form_data=request.form)
        except ValueError:
            flash('Возраст и опыт должны быть числами!')
            return render_template('register.html', form_data=request.form)

        # Проверка уникальности имени
        existing = data_base.fetchbyname(name)
        if existing:
            flash('Пользователь с таким именем уже существует!')
            return render_template('register.html', form_data=request.form)

        # Обработка фото
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'img.png')  # по умолчанию
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(photo_path)

        # Вставка в БД
        success = data_base.insert(
            name=name,
            category=direction,
            subject=subject,
            age=age,
            experience=experience,
            description=description,
            workplace=work_place,
            education=education,
            password=password,
            phone=phone,
            photo_path=photo_path
        )

        if success:
            # Создаём аккаунт
            Account(name, password)
            session['name'] = name
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Ошибка при регистрации. Попробуйте позже.')
            return render_template('register.html', form_data=request.form)

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        account = Account(username, password)
        result = account.log_in()
        if result:
            session['name'] = username
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверное имя пользователя или пароль.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('name', None)
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/profiles')
def show_profiles():
    profiles = data_base.get()
    return render_template('profiles.html', profiles=profiles)

@app.route('/api/search')
def api_search():
    search_type = request.args.get('type', '')
    query = request.args.get('query', '')

    if search_type == 'subject':
        results = data_base.fetchbysubject(query)
    elif search_type == 'name':
        results = data_base.fetchbyname(query)
    elif search_type == 'experience':
        try:
            exp = int(query)
            results = data_base.fetchbyexperience(exp)
        except ValueError:
            results = []
    elif search_type == 'category':
        results = data_base.fetchbycategory(query)
    elif search_type == 'workplace':
        results = data_base.fetchbyworkplace(query)
    else:
        results = data_base.get()

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
