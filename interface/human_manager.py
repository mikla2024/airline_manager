import sqlite3
from datetime import datetime
from abc import ABC

from data import Database


class Creature(ABC):
    pass


class Human(Creature):
    def __init__(self):
        self._name: str
        self._dob: datetime
        self._surname: str


class Employee(Human):
    def __init__(self) -> None:
        super().__init__()

        self._lcode: str
        self._job_title: str
        self._job_start: datetime

    @property
    def name(self) -> str:
        return self._name

    @property
    def surname(self) -> str:
        return self._surname

    @property
    def dob(self) -> datetime:
        return self._dob

    @property
    def job_title(self) -> str:
        return self._job_title

    @property
    def job_start(self) -> datetime:
        return self._job_start

    @property
    def l_code(self):
        return self._lcode

    @name.setter
    def name(self, name: str):
        if not name: raise AttributeError
        self._name = name

    @surname.setter
    def surname(self, surname: str):
        if len(surname) < 3:
            raise ValueError('Слишком короткая фамилия, должно быть больше 2 букв')
        self._surname = surname

    @dob.setter
    def dob(self, dob: str):
        self._dob = self.convert_date(dob)

    @job_title.setter
    def job_title(self, job_title: str):
        # Add validation if required
        self._job_title = job_title

    @job_start.setter
    def job_start(self, job_start: datetime):
        # Add validation if required
        self._job_start = self.convert_date(job_start)

    @l_code.setter
    def l_code(self, l_code: str):
        self._lcode = l_code

    @staticmethod
    def convert_date(dt_str) -> datetime:
        try:
            return datetime.strptime(dt_str, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Дата должна быть в формате дд.мм.гггг')


class HRManager:
    """ HR interface for Employees handling """

    def add_new(self, empl: Employee):

        with Database() as db:
            try:
                db.exec(
                    'INSERT INTO employees (name, last_name, dob, lcode, job_title, job_start)'
                    'VALUES (?,?,?,?,?,?)', empl.name, empl.surname,
                    empl.dob.strftime('%d.%m.%Y'), empl.l_code, empl.job_title,
                    empl.job_start.strftime('%d.%m.%Y')
                )
                db.exec(
                    'INSERT INTO employees_job_title (pers_id, job_id)'
                    f'VALUES ("{db.get_lastrowid()}", (SELECT job_id FROM job_titles '
                    f'WHERE job_title = "{empl.job_title}"));'
                )
                db.commit()

            except sqlite3.IntegrityError as e:

                raise AttributeError(e)


if __name__ == '__main__':
    pass
