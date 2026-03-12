import sqlite3

class BD:
    def __init__(self):
        self.db_teachers = "teachers.sqlite"
        self.db_ids = "ids.sqlite"
        self._init_tables()

    def _init_tables(self):
        """Создаёт таблицы и добавляет недостающие колонки."""
        # Таблица teachers
        conn = self._get_teachers_conn()
        try:
            # Создаём таблицу, если её нет
            conn.execute('''
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    category TEXT,
                    subject TEXT,
                    age INTEGER,
                    experience INTEGER,
                    description TEXT,
                    workplace TEXT,
                    education TEXT,
                    password TEXT,
                    phone TEXT,
                    photo_path TEXT
                )
            ''')
            # Проверяем наличие всех колонок
            cursor = conn.execute("PRAGMA table_info(teachers)")
            existing_columns = [col[1] for col in cursor.fetchall()]
            
            # Список всех нужных колонок
            required_columns = [
                ('experience', 'INTEGER'),
                ('phone', 'TEXT'),
                ('photo_path', 'TEXT'),
                ('description', 'TEXT'),
                ('workplace', 'TEXT'),
                ('education', 'TEXT'),
                ('password', 'TEXT')
            ]
            
            for col_name, col_type in required_columns:
                if col_name not in existing_columns:
                    try:
                        conn.execute(f"ALTER TABLE teachers ADD COLUMN {col_name} {col_type}")
                        print(f"Добавлена колонка {col_name}")
                    except Exception as e:
                        print(f"Не удалось добавить {col_name}: {e}")
            conn.commit()
        finally:
            conn.close()

        # Таблица ids
        conn = self._get_ids_conn()
        try:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS ids (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    password TEXT
                )
            ''')
            conn.commit()
        finally:
            conn.close()

    def _get_teachers_conn(self):
        conn = sqlite3.connect(self.db_teachers, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_ids_conn(self):
        conn = sqlite3.connect(self.db_ids, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def insert(self, name, category, subject, age, experience, description, workplace, education, password, phone, photo_path):
        conn = self._get_teachers_conn()
        try:
            conn.execute('''
                INSERT INTO teachers 
                (name, category, subject, age, experience, description, workplace, education, password, phone, photo_path) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category, subject, age, experience, description, workplace, education, password, phone, photo_path))
            conn.commit()
            return True
        except Exception as e:
            print("="*50)
            print("INSERT ERROR:")
            print(e)
            print("="*50)
            return False
        finally:
            conn.close()

    def fetchbyindex(self, idx):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE id = ?", (idx,))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbyname(self, name):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE name LIKE ?", ('%' + name + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbyworkplace(self, workplace):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE workplace LIKE ?", ('%' + workplace + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbyeducation(self, education):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE education LIKE ?", ('%' + education + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbysubject(self, subject):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE subject LIKE ?", ('%' + subject + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbyage(self, age):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE age >= ?", (age,))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbyexperience(self, exp):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE experience >= ?", (exp,))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbydescription(self, desc):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE description LIKE ?", ('%' + desc + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def fetchbycategory(self, cat):
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers WHERE category LIKE ?", ('%' + cat + '%',))
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def get(self):
        """Возвращает ВСЕХ преподавателей"""
        conn = self._get_teachers_conn()
        try:
            cur = conn.execute("SELECT * FROM teachers")
            return self._format_results(cur.fetchall())
        finally:
            conn.close()

    def _format_results(self, rows):
        """Преобразует строки из БД в формат для шаблонов"""
        result = []
        for row in rows:
            d = dict(row)
            result.append({
                "id": d.get("id"),
                "name": d.get("name"),
                "direction": d.get("category"),      # важно: в шаблоне используется direction
                "subject": d.get("subject"),
                "age": d.get("age"),
                "experience": d.get("experience"),
                "description": d.get("description"),
                "work_place": d.get("workplace"),    # важно: в шаблоне work_place
                "education": d.get("education"),
                "password": d.get("password"),
                "phone": d.get("phone"),
                "photo": d.get("photo_path", "/static/uploads/img.png")
            })
        return result


class Account:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        # Сохраняем учётную запись в ids.sqlite (отдельное соединение)
        conn = sqlite3.connect("ids.sqlite", check_same_thread=False)
        try:
            conn.execute("INSERT INTO ids (login, password) VALUES (?, ?)", (login, password))
            conn.commit()
        finally:
            conn.close()

    def log_in(self):
        # Сначала ищем среди преподавателей
        bd = BD()
        teachers = bd.fetchbyname(self.login)
        for t in teachers:
            if t["password"] == self.password:
                return [t]

        # Если не нашли, ищем в таблице ids
        conn = sqlite3.connect("ids.sqlite", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute("SELECT * FROM ids WHERE login = ? AND password = ?", (self.login, self.password))
            rows = cur.fetchall()
            if rows:
                return [{"name": row["login"]} for row in rows]
            return []
        finally:
            conn.close()
