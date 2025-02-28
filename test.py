import sqlite3


def insert(n, s, e, desc):  #функция, вносящая нового учителя в БД (имя, предмет, опыт работы, описание)
    global cursor
    cursor.execute(f"INSERT INTO teachers(name,subject,experience,description) VALUES({''.join(['"', n, '"'])}, {''.join(['"', s, '"'])}, {e}, {''.join(['"', desc, '"'])})")


def fetchbyname(n):         #находит нужных учителей по имени (если имя совпадает)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE name = {''.join(['"',n, '"' ])}")
    return list(res)

def fetchbysubject(s):       #находит нужных учителей по предмету (если предмет совпадает с нужным)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE subject = {''.join(['"',s, '"' ])}")
    return list(res)

def fetchbyexperience(e):    #находит нужных учителей по опыту работы (если опыт больше или равен нужному, выводит страничку препода)
    global cursor
    res = cursor.execute(f"SELECT * FROM teachers WHERE experience >= {e}")
    return list(res)






con = sqlite3.connect("teachers.sqlite")
cursor = con.cursor()
#insert("Anya", "maths", 23, "hello")
#print(fetchbyname("Anya"))
#print(fetchbyexperience("22"))
#print(fetchbyexperience("23"))
#print(fetchbysubject("maths"))       - примеры для проверки работы кода (убери комменты и проверяй)


#есть вопросы - пишите в телегу