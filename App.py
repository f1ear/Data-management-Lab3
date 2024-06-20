# Основной код

# подключаем модули
from sqlalchemy import create_engine, Table, MetaData, select, insert, and_
from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable

# класс Database - отвечает за соединение с БД через SQLalchemy
class Database:
    def __init__(self, db_file):
        self.engine = create_engine(f'sqlite:///{db_file}')
        self.metadata = MetaData()
        self.session = sessionmaker(bind=self.engine)()

    # метод для разрывания соединения
    def close(self):
        self.session.close()
        self.session = None

# класс Doctors - отвечает за врачей
class Doctors:
    def __init__(self, db):
        self.session = db.session
        self.doctors = Table('doctors', db.metadata, autoload_with=db.engine)

    # метод для вывода всех записей о врачах
    def get_doctors(self):
        return self.session.execute(select(self.doctors)).fetchall()

    # метод для добавления врача
    def add_doctor(self, name, phone, spec, workSince, cab):
        self.session.execute(insert(self.doctors).values(name=name, phone=phone, spec=spec, workSince=workSince, cab=cab))
        self.session.commit()

    # метод для получения записей о врачах конкретной специальности
    def get_doctors_by_specialty(self, specialty):
        return self.session.execute(select(self.doctors).where(self.doctors.c.spec == specialty)).fetchall()

# класс Patients - отвечает за пациентов
class Patients:
    def __init__(self, db):
        self.session = db.session
        self.patients = Table('patients', db.metadata, autoload_with=db.engine)

    # метод для получения всех записей о пациентах
    def get_patients(self):
        return self.session.execute(select(self.patients)).fetchall()

    # метод для добавления пациента
    def add_patient(self, name, medCard, bYear, gender):
        self.session.execute(insert(self.patients).values(name=name, medCard=medCard, bYear=bYear, gender=gender))
        self.session.commit()

# класс Records - отвечает за записи пациентов к врачам
class Records:
    def __init__(self, db):
        self.session = db.session
        self.records = Table('records', db.metadata, autoload_with=db.engine)
        self.patients = Table('patients', db.metadata, autoload_with=db.engine)
        self.doctors = Table('doctors', db.metadata, autoload_with=db.engine)
        self.diseases = Table('diseases', db.metadata, autoload_with=db.engine)

    # метод для получения всех записей
    def get_records(self, date=None):
        if date:
            return self.session.execute(
                select(self.patients.c.name, self.doctors.c.name, self.diseases.c.name, self.records.c.date)
                .where(and_(self.records.c.patientId == self.patients.c.id, self.records.c.doctorId == self.doctors.c.id, self.records.c.diseaseId == self.diseases.c.id, self.records.c.date == date))
            ).fetchall()
        else:
            return self.session.execute(
                select(self.patients.c.name, self.doctors.c.name, self.diseases.c.name, self.records.c.date)
                .where(and_(self.records.c.patientId == self.patients.c.id, self.records.c.doctorId == self.doctors.c.id, self.records.c.diseaseId == self.diseases.c.id))
            ).fetchall()

    # метод для добавления записи
    def add_record(self, patientId, doctorId, diseaseId, date):
        self.session.execute(insert(self.records).values(patientId=patientId, doctorId=doctorId, diseaseId=diseaseId, date=date))
        self.session.commit()

    # метод для получения записей пациента по дате
    def get_records_by_patient_and_date(self, patientId, date):
        return self.session.execute(
            select(self.patients.c.name, self.doctors.c.name, self.diseases.c.name, self.records.c.date)
            .where(and_(self.records.c.patientId == self.patients.c.id, self.records.c.doctorId == self.doctors.c.id, self.records.c.diseaseId == self.diseases.c.id, self.records.c.patientId == patientId, self.records.c.date == date))
        ).fetchall()

    # метод для получения записей по врачу и дате
    def get_records_by_doctor_and_date(self, doctorId, date):
        return self.session.execute(
            select(self.patients.c.name, self.doctors.c.name, self.diseases.c.name, self.records.c.date)
            .where(and_(self.records.c.patientId == self.patients.c.id, self.records.c.doctorId == self.doctors.c.id, self.records.c.diseaseId == self.diseases.c.id, self.records.c.doctorId == doctorId, self.records.c.date == date))
        ).fetchall()

    # метод для получения записей по специальности врача и дате
    def get_records_by_specialty_and_date(self, specialty, date):
        return self.session.execute(
            select(self.patients.c.name, self.doctors.c.name, self.diseases.c.name, self.records.c.date)
            .where(and_(self.records.c.patientId == self.patients.c.id, self.records.c.doctorId == self.doctors.c.id, self.records.c.diseaseId == self.diseases.c.id, self.doctors.c.spec == specialty, self.records.c.date == date))
        ).fetchall()

# класс Diseases - отвечает за болезни
class Diseases:
    def __init__(self, db):
        self.session = db.session
        self.diseases = Table('diseases', db.metadata, autoload_with=db.engine)

    # метод для получения всех записей о болезнях
    def get_diseases(self):
        return self.session.execute(select(self.diseases)).fetchall()

# функция для печати таблицы, чтобы красивый вывод был (:
def print_table(data, columns):
    table = PrettyTable(columns)
    for row in data:
        table.add_row(row)
    print(table)

# собственно, main()
def main():
    db = Database('database.db')
    doctors = Doctors(db)
    patients = Patients(db)
    records = Records(db)
    diseases = Diseases(db)

    # меню
    while True:
        print("1. Показать врачей")
        print("2. Показать пациентов")
        print("3. Показать записи")
        print("4. Показать болезни")
        print("5. Добавить врача")
        print("6. Добавить пациента")
        print("7. Добавить запись")
        print("8. Показать записи пациента по дате")
        print("9. Показать записи врача по дате")
        print("10. Показать записи врачей определенной специальности по дате")
        print("11. Выход")
        choice = input("Выберите опцию: ")
        if choice == '1':
            print_table(doctors.get_doctors(), ["ID", "Имя", "Телефон", "Специальность", "Дата приема на работу", "Номер кабинета"])
        elif choice == '2':
            print_table(patients.get_patients(), ["ID", "Имя", "Номер медкарты", "Год рождения", "Пол"])
        elif choice == '3':
            print_table(records.get_records(), ["Имя пациента", "Имя врача", "Название болезни", "Дата"])
        elif choice == '4':
            print_table(diseases.get_diseases(), ["ID", "Название", "Номер", "Группа болезни"])
        elif choice == '5':
            name = input("Введите имя врача: ")
            phone = input("Введите телефон врача: ")
            spec = input("Введите специальность врача: ")
            workSince = input("Введите дату приема на работу врача: ")
            cab = int(input("Введите номер кабинета врача: "))
            doctors.add_doctor(name, phone, spec, workSince, cab)
        elif choice == '6':
            name = input("Введите имя пациента: ")
            medCard = int(input("Введите номер медкарты пациента: "))
            bYear = int(input("Введите год рождения пациента: "))
            gender = input("Введите пол пациента: ")
            patients.add_patient(name, medCard, bYear, gender)
        elif choice == '7':
            patientId = int(input("Введите ID пациента: "))
            doctorId = int(input("Введите ID врача: "))
            diseaseId = int(input("Введите ID болезни: "))
            date = input("Введите дату: ")
            records.add_record(patientId, doctorId, diseaseId, date)
        elif choice == '8':
            patientId = int(input("Введите ID пациента: "))
            date = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
            print_table(records.get_records_by_patient_and_date(patientId, date), ["Имя пациента", "Имя врача", "Название болезни", "Дата"])
        elif choice == '9':
            doctorId = int(input("Введите ID врача: "))
            date = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
            print_table(records.get_records_by_doctor_and_date(doctorId, date), ["Имя пациента", "Имя врача", "Название болезни", "Дата"])
        elif choice == '10':
            specialty = input("Введите специальность: ")
            date = input("Введите дату (в формате ГГГГ-ММ-ДД): ")
            print_table(records.get_records_by_specialty_and_date(specialty, date), ["Имя пациента", "Имя врача", "Название болезни", "Дата"])
        elif choice == '11':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

    # при выборе пункта "Выход" в меню, закрываем соденинение с БД
    db.close()

# запуск кода
if __name__ == "__main__":
    main()
