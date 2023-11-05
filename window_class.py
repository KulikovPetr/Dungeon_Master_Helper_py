import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, filedialog
import tkinter.filedialog as fd
from random import randint
import re
import psycopg2



class Window(Tk):  # описание окна карточки моба
    def __init__(self, mob_name, connection_data): # инициализация
        super().__init__()



        # конфигурация окна
        self.title("Новый моб")  # название окна
        self.geometry("510x260")  # размеры окна
        self.make_the_thole_grid(connection_data)  # вызыв функции для отрисовки всех элементов окна
        self.clicked_counter = 0

        if mob_name != "": # сразу загружаем параметры моба, если он был выбран заранее
            self.DB_load_button_click(mob_name,connection_data)


    def make_the_thole_grid(self, connection_data):  # функция отрисовки окна. В скобочках - строка, на которой будет отрисовываться строка

        self.add_information_row(0)  # имя, кд и лог боя
        self.add_hp_row(1)  # хп моба, текстбоксы для подсчёта урона и кнопка вычитания

        self.add_save_throws(2) # поле для спасбросков

        self.add_comments_row(5)  # комментарии для таблицы атак

        self.add_attack_1_row(6)  # строка атак 1
        #attack_row_2 =  self.add_attack_1_row(4)
        self.add_attack_2_row(7)  # строка атак 2
        self.add_attack_3_row(8)  # строка атак 3
        self.add_dice_bucket_row(9)  # строка броска ведра кубов
        self.add_options_row(10, connection_data)  # опции сохранения, загрузки и очистки лога

    def add_information_row(self,pos):

        # метка для имени
        self.label = ttk.Label(self, text="Имя моба:")
        self.label.grid(column=0, row=pos)

        # текстбокс с именем
        self.txt = Entry(self,width=10)
        self.txt.grid(column=1, row=pos)

        # текстбокс с кд
        self.AC_txt = Entry(self,width=10)
        self.AC_txt.grid(column=2, row=pos)
        self.AC_txt.insert(0,"КД: 13")

        # отрисовка батллога
        self.battlelog = scrolledtext.ScrolledText(self, width=20, height=14)
        self.battlelog.place(x=320, y=0)

        # отрисовка описания
        self.description_textbox = scrolledtext.ScrolledText(self, width=60, height=16, wrap="word")
        self.description_textbox.place(x=0, y=261)


    #====================  Разметка для ХП ==========================

    def add_hp_row(self,pos):

        # метка хп моба
        self.HP_label = ttk.Label(self, text="ХП моба:")
        self.HP_label.grid(column=0, row=pos)

        # текстбокс с текущим хп
        self.HP_current_txt = Entry(self,width=5)
        self.HP_current_txt.grid(column=1, row=pos)

        # текстбокс для ввода урона
        self.dmg_txt = Entry(self,width=5)
        self.dmg_txt.grid(column=2, row=pos)

        # кнопка для нанесения урона
        self.add_damage_button = ttk.Button(self, text="Вычесть!")
        self.add_damage_button["command"] = self.add_damage_clicked
        self.add_damage_button.grid(column=3, row=pos)

    def add_damage_clicked(self): # наносит урон по хп из окна урона

        if self.HP_current_txt.get() != '' and self.dmg_txt.get() != '':  # проверка на не пустые окна хп и урона
            hp_current = int(self.HP_current_txt.get())  # сохранение текущего хп
            self.HP_current_txt.delete(0,END)  # удаление текущего хп из текстбокса
            self.HP_current_txt.insert(0,str(int(hp_current - int(self.dmg_txt.get()))))  # вычитание из текущего хп урона и запись нового значения
            self.dmg_txt.delete(0,END)  # удаление значения урона


    #========================== Отрисовка окна со спас-бросками =============================
    def  add_save_throws(self, pos):

        self.information_frame = LabelFrame(self, text= "Спасброски:", width=200, height=200)
        self.information_frame.grid(column=0, columnspan=4, rowspan =3, row=pos)
        #self.information_frame.place(x=100,y=100)

        self.savethrows_textboxes = [0,1,2,3,4,5]
        self.savethrows_buttons = ["str", "dex", "con", "int", "wis", "cha"]

        self.str_save_throw = Entry(self.information_frame,width=5)
        self.str_save_throw.grid(column=0, row=pos+1)
        self.str_save_throw.insert(0,"0")

        self.dex_save_throw = Entry(self.information_frame,width=5)
        self.dex_save_throw.grid(column=1, row=pos+1)
        self.dex_save_throw.insert(0,"0")

        self.con_save_throw = Entry(self.information_frame,width=5)
        self.con_save_throw.grid(column=2, row=pos+1)
        self.con_save_throw.insert(0,"0")

        self.int_save_throw = Entry(self.information_frame,width=5)
        self.int_save_throw.grid(column=3, row=pos+1)
        self.int_save_throw.insert(0,"0")

        self.wis_save_throw = Entry(self.information_frame,width=5)
        self.wis_save_throw.grid(column=4, row=pos+1)
        self.wis_save_throw.insert(0,"0")

        self.cha_save_throw = Entry(self.information_frame,width=5)
        self.cha_save_throw.grid(column=5, row=pos+1)
        self.cha_save_throw.insert(0,"0")

        self.str_save_throw_button = ttk.Button(self.information_frame, text="СИЛ", width=5)
        self.str_save_throw_button["command"] = self.str_save_throw_button_click
        self.str_save_throw_button.grid(column=0, row=pos+2)

        self.dex_save_throw_button = ttk.Button(self.information_frame, text="ЛВК", width=5)
        self.dex_save_throw_button["command"] = self.dex_save_throw_button_click
        self.dex_save_throw_button.grid(column=1, row=pos+2)

        self.con_save_throw_button = ttk.Button(self.information_frame, text="ТЕЛ", width=5)
        self.con_save_throw_button["command"] = self.con_save_throw_button_click
        self.con_save_throw_button.grid(column=2, row=pos+2)

        self.int_save_throw_button = ttk.Button(self.information_frame, text="ИНТ", width=5)
        self.int_save_throw_button["command"] = self.int_save_throw_button_click
        self.int_save_throw_button.grid(column=3, row=pos+2)

        self.wis_save_throw_button = ttk.Button(self.information_frame, text="МДР", width=5)
        self.wis_save_throw_button["command"] = self.wis_save_throw_button_click
        self.wis_save_throw_button.grid(column=4, row=pos+2)

        self.cha_save_throw_button = ttk.Button(self.information_frame, text="ХАР", width=5)
        self.cha_save_throw_button["command"] = self.cha_save_throw_button_click
        self.cha_save_throw_button.grid(column=5, row=pos+2)

    def str_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок СИЛ: "+str(randint(1,20)+int(self.str_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз

    def dex_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок ЛВК: "+str(randint(1,20)+int(self.dex_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз

    def con_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок ТЕЛ: "+str(randint(1,20)+int(self.con_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз

    def int_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок ИНТ: "+str(randint(1,20)+int(self.int_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз

    def wis_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок МДР: "+str(randint(1,20)+int(self.wis_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз

    def cha_save_throw_button_click(self):
        self.battlelog.insert(INSERT, "Спасбросок ХАР: "+str(randint(1,20)+int(self.cha_save_throw.get()))+"\n")
        self.battlelog.see("end") # автопрокрутка лога вниз
    #========================== отрисовка строки комментариев к таблице атак ================

    def add_comments_row(self,pos):
        # отрисовка метки
        self.amount_of_attacks = ttk.Label(self, text="Колво атак")
        self.amount_of_attacks.grid(column=0, row=pos)

        # отрисовка метки
        self.damage_of_attacks = ttk.Label(self, text="урон")
        self.damage_of_attacks.grid(column=1, row=pos)

        # отрисовка метки
        self.atk_bonus = ttk.Label(self, text="Бонус атаки")
        self.atk_bonus.grid(column=2, row=pos)

        # кнопка нанесения всех атак за один клик
        self.do_all_attacks_button = ttk.Button(self, text="Все атаки!")
        self.do_all_attacks_button["command"] = self.do_all_attacks_button_clicked
        self.do_all_attacks_button.grid(column=3, row=pos)


    #===================== отрисовка строк атак: ====================================
    """ В идеале стоило бы добавить отдельный класс под строку атаки, состоящий из: количество атак, урон, попадание.
    Но я не додумался, как это делать, поэтому создал три, по сути, одинаковые функции, когда можно было обойтись одной.
    """

    def add_attack_1_row(self,pos): # отрисовка первой строки атаки

        # текстбокс количества атак
        self.atk_counter_1 = Entry(self, width=10)
        self.atk_counter_1.grid(column=0, row=pos)
        self.atk_counter_1.insert(0,"1")  # заполнение его "по умолчанию"

        # текстбокс урона
        self.damage_1 = Entry(self, width=10)
        self.damage_1.grid(column=1, row=pos)
        self.damage_1.insert(0,"1d6 +2")  # заполнение его "по умолчанию"

        # текстбокс модификатора атаки (на попадание)
        self.atk_bonus_1 = Entry(self, width=10)
        self.atk_bonus_1.grid(column=2, row=pos)
        self.atk_bonus_1.insert(0,"+4")  # заполнение его "по умолчанию"

        # кнопка для совершения атаки
        self.button_attack_1 = ttk.Button(self, text="Атака 1")
        self.button_attack_1["command"] = self.roll_the_attack_1
        self.button_attack_1.grid(column=3, row=pos)

    def add_attack_2_row(self,pos): # отрисовка второй строки атаки

        # текстбокс количества атак
        self.atk_counter_2 = Entry(self, width=10)
        self.atk_counter_2.grid(column=0, row=pos)

        # текстбокс урона
        self.damage_2 = Entry(self, width=10)
        self.damage_2.grid(column=1, row=pos)

        # текстбокс модификатора атаки (на попадание)
        self.atk_bonus_2 = Entry(self, width=10)
        self.atk_bonus_2.grid(column=2, row=pos)

        # кнопка для совершения атаки
        self.button_attack_2 = ttk.Button(self, text="Атака 2")
        self.button_attack_2["command"] = self.roll_the_attack_2
        self.button_attack_2.grid(column=3, row=pos)

    def add_attack_3_row(self,pos): # отрисовка третьей строки атаки

        # текстбокс количества атак
        self.atk_counter_3 = Entry(self, width=10)
        self.atk_counter_3.grid(column=0, row=pos)

        # текстбокс урона
        self.damage_3 = Entry(self, width=10)
        self.damage_3.grid(column=1, row=pos)

        # текстбокс модификатора атаки (на попадание)
        self.atk_bonus_3 = Entry(self, width=10)
        self.atk_bonus_3.grid(column=2, row=pos)

        # кнопка для совершения атаки
        self.button_attack_3 = ttk.Button(self, text="Атака 3")
        self.button_attack_3["command"] = self.roll_the_attack_3
        self.button_attack_3.grid(column=3, row=pos)

    def add_dice_bucket_row(self, pos):  # отрисовка строки с ведром кубов

        # текстовая метка для ведра кубок
        self.label_dice_bucket = ttk.Label(self, text="AOE спелл")
        self.label_dice_bucket.grid(column=0, row=pos)

        # текстбокс урона
        self.txt_dice_bucket = Entry(self,width=10)
        self.txt_dice_bucket.grid(column=1, row=pos)
        self.txt_dice_bucket.insert(0,"8d6") # заполнение его "по умолчанию"

        # кнопка броска кубов
        self.button_dice_bucket = ttk.Button(self, text="Кинуть!")
        self.button_dice_bucket["command"] = self.roll_the_dice_bucket
        self.button_dice_bucket.grid(column=3, row=pos)

    #======================== логика кнопки "все атаки" =========================================

    def do_all_attacks_button_clicked(self):  # кнопка для совершения всех прописанных атак

        self.battlelog.insert(INSERT, "Все атаки:\n")  # вывод  строки о совершении всех атак в лог

        if self.atk_counter_1.get() != '' and self.atk_counter_1.get() != '\n':  # проверка, не пустой ли текстбокс количества атак
            for i in range(0,int(self.atk_counter_1.get())):  # срабатывает на указанное количество атак
                self.roll_the_attack_1()  # совершение атаки 1

        if self.atk_counter_2.get() != '' and self.atk_counter_2.get() != '\n':  # проверка, не пустой ли текстбокс количества атак
            for i in range(0,int(self.atk_counter_2.get())):  # срабатывает на указанное количество атак
                self.roll_the_attack_2()  # совершение атаки 2

        if self.atk_counter_3.get() != '' and self.atk_counter_3.get() != '\n':  # проверка, не пустой ли текстбокс количества атак
            for i in range(0,int(self.atk_counter_3.get())):  # срабатывает на указанное количество атак
                self.roll_the_attack_3()  # совершение атаки 3

    #======================= методы для совершения атак =============================================
    """ Опять же, если бы я описал строку атаки одним классом, можно было бы ограничиться одним методом. 
    Приходится писать для каждой строки свой метод. Или это функция, а не метод? 
    """
    # метод для атаки 1
    def roll_the_attack_1(self):

        if self.atk_counter_1.get() != '' and self.damage_1.get() != '' and self.atk_bonus_1.get() != '':  # проверка, что строка не пустая
            self.battlelog.insert(INSERT,self.roll_the_dices(self.damage_1,self.atk_bonus_1)+"\n")  # запись в лог результатов бросков

        self.battlelog.see("end") # автопрокрутка лога вниз

    # метод для атаки 2
    def roll_the_attack_2(self):

        if self.atk_counter_2.get() != '' and self.damage_2.get() != '' and self.atk_bonus_2.get() != '':  # проверка, что строка не пустая
            self.battlelog.insert(INSERT,self.roll_the_dices(self.damage_2,self.atk_bonus_2)+"\n")  # запись в лог результатов бросков

        self.battlelog.see("end") # автопрокрутка лога вниз

    # метод для атаки 3
    def roll_the_attack_3(self):

        if self.atk_counter_3.get() != '' and self.damage_3.get() != '' and self.atk_bonus_3.get() != '':  # проверка, что строка не пустая
            self.battlelog.insert(INSERT,self.roll_the_dices(self.damage_3,self.atk_bonus_3)+"\n")  # запись в лог результатов бросков

        self.battlelog.see("end") # автопрокрутка лога вниз

    # совершение броска нескольких дайсов
    def roll_the_dice_bucket(self):

        if self.txt_dice_bucket.get() != '':  # проверка, что строка не пустая
            self.battlelog.insert(INSERT,self.roll_the_dices(self.txt_dice_bucket, None)+"\n") # запись в лог результатов бросков

        self.battlelog.see("end") # автопрокрутка лога вниз



    """ а здесь явно нарушается принцип SOLID. 
    А именно тот самый, который про "одна функция не должна уметь делать все".    
    Или как-то так он звучит.
    """
    # метод реализующий броски атаки и урона
    def roll_the_dices(self, damage_text_area, atk_bonus_area):  # принимает два аргумента: текстбокс с уроном и текстбокс с бонусом на атаку
        string = damage_text_area.get()  # получение значения из строки урона
        atk_value_string =""
        #damage_rolls = []
        damage_rolls = re.findall("\d+[d]\d+",string)  # поиск всех значений формата "число-d-число" в строке
        total_damage_of_dices = 0  # переменная для подсчёта всего урона

        if atk_bonus_area != None:  # костыльная проверка на то, урон это от атаки или от ведра кубов
            atk_dice = randint(1,20)  # генерируется значение от 1 до 20

            if atk_dice == 20:  # можно не добавлять модификатор атаки, и так проще выделить крит.
                atk_value_string = "Nat 20! :"  # формируем строку для вывода в лог
            elif atk_dice == 1:  # можно не добавлять модификатор атаки, и так проще выделить крит.
                atk_value_string = "Nat 1! :"  # формируем строку для вывода в лог
            else:
                #atk_value = atk_dice+int(atk_bonus_area.get())
                atk_value_string = str(atk_dice+int(atk_bonus_area.get())) + ": "  # добавляем бонус атаки и формируем строку для вывода в лог

        for item in damage_rolls:  #  Если прописано несколько разных типов дайсов для разных типов урона
            damage_from_dices_for_each_type = 0
            dice_to_roll = item.split('d')  # разделение на сколько и каких дайсов

            if atk_bonus_area != None:  # опять же, костыль на "заклинание ли это?". если не спелл, то:

                if atk_dice == 20:  # если попадание критическое,
                    dice_to_roll_total = int(dice_to_roll[0])*2  # то количество костей урона удваиваются
                else:
                    dice_to_roll_total = int(dice_to_roll[0])  # если не крит, то не удиваиваются

            else:
                dice_to_roll_total = int(dice_to_roll[0])  # если спелл то считаем количество костей урона

            for i in range(0,dice_to_roll_total):  # для каждой кости урона делаем бросок
                # damage_from_dice =
                damage_from_dices_for_each_type += randint(1, int(dice_to_roll[1])) # считаем сколько выпало с каждой кости

            atk_value_string += str(damage_from_dices_for_each_type) + "+"
            total_damage_of_dices+=damage_from_dices_for_each_type

        if atk_bonus_area != None:  # очередная костыльная проверка на то, не спелл ли это

            if re.findall("[+-]\d+",string)[0] != '':  # проверка, есть ли в строке модификатор характеристики для урона
                print("есть урон")
                atk_value_string = atk_value_string[0:-1]
                total_damage_of_dices += int(re.findall("[+-]\d+",string)[0])
                atk_value_string += re.findall("[+-]\d+",string)[0] + "="
                return atk_value_string + str(total_damage_of_dices)
                #return atk_value_string + str(total_damage_of_dices + int(re.findall("[+-]\d+",string)[0]))  # если модификатор есть, то добавляем его к урону и
                # и возвращаем значение урона
            else:
                return atk_value_string + str(total_damage_of_dices) # если нет, то просто возвращаем значение урона на костях

        else:
            return "Урон: " + str(total_damage_of_dices)  # если спелл, то тоже просто возвращаем значение урона на костях. Заклинания же не критуют


    #def change_name(self):
    #    self.label.configure(text=self.txt.get())

    #====================== строка опций: ===============================================
    def add_options_row(self, pos, connection_data):

        # отрисовка кнопки очистки лога
        self.clear_button = ttk.Button(self, text="Очистить")
        self.clear_button["command"] = self.clear_button_click
        self.clear_button.grid(column=4, row=pos)

        # отрисовка кнопки сохранения инфы в бд
        self.DB_save_button = ttk.Button(self, text="Сохранить")
        self.DB_save_button["command"] = lambda: self.DB_save_button_click(connection_data)
        self.DB_save_button.grid(column=1, row=pos)

        # отрисовка кнопки загрузки инфы из БД
        #self.DB_load_button = ttk.Button(self, text="Загрузить")
        #self.DB_load_button["command"] = lambda: self.DB_load_button_click(self.mob_name, self.connection_data)
        #self.DB_load_button.grid(column=0, row=pos)

        # отрисовка кнопки описания моба
        self.description_button = ttk.Button(self, text="Развернуть описание")
        self.description_button["command"] = self.description_button_click
        self.description_button.grid(column=2, row=pos, columnspan=2)

    #======================================================================================================================= Прикрученная база данных
    # описание кнопки сохранения моба в бд
    def DB_save_button_click(self, connection_data):
        # установка соединения
        conn_to_save = psycopg2.connect(dbname=connection_data[0], user=connection_data[1],
                                        password=connection_data[2], host=connection_data[3])

        # отправка запроса для сохранения параметров моба
        with conn_to_save.cursor() as cursor:
            cursor.execute(
                f"""
            DELETE FROM mobs_6
            WHERE mob_name='{self.txt.get()}'
            """

            )
            conn_to_save.commit()
            print("Данные удалены из БД")

            cursor.execute(
                f""" INSERT INTO mobs_6(
                
                mob_name, mob_AC, mob_hp,
                
                str, dex, con,
                int, wis, cha,
                
                atk_1_counter, atk_1_damage, atk_1_damage_bonus,
                atk_2_counter, atk_2_damage, atk_2_damage_bonus,
                atk_3_counter, atk_3_damage, atk_3_damage_bonus,
                
                mob_spell,
                mob_description) VALUES(
                '{self.txt.get()}', '{self.AC_txt.get()}', '{int(self.HP_current_txt.get())}',
                
                '{int(self.str_save_throw.get())}', '{int(self.dex_save_throw.get())}', '{int(self.con_save_throw.get())}',
                '{int(self.int_save_throw.get())}', '{int(self.wis_save_throw.get())}', '{int(self.cha_save_throw.get())}',
                
                '{int(self.atk_counter_1.get())}', '{str(self.damage_1.get())}', '{str(self.atk_bonus_1.get())}',
                '{int(self.atk_counter_2.get())}', '{str(self.damage_2.get())}', '{str(self.atk_bonus_2.get())}',
                '{int(self.atk_counter_3.get())}', '{str(self.damage_3.get())}', '{str(self.atk_bonus_3.get())}',
                
                '{str(self.txt_dice_bucket.get())}',
                '{self.description_textbox.get("1.0", END)}');              
                """
            )
            conn_to_save.commit()
            #print("Данные сохранены в БД")
        self.battlelog.insert(INSERT, "Данные сохранены\n")
        if conn_to_save:
            conn_to_save.close()
            print("Connection closed")


    # описание кнопки для загрузки карточки моба из БД
    def DB_load_button_click(self, mob_name, connection_data):
        # установка соединения
        conn_to_load = psycopg2.connect(dbname=connection_data[0], user=connection_data[1],
                                        password=connection_data[2], host=connection_data[3])

        # отправка запроса для сохранения параметров моба
        with conn_to_load.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT * FROM mobs_6 WHERE mob_name = '{mob_name}';
                """
            )
            data = cursor.fetchone()
            #========================================== Загрузка значений
            """ниже для каждого текстбокса сначала удаляется значение
               а затем вставляется значение из БД"""
            self.txt.delete(0, END)
            self.txt.insert(0,data[0])  # загружается имя моба
            self.title(self.txt.get())  # загружается имя моба и переименовывается окно

            self.AC_txt.delete(0,END)
            self.AC_txt.insert(0,data[1])   # загружается Кд

            self.HP_current_txt.delete(0,END)
            self.HP_current_txt.insert(0,data[2])  # загружается ХП

            #============================ Спасброски ====================================
            self.str_save_throw.delete(0,END)
            self.str_save_throw.insert(0,data[3])  # загружается спасбросок СИЛ

            self.dex_save_throw.delete(0,END)
            self.dex_save_throw.insert(0,data[4])  # загружается спасбросок ЛВК

            self.con_save_throw.delete(0,END)
            self.con_save_throw.insert(0,data[5])  # загружается спасбросок ТЕЛ

            self.int_save_throw.delete(0,END)
            self.int_save_throw.insert(0,data[6])  # загружается спасбросок ИНТ

            self.wis_save_throw.delete(0,END)
            self.wis_save_throw.insert(0,data[7])  # загружается спасбросок МДР

            self.cha_save_throw.delete(0,END)
            self.cha_save_throw.insert(0,data[8])  # загружается спасбросок ХАР

            #============================= Атаки =========================================
            self.atk_counter_1.delete(0,END)
            self.atk_counter_1.insert(0,data[9])   # загружается количество атак для атаки 1

            self.damage_1.delete(0,END)
            self.damage_1.insert(0,data[10])   # загружается урона для атаки 1

            self.atk_bonus_1.delete(0,END)
            self.atk_bonus_1.insert(0,data[11])  # загружается бонус атаки для атаки 1



            self.atk_counter_2.delete(0,END)
            self.atk_counter_2.insert(0,data[12])   # загружается количество атак для атаки 2

            self.damage_2.delete(0,END)
            self.damage_2.insert(0,data[13])   # загружается урона для атаки 2

            self.atk_bonus_2.delete(0,END)
            self.atk_bonus_2.insert(0,data[14])  # загружается бонус атаки для атаки 2



            self.atk_counter_3.delete(0,END)
            self.atk_counter_3.insert(0,data[15])   # загружается количество атак для атаки 3

            self.damage_3.delete(0,END)
            self.damage_3.insert(0,data[16])   # загружается урона для атаки 2

            self.atk_bonus_3.delete(0,END)
            self.atk_bonus_3.insert(0,data[17])  # загружается бонус атаки для атаки 3



            self.txt_dice_bucket.delete(0,END)
            self.txt_dice_bucket.insert(0,data[18])  # урон от аое-спелла

            # загрузка описания
            self.description_textbox.delete('1.0', END)
            self.description_textbox.insert(INSERT, data[19])
            #====================================================================


        if conn_to_load:
            conn_to_load.close()
            print("Connection closed")
#=================================================================================================================================================

    def click(self):
        self.battlelog.insert(INSERT, self.stat+str(randint(1,20)+self.mod))



    def clear_button_click(self):
        self.battlelog.delete('1.0', END)

    def description_button_click(self):
        self.clicked_counter +=1
        if self.clicked_counter % 2 == 1:
            self.geometry("510x520")  # изменяются размеры окна
        else:
            self.geometry("510x260")  # изменяются размеры окна

