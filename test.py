import sqlite3

class BD:
    def __init__(self):            #просто инит
        con = sqlite3.connect("teachers.sqlite")
        self.cursor = con.cursor()


    def insert(self, i: object, n: object, c: object, s: object, a: object, desc: object, w: object, e: object, p: object) -> object:  #функция, вносящая нового учителя в БД (иднекс, имя, направление, предмет, опыт работы, описание)
        self.cursor.execute(f"INSERT INTO teachers(ind,name,category,subject,age,description,workplace,education,password) VALUES({i}, {''.join(['"', n, '"'])}, {''.join(['"', c, '"'])}, {''.join(['"', s, '"'])}, {a}, {''.join(['"', desc, '"'])}, {''.join(['"', w, '"'])}, {''.join(['"', e, '"'])}, {''.join(['"', p, '"'])})")


    def fetchbyindex(self, i):       #находит препода по индексу (они по порядку будут)
        res = self.cursor.execute(f"SELECT * FROM teachers WHERE ind = {i}")
        return list(res)


    def fetchbyname(self, n):         #находит нужных учителей по любому отрывку имени
        res = self.cursor.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + n + '%',))
        return list(res)


    def fetchbyworkplace(self, w):         #находит нужных учителей по месту работы
        res = self.cursor.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + w + '%',))
        return list(res)


    def fetchbyeducation(self, e):         #находит нужных учителей по его образованию
        res = self.cursor.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + e + '%',))
        return list(res)


    def fetchbysubject(self, s):       #находит нужных учителей по любой части названия предмета
        res = self.cursor.execute("SELECT * FROM teachers WHERE subject like ?", ('%' + s + '%',))
        return list(res)


    def fetchbyage(self, a):    #находит нужных учителей по опыту работы (если опыт больше или равен нужному, выводит страничку препода)
        res = self.cursor.execute(f"SELECT * FROM teachers WHERE experience >= {a}")
        return list(res)


    def fetchbydescription(self, desc):    #находит учителей по любому отрывку описания
        res = self.cursor.execute("""SELECT * FROM teachers WHERE description like ? """, ('%' + desc + '%',))
        return list(res)


    def fetchbycategory(self, cat):    #находит учителей по любому отрывку направления
        res = self.cursor.execute("""SELECT * FROM teachers WHERE category like ? """, ('%' + cat + '%',))
        return list(res)


class Account:
    def __init__(self, login, password):
        coni = sqlite3.connect("ids.sqlite")
        cont = sqlite3.connect("teachers.sqlite")
        self.cursor = coni.cursor()
        self.cursort = cont.cursor()
        self.login = login
        self.password = password
        self.cursor.execute(f"INSERT INTO ids(login, password) VALUES({''.join(['"', self.login, '"'])}, {''.join(['"', self.password, '"'])})")


    def log_in(self):
        res = self.cursort.execute(f"""SELECT * FROM teachers WHERE name = {''.join(['"', self.login, '"'])} and password = {''.join(['"', self.password, '"'])} """).fetchall()
        return res



base = BD() #класс базы данных, ему можно дать любое имя, я выбрал base
base.insert(1, "Anya", "physics and mathematics", "maths", 23, "hello, my friends!", "", "", "b")
Anya = Account("Anya", "b")
print(Anya.log_in())
#base.insert(2, "Tobey", "Internet Technology", "maths", 12, "yo bozo")
#print(base.fetchbycategory("in"))
#print(base.fetchbyindex(1))
#print(base.fetchbydescription(""))
#print(base.fetchbyname("y"))
#print(base.fetchbyexperience("22"))
#print(base.fetchbyexperience("23"))
#print(base.fetchbysubject("mat"))       # примеры для проверки работы кода (убери комменты и проверяй)


#есть вопросы - пишите в телегу