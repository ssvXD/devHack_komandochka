import sqlite3

class BD:
    def __init__(self):            #просто инит
        global coni
        global cont
        global cursort
        global cursori


    def insert(self, i, n, c, s, a, desc, w, e, p):  #функция, вносящая нового учителя в БД (иднекс, имя, направление, предмет, опыт работы, описание)
        cursort.execute(f"INSERT INTO teachers(ind,name,category,subject,age,description,workplace,education,password) VALUES({i}, {''.join(['"', n, '"'])}, {''.join(['"', c, '"'])}, {''.join(['"', s, '"'])}, {a}, {''.join(['"', desc, '"'])}, {''.join(['"', w, '"'])}, {''.join(['"', e, '"'])}, {''.join(['"', p, '"'])})")



    def fetchbyindex(self, i):       #находит препода по индексу (они по порядку будут)
        res = cursort.execute(f"SELECT * FROM teachers WHERE ind = {i}")
        return list(res)


    def fetchbyname(self, n):         #находит нужных учителей по любому отрывку имени
        res = cursort.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + n + '%',))
        return list(res)


    def fetchbyworkplace(self, w):         #находит нужных учителей по месту работы
        res = cursort.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + w + '%',))
        return list(res)


    def fetchbyeducation(self, e):         #находит нужных учителей по его образованию
        res = cursort.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + e + '%',))
        return list(res)


    def fetchbysubject(self, s):       #находит нужных учителей по любой части названия предмета
        res = cursort.execute("SELECT * FROM teachers WHERE subject like ?", ('%' + s + '%',))
        return list(res)


    def fetchbyage(self, a):    #находит нужных учителей по опыту работы (если опыт больше или равен нужному, выводит страничку препода)
        res = cursort.execute(f"SELECT * FROM teachers WHERE experience >= {a}")
        return list(res)


    def fetchbydescription(self, desc):    #находит учителей по любому отрывку описания
        res = cursort.execute("""SELECT * FROM teachers WHERE description like ? """, ('%' + desc + '%',))
        return list(res)


    def fetchbycategory(self, cat):    #находит учителей по любому отрывку направления
        res = cursort.execute("""SELECT * FROM teachers WHERE category like ? """, ('%' + cat + '%',))
        return list(res)


class Account:
    def __init__(self, login, password):
        global coni
        global cont
        global cursort
        global cursori
        self.login = login
        self.password = password
        cursori.execute(f"INSERT INTO ids(login, password) VALUES({'"' + login + '"'}, {''.join(['"', password, '"'])})")


    def log_in(self):
        res = cursort.execute(f"""SELECT * FROM teachers WHERE name = {'"' + self.login + '"'} and password = {''.join(['"', self.password, '"'])} """).fetchall()
        return res


cont = sqlite3.connect("teachers.sqlite")
cursort = cont.cursor()
coni = sqlite3.connect("ids.sqlite")
cursori = coni.cursor()
base = BD() #класс базы данных, ему можно дать любое имя, я выбрал base
base.insert(1, "Anya", "physics and mathematics", "maths", 23, "hello, my friends!", "wa", "adsa", "ble")
base.insert(2, "Tobey", "Internet Technology", "maths", 12, "yo bozo", "", "", "aaa")
Anya = Account("Anya", "ble")
print(Anya.log_in())
#print(base.fetchbycategory("in"))
#print(base.fetchbyindex(1))
#print(base.fetchbydescription(""))
#print(base.fetchbyname("y"))
#print(base.fetchbyexperience("22"))
#print(base.fetchbyexperience("23"))
#print(base.fetchbysubject("mat"))       # примеры для проверки работы кода (убери комменты и проверяй)


#есть вопросы - пишите в телегу