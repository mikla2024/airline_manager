import interface
from data import Database
import PySimpleGUI as sg
from typing import Optional
from datetime import datetime, date

class GUInterface:

    def __init__(self):
        self._window: Optional[sg.Window] = None
        self._layout: list

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._window: self._window.close()



class GUInterfaceFlight(GUInterface):

    def __init__(self):
        super().__init__()

        with Database() as db:
            lst_ap = db.fetch_lst('SELECT icao_code FROM airports')

        self._layout = [
            [sg.Text("Введите номер рейса:", s=20), sg.InputText(k='-name-', s=10, default_text='MMO3140')],
            [sg.Text("Выберете а/п вылета:", s=20),
             sg.Combo(values=lst_ap, k="-dep_ap-", enable_events=True, s=10, readonly=True)],
            [sg.Text("Выберете а/п прилета:", s=20),
             sg.Combo(values=lst_ap, k="-arr_ap-", enable_events=True, s=10, readonly=True)],
            [sg.Text("Дата вылета:", s=20), sg.InputText(key="-dep_date-", s=10,default_text='10.10.2025' ),
                sg.Text("Время вылета UTC:", s=15), sg.InputText(key="-dep_time-", s=5,default_text='10:00')],
            [sg.Text("Дата прилета:", s=20),sg.InputText(key="-arr_date-", s=10, default_text='10.10.2025'),
             sg.Text("Время прилета UTC:", s=15), sg.InputText(key="-arr_time-", s=5,default_text='15:00')],
            [sg.Button("Ok", k="-add_new-"), sg.Button("Cancel")]
        ]
        self._window = sg.Window('Добавить новый рейс', self._layout)
        self.event_loop()

    def event_loop(self):

        while True:
            event, values = self._window.read()
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            elif event == '-add_new-':
                try:
                    new_flight = interface.Flight()
                    new_flight.name = values['-name-'].strip() if values['-name-'] else None
                    new_flight.dep_ap = values['-dep_ap-']
                    new_flight.arr_ap = values['-arr_ap-']
                    new_flight.dep_dt = " ".join((values['-dep_date-'], values['-dep_time-']))
                    new_flight.arr_dt = " ".join((values['-arr_date-'], values['-arr_time-']))

                    interface.FlightManager().add_flight(new_flight)

                except ValueError:
                    print("event_loop new_flight")

    @property
    def get_layout(self):
        return self._layout


class GUInterfaceEmployee(GUInterface):

    def __init__(self):
        super().__init__()

        with Database() as db:
            self._lst_dpt = db.fetch_lst('SELECT dep_name FROM departments')

        self._layout = [
            [sg.Text("Департамент:", s=30),
             sg.Combo(values=self._lst_dpt, readonly=True,
                      k="-dep_name-", enable_events=True, s=15)],
            [sg.Text("Фамилия (минимум 3 символа):", s=30),sg.InputText(k="-surname-", s=15)],
            [sg.Text("Имя:", s=30), sg.InputText(k="-name-", s=15)],
            [sg.Text("Дата рождения:", s=30), sg.InputText(k="-dob-", s=15)],
            [sg.Text("Буквенный код (уникальный)", s=30), sg.InputText(k='-l_code-', s=15)],
            [sg.Text("Должность", s=30),
             sg.Combo(values=[], k='-job_title-',s=15, readonly=True )],
            [sg.Text("Дата приема на работу:", s=30), sg.InputText(key="-job_start-", s=15),
             sg.Button("Сегодня", k='-today-')],
            [sg.Button("Ok", key="-add_new-"), sg.Button("Cancel")]
        ]
        self._window = sg.Window('Принять на работу', self._layout)
        self.event_loop()

    @property
    def get_layout(self):
        return self._layout


    def event_loop(self):

        while True:

            event, values = self._window.read()
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            elif event == '-add_new-':
                try:
                    new_empl = interface.Employee()
                    new_empl.name = values['-name-'].strip() if values['-name-'] else None
                    new_empl.surname = values['-surname-']
                    new_empl.dob = values['-dob-']
                    new_empl.l_code = values['-l_code-'].strip() if values['-l_code-'] else None
                    new_empl.job_title = values['-job_title-'].strip() if values['-job_title-'] else None
                    new_empl.job_start = values['-job_start-']

                    interface.HRManager().add_new(new_empl)
                    for i,f in enumerate(self._window.element_list()):
                        if isinstance(f,(sg.InputText, sg.Combo)) :
                            f.update(value='')

                except ValueError:
                    sg.popup('Одно или несколько значений '
                             'имеют неверный формат',title='Ошибка')

                    continue


                except AttributeError as e:

                    sg.popup(f'Проверьте все поля...{e.args[0]}', title='Ошибка')
                    for f in self._window.element_list():
                        if isinstance(f, (sg.InputText, sg.Combo)) and not values[f.key]:
                            f.update(background_color='Red')
                    continue

                sg.popup('Сотрудник добавлен')
                self._reset_backgr_color()


            elif event == '-dep_name-':
                with Database() as db:
                   lst_jobs = db.fetch_lst(
                    'SELECT job_title FROM job_titles WHERE depart_id = '
                    f'(SELECT depart_id FROM departments WHERE dep_name = "{values['-dep_name-']}")'
                        )
                if not lst_jobs: lst_jobs = ['']
                element = self._window['-job_title-'] # type:sg.Combo
                element.update(values=lst_jobs, size=(15,15), value=lst_jobs[0])

            elif event == '-today-':
                element = self._window['-job_start-'] # type: sg.InputText
                element.update(value= datetime.strftime(datetime.today(),'%d.%m.%Y'))


    def _reset_backgr_color(self):
        for f in self._window.element_list():
            if isinstance(f, (sg.InputText, sg.Combo)):
                f.update(background_color='White')



if __name__ == '__main__':
    GUInterfaceEmployee()
    # GUInterfaceFlight()