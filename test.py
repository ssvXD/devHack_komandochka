import sqlite3


def insert(i, n, s, e, desc):  #функция, вносящая нового учителя в БД (имя, предмет, опыт работы, описание)
    global cursor
    cursor.execute(f"INSERT INTO teachers(ind,name,subject,experience,description) VALUES({i}, {''.join(['"', n, '"'])}, {''.join(['"', s, '"'])}, {e}, {''.join(['"', desc, '"'])})")

def fetchbyindex(i):       #находит препода по индексу (они по порядку будут)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE ind = {i}")
    return list(res)

def fetchbyname(n):         #находит нужных учителей по имени (если имя совпадает)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE name = {''.join(['"',n, '"' ])}")
    return list(res)

def fetchbysubject(s):       #находит нужных учителей по любой части названия предмета
    global cursor
    res = cursor.execute("SELECT * FROM teachers WHERE subject like ?", ('%' + s + '%',))
    return list(res)

def fetchbyexperience(e):    #находит нужных учителей по опыту работы (если опыт больше или равен нужному, выводит страничку препода)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE experience >= {e}")
    return list(res)


def fetchbydescription(desc):    #находит учителей по любому отрывку описания
    global cursor
    res = cursor.execute("""SELECT * FROM teachers WHERE description like ? """, ('%' + desc + '%',))
    return list(res)





con = sqlite3.connect("teachers.sqlite")
cursor = con.cursor()
insert(1, "Anya", "maths", 23, "hello, my friends!")
insert(2, "Tobey", "maths", 12, "yo bozo")
#print(fetchbyindex(1))
#print(fetchbydescription(""))
#print(fetchbyname("Anya"))
#print(fetchbyexperience("22"))
#print(fetchbyexperience("23"))
#print(fetchbysubject("mat"))       # примеры для проверки работы кода (убери комменты и проверяй)


#есть вопросы - пишите в телегу