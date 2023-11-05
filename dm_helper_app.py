import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, filedialog
import tkinter.filedialog as fd
from random import randint
import re
import psycopg2
from  window_class import Window

#=============================== методы кнопок ==========================
# описание кнопки "добавить моба"
def click(connection_data):
    window = Window("", connection_data)  # создается новый экземпляр класса Window

def multiple_click(connection_data):
    for i in range(0, int(multiple_mobs_counter.get())):
        window = Window(mob_combobox.get(), connection_data) # сразу открываем несколько мобов:

def db_load_mobs(connection_data):
    # установка соединения
    conn = psycopg2.connect(dbname=connection_data[0], user=connection_data[1],
                            password=connection_data[2], host=connection_data[3])

    # загрузка списка мобов
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT mob_name FROM mobs_6;
            """
        )
        mobs_list = list(cursor.fetchall())
        print (mobs_list)
        print("Список мобов загружен ")



    if conn:
        conn.close()
        print("Connection closed")
    mobs_list.sort()
    return mobs_list

def db_disconnect():
    pass

#=============================================================================================================================

#========================== Отрисовка стартового окна =============================
root = Tk()  # создание стартового окна
root.title("Dungeon Master Helper")  # имя стартового окна
root.geometry("350x200")  # размеры стартового окна

connection_data = []  # список с информацией для подключения к БД
file = "key.txt"  # имя файла
with open(file, 'r') as fp:  # открывается файл и построчно читается
    connection_data.append(fp.readline()[0:-1])
    connection_data.append(fp.readline()[0:-1])
    connection_data.append(fp.readline()[0:-1])
    connection_data.append(fp.readline())
print(connection_data)

# описание и расположение кнопки "добавить моба"
open_button = ttk.Button(text="Добавить моба", command=lambda: click(connection_data))
open_button.pack(anchor="center", expand=1)

# описание и расположения компонента для открытия сразу нескольких мобов
Multiple_mobs_frame = LabelFrame(text= "добавить нескольких мобов:", width=250, height=100)
Multiple_mobs_frame.pack(padx=10,pady=10)

multiple_mobs_label = ttk.Label(Multiple_mobs_frame, text="Сколько?")
multiple_mobs_label.pack(pady=10, padx=10, side=LEFT)

multiple_mobs_counter = Entry(Multiple_mobs_frame, width=5)
multiple_mobs_counter.insert(0, "1")
multiple_mobs_counter.pack(pady=10, padx=10, side=LEFT)

downloaded_mobs_names = db_load_mobs(connection_data)
mob_combobox = ttk.Combobox(Multiple_mobs_frame, values=downloaded_mobs_names, width=8)
if len(downloaded_mobs_names) > 0:
    mob_combobox.current(0)
mob_combobox.pack(pady=10, padx=10, side=LEFT)

multiple_open_button = ttk.Button(Multiple_mobs_frame, text="Выбрать", command=lambda: multiple_click(connection_data))
multiple_open_button.pack(pady=10, padx=10, side=LEFT)


root.mainloop()  # бесконечный цикл главного окна


