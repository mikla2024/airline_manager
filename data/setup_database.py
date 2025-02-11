import os
import sqlite3
import sys
from typing import Optional



class Database:

    def __init__(self, db_name: Optional[str] = None) -> None:
        if not db_name: db_name = os.environ.get('db_name')
        self._name = db_name
        self._connection = self._connect()
        self._cursor = self._connection.cursor()
        self._last_rowid: Optional[int] = None

    def _connect(self) -> sqlite3.Connection:
        try:
            return sqlite3.connect(self._name)
        except TypeError as e:
            print('Ошибка при установлении соединения с БД', e)
            sys.exit(1)

    def __enter__(self):
        print('Соединение с БД установлено')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._connection.close()
        # print (exc_type,'|',exc_val)

    @staticmethod
    def _dict_factory(cursor, row):
        columns: list = [description[0] for description in cursor.description]
        return {k:v for k, v in zip(columns, row)}

    def fetch_dict(self, sql: str, *args) -> list[dict] | None:
        """Возвращает любое количество столбцов построчно в виде словаря {column: value}"""
        try:
            self._connection.row_factory = self._dict_factory
            crsr = self._connection.cursor()
            rows = crsr.execute(sql, args)
            if not rows: return None
            crsr.close()
            return rows.fetchall()

        except sqlite3.OperationalError:
            raise sqlite3.OperationalError

    def fetch_lst(self, sql: str, *args) -> list[str] | None:
        """ Возвращает первый столбец из запроса построчно в виде списка list[column[0]]"""

        try:
            self._connection.row_factory = lambda cursor, raw: raw[0]
            crsr = self._connection.cursor()
            rows = crsr.execute(sql, args)
            if not rows: return None
            return rows.fetchall()

        except sqlite3.OperationalError:
            raise sqlite3.OperationalError

    def get_lastrowid(self):
        return self._last_rowid


    def exec(self, sql: str, *args):
        self._cursor.execute(sql, args)
        self._last_rowid = self._cursor.lastrowid

    def commit(self):
        self._connection.commit()

    def setup_database(self) -> None:
        try:
                self._cursor.executescript ("""
                    BEGIN;
                    PRAGMA foreign_keys = 1;

                    CREATE TABLE IF NOT EXISTS employees (
                    pers_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_name TEXT NOT NULL,
                    name TEXT NOT NULL,
                    dob TEXT NOT NULL,
                    lcode TEXT UNIQUE NOT NULL,
                    job_title TEXT NOT NULL,
                    job_start TEXT NOT NULL );

                    CREATE TABLE IF NOT EXISTS departments (
                    depart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dep_name TEXT NOT NULL,
                    UNIQUE (dep_name));

                    CREATE TABLE IF NOT EXISTS job_titles (
                    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    depart_id INTEGER NOT NULL,
                    FOREIGN KEY (depart_id) REFERENCES departments(depart_id));

                    CREATE TABLE IF NOT EXISTS employees_job_title (
                    pers_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    FOREIGN KEY (pers_id) REFERENCES employees(pers_id),
                    FOREIGN KEY (job_id) REFERENCES job_titles(job_id),
                    PRIMARY KEY (job_id, pers_id));
                
                    CREATE TABLE IF NOT EXISTS airports (
                    ap_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    icao_code TEXT UNIQUE NOT NULL,
                    iata_code TEXT UNIQUE NOT NULL,
                    city TEXT NOT NULL);
                    
                    CREATE TABLE IF NOT EXISTS flights (
                    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_str TEXT NOT NULL,
                    dep_dt TEXT NOT NULL,
                    arr_dt TEXT NOT NULL,
                    dep_ap TEXT NOT NULL,
                    arr_ap TEXT NOT NULL);
                
                    CREATE TABLE IF NOT EXISTS apts_flights(
                    ap_id INTEGER NOT NULL,
                    flight_id INTEGER NOT NULL,
                    FOREIGN KEY (ap_id) REFERENCES airports(ap_id),
                    FOREIGN KEY (flight_id) REFERENCES flights(flight_id),
                    PRIMARY KEY (ap_id, flight_id));

                    COMMIT;
                """)


                try:
                    self._cursor.executescript("""
                                
                                BEGIN;
                                INSERT INTO airports (icao_code, iata_code, city)
                                VALUES ("LIME", "BGY", "Bergamo, Italy"),
                                ("HEMA", "RMF", "MARSA ALAM intl., Egypt");
                                
                                INSERT INTO departments (dep_name) 
                                VALUES ("Operations"), ("Marketing");
                                
                                INSERT INTO job_titles (job_title, depart_id)
                                VALUES ("Cabin CM", 1), ("Captain", 1), ("First Officer", 1);
                                
                                COMMIT;
                            """)

                except sqlite3.IntegrityError as e:
                    pass
                    # print('INSERT departments error')

                self._connection.commit()

        except sqlite3.OperationalError as e:
            print(e)
            raise sqlite3.OperationalError


if __name__ == '__main__':
    pass
    # cn = Database(os.environ.get('db_name'))
    # rows = cn.cursor.execute('SELECT * FROM job_titles')
    # for r in rows:
    #     print(r[1])

    # with sqlite3.connect(os.environ.get('db_path')) as cn:
    #
