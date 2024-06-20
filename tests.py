# Unit-тесты

# подключаем модули
import unittest

# импортируем классы из App.py
from App import Database, Doctors, Patients, Records, Diseases

# класс TestDatabase - тестирует класс Database
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database('database.db')

    # тест подключения
    def test_close(self):
        self.db.close()
        self.assertIsNone(self.db.session)

# класс TestDoctors - тестирует класс Doctors
class TestDoctors(unittest.TestCase):
    def setUp(self):
        self.db = Database('database.db')
        self.doctors = Doctors(self.db)

    # тест получения всех записей о врачах
    def test_get_doctors(self):
        doctors = self.doctors.get_doctors()
        self.assertEqual(len(doctors), 3)

    # тест получения всех записей о врачах по специальности
    def test_get_doctors_by_specialty(self):
        doctors = self.doctors.get_doctors_by_specialty('Терапевт')
        self.assertEqual(len(doctors), 1)

# класс TestPatients - тестирует класс Patients
class TestPatients(unittest.TestCase):
    def setUp(self):
        self.db = Database('database.db')
        self.patients = Patients(self.db)

    # тест получения всех записей о пациентах
    def test_get_patients(self):
        patients = self.patients.get_patients()
        self.assertEqual(len(patients), 3)

# класс TestRecords - тестирует класс Records
class TestRecords(unittest.TestCase):
    def setUp(self):
        self.db = Database('database.db')
        self.records = Records(self.db)

    # тест получения всех записей
    def test_get_records(self):
        records = self.records.get_records()
        self.assertEqual(len(records), 3)

    # тест получения записей по пациенту и дате
    def test_get_records_by_patient_and_date(self):
        records = self.records.get_records_by_patient_and_date(1, '2024-06-10')
        self.assertEqual(len(records), 1)

    # тест получения записей по врачу и дате
    def test_get_records_by_doctor_and_date(self):
        records = self.records.get_records_by_doctor_and_date(1, '2024-06-10')
        self.assertEqual(len(records), 1)

    # тест получения записей по специальности и дате
    def test_get_records_by_specialty_and_date(self):
        records = self.records.get_records_by_specialty_and_date('Терапевт', '2024-06-10')
        self.assertEqual(len(records), 1)

# класс TestDiseases - тестирует класс Diseases
class TestDiseases(unittest.TestCase):
    def setUp(self):
        self.db = Database('database.db')
        self.diseases = Diseases(self.db)

    # тест получения записей о всех болезнях
    def test_get_diseases(self):
        diseases = self.diseases.get_diseases()
        self.assertEqual(len(diseases), 3)

# собственно, main()  • _ •
if __name__ == '__main__':
    # выводим результаты тестов в файл "unit tests.txt"
    with open('unit tests.txt', 'w') as f:
        # инициализируем и запускаем тесты
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
