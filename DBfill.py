# Код, заполняющий БД начальными данными

# импортируем модули
import sqlite3
from sqlite3 import Error
from sys import stderr

# пробуем подключиться к БД через конструкцию try-except
try:
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
except Error as err:
    print(err)

# создаем таблицу с врачами (id, ФИО, номер телефона, специальность, дата приема на работу, номер кабинета)
cur.execute("CREATE TABLE doctors(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, spec TEXT, workSince TEXT, cab INTEGER)")
conn.commit()

# добавляем врачей
cur.execute("INSERT INTO doctors VALUES (1, 'Иванов Иван Иванович', '88005553535', 'Терапевт', '2001-09-09', 115)")
cur.execute("INSERT INTO doctors VALUES (2, 'Смирнов Никита Дмитриевич', '89122190110', 'Педиатр', '2003-05-10', 116)")
cur.execute("INSERT INTO doctors VALUES (3, 'Жданов Алексей Александрович', '89200291144', 'Офтальмолог', '2003-07-17', 120)")
conn.commit()

# создаем таблицу с пациентами (id, ФИО, номер медкарты, год рождения, пол)
cur.execute("CREATE TABLE patients(id INTEGER PRIMARY KEY, name TEXT, medCard INTEGER, bYear INTEGER, gender TEXT)")
conn.commit()

# добавляем пациентов
cur.execute("INSERT INTO patients VALUES (1, 'Жмышенко Валерий Альбертович', 100001, 1955, 'М')")
cur.execute("INSERT INTO patients VALUES (2, 'Кузнецова Евгения Алексеевна', 100002, 2009, 'Ж')")
cur.execute("INSERT INTO patients VALUES (3, 'Молчанов Евгений Олегович', 100003, 1999, 'М')")
conn.commit()

# создаем таблицу с болезнями (id, название, номер болезни, группа болезни)
cur.execute("CREATE TABLE diseases(id INTEGER PRIMARY KEY, name TEXT, num INTEGER, diseaseGroup TEXT)")
conn.commit()

# добавляем болезни
cur.execute("INSERT INTO diseases VALUES (1, 'Близорукость', 001, 'Зрение')")
cur.execute("INSERT INTO diseases VALUES (2, 'Геморрой', 002, 'Воспаление')")
cur.execute("INSERT INTO diseases VALUES (3, 'ОРВИ', 003, 'Инфекция')")
conn.commit()

# создаем таблицу с записями (id, id пациента, id врача, id болезни, дата записи)
cur.execute("CREATE TABLE records(id INTEGER PRIMARY KEY, patientId INTEGER, doctorId INTEGER, diseaseId INTEGER, date TEXT)")
conn.commit()

# добавляем записи
cur.execute("INSERT INTO records VALUES (1, 1, 1, 2, '2024-06-10')")
cur.execute("INSERT INTO records VALUES (2, 2, 2, 3, '2023-10-07')")
cur.execute("INSERT INTO records VALUES (3, 3, 3, 1, '2024-05-20')")
conn.commit()

# закрываем соединение с БД
conn.close()