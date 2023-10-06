from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext, filedialog
import tkinter.filedialog as fd
from random import randint
import re



class Window(Tk):  # описание окна карточки моба
    def __init__(self): # инициализация
        super().__init__()

        # конфигурация окна
        self.title("Новый моб")  # название окна
        self.geometry("500x200")  # размеры окна
        self.make_the_thole_grid()  # вызыв функции для отрисовки всех элементов окна



    def make_the_thole_grid(self):  # функция отрисовки окна. В скобочках - строка, на которой будет отрисовываться строка

        self.add_information_row(0)  # имя, кд и лог боя
        self.add_hp_row(1)  # хп моба, текстбоксы для подсчёта урона и кнопка вычитания
        self.add_comments_row(2)  # комментарии для таблицы атак

        self.add_attack_1_row(3)  # строка атак 1
        #attack_row_2 =  self.add_attack_1_row(4)
        self.add_attack_2_row(4)  # строка атак 2
        self.add_attack_3_row(5)  # строка атак 3
        self.add_dice_bucket_row(6)  # строка броска ведра кубов
        self.add_options_row(7)  # опции сохранения, загрузки и очистки лога

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
        self.battlelog = scrolledtext.ScrolledText(self, width=20, height=10)
        self.battlelog.place(x=300, y=0)


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

    #======================= методы(или функции?) для совершения атак =============================================
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
    # функция(метод?) реализующая броски атаки и урона
    def roll_the_dices(self, damage_text_area, atk_bonus_area):  # принимает два аргумента: текстбокс с уроном и текстбокс с бонусом на атаку
        string = damage_text_area.get()  # получение значения из строки урона
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
            dice_to_roll = item.split('d')  # разделение на сколько и каких дайсов

            if atk_bonus_area != None:  # опять же, костыль на "заклинание ли это?". если не спелл, то:

                if atk_dice == 20:  # если попадание критическое,
                    dice_to_roll_total = int(dice_to_roll[0])*2  # то количество костей урона удваиваются
                else:
                    dice_to_roll_total = int(dice_to_roll[0])  # если не крит, то не удиваиваются

            else:
                dice_to_roll_total = int(dice_to_roll[0])  # если спелл то считаем количество костей урона

            for i in range(0,dice_to_roll_total):  # для каждой кости урона делаем бросок
                total_damage_of_dices += randint(1, int(dice_to_roll[1]))  # считаем сколько выпало с каждой кости

        if atk_bonus_area != None:  # очередная костыльная проверка на то, не спелл ли это

            if re.findall("[+-]\d+",string)[0] != '':  # проверка, есть ли в строке модификатор характеристики для урона
                print("есть урон")
                return atk_value_string + str(total_damage_of_dices + int(re.findall("[+-]\d+",string)[0]))  # если модификатор есть, то добавляем его к урону и
                                                                                                             # и возвращаем значение урона
            else:
                return atk_value_string + str(total_damage_of_dices) # если нет, то просто возвращаем значение урона на костях

        else:
            return "Урон: " + str(total_damage_of_dices)  # если спелл, то тоже просто возвращаем значение урона на костях. Заклинания же не критуют


    #def change_name(self):
    #    self.label.configure(text=self.txt.get())

    #====================== строка опций: ===============================================
    def add_options_row(self, pos):

        # отрисовка кнопки загрузки
        self.load_button = ttk.Button(self, text="Загрузить")
        self.load_button["command"] = self.load_button_click
        self.load_button.grid(column=0, row=pos)

        # отрисовка кнопки сохранения
        self.save_button = ttk.Button(self, text="Сохранить")
        self.save_button["command"] = self.save_button_click
        self.save_button.grid(column=1, row=pos)

        # отрисовка кнопки очистки лога
        self.clear_button = ttk.Button(self, text="Очистить")
        self.clear_button["command"] = self.clear_button_click
        self.clear_button.grid(column=4, row=pos)

    """
    Наверняка существует более элегантное решение чтения из текстового файла строк и записи их в каждое окошко
    """
    # описание логики кнопки загрузки:
    def load_button_click(self):
        # вызов диалогового окна для выбора .txt файла для чтения
        file = fd.askopenfilename(parent=root, title='Выберите', filetypes = (("Текстовые файлы", "*.txt"),))

        if file != "":  # если файл выбран
            with open(file, 'r') as fp:  # открывается файл и построчно читается

                """ниже для каждого текстбокса сначала удаляется значение
                а затем вставляется строка кроме последнего символа - \n"""
                self.txt.delete(0, END)
                self.txt.insert(0,fp.readline()[0:-1])  # загружается имя моба
                self.title(self.txt.get())  # загружается имя моба и переименовывается окно

                self.AC_txt.delete(0,END)
                self.AC_txt.insert(0, fp.readline()[0:-1])   # загружается Кд

                self.HP_current_txt.delete(0,END)
                self.HP_current_txt.insert(0, fp.readline()[0:-1])  # загружается ХП



                self.atk_counter_1.delete(0,END)
                self.atk_counter_1.insert(0, fp.readline()[0:-1])   # загружается количество атак для атаки 1

                self.damage_1.delete(0,END)
                self.damage_1.insert(0, fp.readline()[0:-1])   # загружается урона для атаки 1

                self.atk_bonus_1.delete(0,END)
                self.atk_bonus_1.insert(0, fp.readline()[0:-1])  # загружается бонус атаки для атаки 1



                self.atk_counter_2.delete(0,END)
                self.atk_counter_2.insert(0, fp.readline()[0:-1])   # загружается количество атак для атаки 2

                self.damage_2.delete(0,END)
                self.damage_2.insert(0, fp.readline()[0:-1])   # загружается урона для атаки 2

                self.atk_bonus_2.delete(0,END)
                self.atk_bonus_2.insert(0, fp.readline()[0:-1])  # загружается бонус атаки для атаки 2



                self.atk_counter_3.delete(0,END)
                self.atk_counter_3.insert(0, fp.readline()[0:-1])   # загружается количество атак для атаки 3

                self.damage_3.delete(0,END)
                self.damage_3.insert(0, fp.readline()[0:-1])   # загружается урона для атаки 2

                self.atk_bonus_3.delete(0,END)
                self.atk_bonus_3.insert(0, fp.readline()[0:-1])  # загружается бонус атаки для атаки 3



                self.txt_dice_bucket.delete(0,END)
                self.txt_dice_bucket.insert(0, fp.readline()[0:-1])  # урон от аое-спелла



    # описание кнопки сохранения карточки моба
    def save_button_click(self):
        file = open(self.txt.get()+'.txt', "w")  # создается и открывается для записи .txt файл с именем моба

        if file != "":  # проверка, что у моба есть имя
                # построчно записываются его имя, кд, хп, атаки и урон аое-спелла
                file.write(
                        self.txt.get() + '\n' + self.AC_txt.get() + '\n' + self.HP_current_txt.get() + '\n' +
                        self.atk_counter_1.get() + '\n' + self.damage_1.get() + '\n' + self.atk_bonus_1.get() + '\n' +
                        self.atk_counter_2.get() + '\n' + self.damage_2.get() + '\n' + self.atk_bonus_2.get() + '\n' +
                        self.atk_counter_3.get() + '\n' + self.damage_3.get() + '\n' + self.atk_bonus_3.get() + '\n' +
                        self.txt_dice_bucket.get() + '\n'
                           )
        file.close()  # закрытие файла

    # описание кнопки очистки лога
    def clear_button_click(self):
        self.battlelog.delete('1.0', END)

#========================== логика стартового окна =============================
root = Tk()  # создание стартового окна
root.title("Dungeon Master Helper")  # имя стартового окна
root.geometry("250x200")  # размеры стартового окна

# описание кнопки "добавить моба"
def click():
    window = Window()  # создается новый экземпляр класса Window

# описание и расположение кнопки "добавить моба"
open_button = ttk.Button(text="Добавить моба", command=click)
open_button.pack(anchor="center", expand=1)

root.mainloop()  # бесконечный цикл главного окна