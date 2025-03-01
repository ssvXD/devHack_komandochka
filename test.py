import sqlite3

class BD:
    def __init__(self):
        con = sqlite3.connect("teachers.sqlite")
        self.cursor = con.cursor()


    def insert(self, i, n, s, e, desc):  #функция, вносящая нового учителя в БД (имя, предмет, опыт работы, описание)
        self.cursor.execute(f"INSERT INTO teachers(ind,name,subject,experience,description) VALUES({i}, {''.join(['"', n, '"'])}, {''.join(['"', s, '"'])}, {e}, {''.join(['"', desc, '"'])})")

    def fetchbyindex(self, i):       #находит препода по индексу (они по порядку будут)
        res = self.cursor.execute(f"SELECT * FROM teachers WHERE ind = {i}")
        return list(res)

    def fetchbyname(self, n):         #находит нужных учителей по любому отрывку имени
        res = self.cursor.execute("SELECT * FROM teachers WHERE name like ? ", ('%' + n + '%',))
        return list(res)

    def fetchbysubject(self, s):       #находит нужных учителей по любой части названия предмета
        res = self.cursor.execute("SELECT * FROM teachers WHERE subject like ?", ('%' + s + '%',))
        return list(res)

    def fetchbyexperience(self, e):    #находит нужных учителей по опыту работы (если опыт больше или равен нужному, выводит страничку препода)
        res = self.cursor.execute(f"SELECT * FROM teachers WHERE experience >= {e}")
        return list(res)


    def fetchbydescription(self, desc):    #находит учителей по любому отрывку описания
        res = self.cursor.execute("""SELECT * FROM teachers WHERE description like ? """, ('%' + desc + '%',))
        return list(res)





base = BD()  #класс базы данных, ему можно дать любое имя, я выбрал base
#base.insert(1, "Anya", "maths", 23, "hello, my friends!")
#base.insert(2, "Tobey", "maths", 12, "yo bozo")
#print(fetchbyindex(1))
#print(fetchbydescription(""))
#print(fetchbyname("y"))
#print(fetchbyexperience("22"))
#print(fetchbyexperience("23"))
#print(fetchbysubject("mat"))       # примеры для проверки работы кода (убери комменты и проверяй)


#есть вопросы - пишите в телегу