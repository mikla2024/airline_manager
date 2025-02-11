
from data import Database
from datetime import datetime
from typing import Optional


class FlightManager:

    def __init__(self):
        self._flight_list: list[dict] = self._get_flights()

    @staticmethod
    def _get_flights() -> list:
        return Database().fetch_lst(
            sql='SELECT * FROM flights'
        )

    def add_flight(self, flight):
        with Database() as db:
            try:
                db.exec(
                    'INSERT INTO flights (flight_str, dep_dt, arr_dt, dep_ap, arr_ap)'
                    'VALUES (?,?,?,?,?)', flight.name, flight.dep_dt.strftime('%d.%m.%Y %H:%M'),
                    flight.arr_dt.strftime('%d.%m.%Y %H:%M'), flight.dep_ap, flight.arr_ap
                )

                db.exec(
                    'INSERT INTO apts_flights (flight_id, ap_id)'
                    f'VALUES ("{db.get_lastrowid()}", (SELECT ap_id FROM airports '
                    f'WHERE icao_code = "{flight.dep_ap}")),'
                    f'("{db.get_lastrowid()}", (SELECT ap_id FROM airports '
                    f'WHERE icao_code = "{flight.arr_ap}"));'
                )
                db.commit()

            except:
                print('ERROR in INSERT INTO flights')




class Flight:
    def __init__(self):
        self._name: str
        self._dep_dt: datetime
        self._dep_ap = str
        self._arr_ap = str
        self._arr_dt: datetime

    @property
    def name(self) -> str:
        return self._name

    @property
    def dep_ap(self):
        return self._dep_ap

    @property
    def arr_ap(self):
        return self._arr_ap

    @property
    def dep_dt(self) -> datetime:
        return self._dep_dt

    @property
    def arr_dt(self) -> datetime:
        return self._arr_dt



    @name.setter
    def name(self, name: str):
        # Add validation if required
        self._name = name

    @dep_ap.setter
    def dep_ap(self, dep_ap: str):
        # Add validation if required
        self._dep_ap = dep_ap

    @arr_ap.setter
    def arr_ap(self, arr_ap: str):
        # Add validation if required
        self._arr_ap = arr_ap

    @dep_dt.setter
    def dep_dt(self, dep_dt: str):
        try:
            self._dep_dt = self.pars_date(dep_dt)
        except ValueError:
            raise ValueError

    @arr_dt.setter
    def arr_dt(self, arr_dt: str):
        try:
            self._arr_dt = self.pars_date(arr_dt)
        except ValueError:
            raise ValueError

    @staticmethod
    def pars_date (dt_str: str) -> datetime:
        try:
            return datetime.strptime(dt_str,'%d.%m.%Y %H:%M')

        except ValueError:
            raise ValueError


if __name__ == '__main__':
    pass







