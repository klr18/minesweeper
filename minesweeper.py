import tkinter as tk  # импортируем графическую библиотеку Tkinter
from random import shuffle  # импортируем функцию shuffle из модуля random
from tkinter.messagebox import showinfo, showerror  # импортируем showinfo и showerror из модуля tkinter.messagebox

colors = {
    1: '#e44aa8',
    2: '#49e3d9',
    3: '#49e360',
    4: '#e34949',
    5: '#4b49e3',
    6: '#e3e349',
    7: '#b049e3',
    8: '#ff00ba',
}  # словарь, хранящий цвета для каждого значения кнопки


class MyButton(tk.Button):  # класс, наследуемый от класса tk.Button

    def __init__(self, master, x, y, number=0, *args, **kwargs):  # переопределение метода init для инициализации
        # дополнительных данных кнопки
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)  # вызываем init
        # у самой кнопки (tk.Button)
        self.x = x  # присваиваем кнопке координату по x
        self.y = y  # присваиваем кнопке координату по y
        self.number = number  # присваиваем кнопке собственный порядковый номер
        self.is_mine = False  # проверка, является ли кнопка бомбой
        self.count_bomb = 0  # количество бомб по соседству
        self.is_open = False  # проверка, открыта ли кнопка


class MineSweeper:  # основной класс для экземпляра игры

    window = tk.Tk()  # с помощью объекта класса Tk создаем главное окно
    rows = 10  # количество строк на игровом поле
    cols = 16  # количество столбцов на игровом поле
    mines = 20  # количество мин на игровом поле
    is_game_over = False  # проверка, закончилась ли игра
    is_first_click = True  # проверка, кликнул ли пользователь мышкой с момента начала игры

    def __init__(self):  # переопределение метода init для инициализации данных игры
        self.buttons = []  # список, хранящий кнопки поля
        for i in range(MineSweeper.rows + 2):
            temp = []
            for j in range(MineSweeper.cols + 2):  # циклы для создания двумерного списка
                btn = MyButton(MineSweeper.window, x=i, y=j)  # создаем экземпляр класса MyButton
                btn.config(command=lambda button=btn: self.click(button))  # обработка нажатия кнопки
                btn.bind('<Button-3>', self.right_click)  # связывает виджет (кнопку),
                # событие (нажатие правой кнопки мыши) и действие (метод)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):  # вызывается при нажатии правой кнопки мыши
        if MineSweeper.is_game_over:  # не срабатывает, если игра закончена
            return
        cur_btn = event.widget  # кнопка, которую нажали
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disable'  # переход обычной кнопки в статичное состояние (нельзя нажать)
            cur_btn['text'] = '🚩'  # рисуем красный флажок на данной кнопке
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '🚩':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'  # возвращаем кнопку в обычное состояние

    def click(self, clicked_button: MyButton):  # обработка нажатия кнопки
        if MineSweeper.is_game_over:  # не срабатывает, если игра закончена
            return None

        if MineSweeper.is_first_click:  # если со времени начала игры это первый клик мышкой
            self.insert_mines(clicked_button.number)  # минирование кнопок
            self.count_mines_in_buttons()  # подсчет заминированных соседей
            self.print_buttons()  # вывод вспомогательной таблицы на консоль
            MineSweeper.is_first_click = False

        if clicked_button.is_mine:  # если кнопка заминирована
            clicked_button.config(text='*', background='red', disabledforeground='black')  # изменение вида кнопки
            clicked_button.is_open = True  # открытие кнопки
            MineSweeper.is_game_over = True  # завершение игры
            showinfo('game over', 'вы проиграли')  # вывод сообщения о проигрыше
            for i in range(1, MineSweeper.rows + 1):
                for j in range(1, MineSweeper.cols + 1):  # циклы по кнопкам, кроме крайних
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'  # открытие всех заминированных полей
        else:  # если кнопка не заминирована
            color = colors.get(clicked_button.count_bomb, 'black')  # достаем из словаря colors нужный цвет
            if clicked_button.count_bomb:  # если число соседних мин не равно 0
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)  # придаем кнопке
                # нужный вид
                clicked_button.is_open = True  # открываем кнопку
            else:  # если число соседних мин равно 0
                self.breadth_first_search(clicked_button)  # вызываем алгоритм поиска в ширину
        clicked_button.config(state='disabled')  # делаем кнопку статичной
        clicked_button.config(relief=tk.SUNKEN)  # меняем рельеф кнопки

    def breadth_first_search(self, btn: MyButton):  # алгоритм поиска в ширину
        queue = [btn]  # создаем список из необработанных кнопок
        while queue:  # пока список не пустой
            cur_btn = queue.pop()  # вынимаем из него элемент
            color = colors.get(cur_btn.count_bomb, 'black')  # достаем из словаря colors нужный цвет
            if cur_btn.count_bomb:  # если среди соседей есть заминированные
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)  # кнопка с номером
            else:
                cur_btn.config(text='', disabledforeground=color)  # пустая кнопка
            cur_btn.is_open = True  # открываем кнопку
            cur_btn.config(state='disabled')  # делаем кнопку статичной
            cur_btn.config(relief=tk.SUNKEN)  # меняем рельеф кнопки

            if cur_btn.count_bomb == 0:  # если вокруг нет заминированных кнопок
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:  # цикл по всем соседям кнопки
                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.rows and \
                                1 <= next_btn.y <= MineSweeper.cols and next_btn not in queue:  # если кнопка еще не
                            # открыта, если она не крайняя и если она еще не в списке
                            queue.append(next_btn)  # добавить ее в список

    def reload(self):  # перезапуск игры
        [child.destroy() for child in self.window.winfo_children()]  # удаление всех компонентов на главном окне
        self.__init__()  # инициализация новых данных игры
        self.create_widgets()  # создание новых виджетов
        MineSweeper.is_first_click = True
        MineSweeper.is_game_over = False  # сброс до значения по умолчанию основных переменных

    def create_settings_window(self):
        win_settings = tk.Toplevel(self.window)  # создание дочернего окна
        win_settings.title('настройки')  # определяем заголовок окна

        tk.Label(win_settings, text='количество строк').grid(row=0, column=0)  # текст для поля ввода строк
        rows_entry = tk.Entry(win_settings)  # создаем поле ввода строк
        rows_entry.insert(0, MineSweeper.rows)  # наполнение поля ввода строк содержимым
        rows_entry.grid(row=0, column=1, padx=20, pady=20)  # вставка поля ввода в окно по индексу

        tk.Label(win_settings, text='количество столбцов').grid(row=1, column=0)  # текст для поля ввода столбцов
        cols_entry = tk.Entry(win_settings)  # создаем поле ввода столбцов
        cols_entry.insert(0, MineSweeper.cols)  # наполнение поля ввода столбцов содержимым
        cols_entry.grid(row=1, column=1, padx=20, pady=20)  # вставка поля ввода в окно по индексу

        tk.Label(win_settings, text='количество мин').grid(row=2, column=0)  # текст для поля ввода мин
        mines_entry = tk.Entry(win_settings)  # создаем поле ввода мин
        mines_entry.insert(0, MineSweeper.mines)  # наполнение поля ввода мин содержимым
        mines_entry.grid(row=2, column=1, padx=20, pady=20)  # вставка поля ввода в окно по индексу

        save_btn = tk.Button(win_settings, text='применить',
                  command=lambda :self.change_settings(rows_entry, cols_entry, mines_entry))  # кнопка сохранения
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)  # параметры кнопки сохранения

    def change_settings(self, row: tk.Entry, col: tk.Entry, mine: tk.Entry):  # изменение настроек
        try:  # проверка типа введенных значений
            int(row.get()), int(col.get()), int(mine.get())
        except ValueError:
            showerror('ошибка', 'вы ввели неправильное значение')  # открываем диалоговое окно с ошибкой
            return
        MineSweeper.rows = int(row.get())
        MineSweeper.cols = int(col.get())
        MineSweeper.mines = int(mine.get())  # присваивание полям введенных значений
        self.reload()  # перезапуск игры

    def create_widgets(self):  # создаем необходимые виджеты
        menubar = tk.Menu(self.window)  # создание главной полоски меню на основном окне
        self.window.config(menu=menubar)  # располагаем меню на основном окне

        settings_menu = tk.Menu(menubar, tearoff=0)  # создание пунктов в меню
        settings_menu.add_command(label='играть', command=self.reload)
        settings_menu.add_command(label='настройки', command=self.create_settings_window)
        settings_menu.add_command(label='выход', command=self.window.destroy)  # добавление кнопок и сопоставление
        # им определенных функций
        menubar.add_cascade(label='файл', menu=settings_menu)  # передаем settings_menu в menubar и формируем
        # выпадающий список

        count = 1
        for i in range(1, MineSweeper.rows + 1):
            for j in range(1, MineSweeper.cols + 1):  # циклы по всем кнопкам, кроме крайних
                btn = self.buttons[i][j]
                btn.number = count  # присваиваем каждой кнопке порядковый номер
                btn.grid(row=i, column=j, stick='NWES')  # размещаем кнопку в ячейках
                count += 1

        for i in range(1, MineSweeper.rows + 1):  # установка каждому ряду фиксированного размера на окне
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for i in range(1, MineSweeper.cols + 1):  # установка каждому столбцу фиксированного размера на окне
            tk.Grid.columnconfigure(self.window, i, weight=1)

    def print_buttons(self):  # выводим вспомогательную таблицу на консоль (прототип информации на игровом поле)
        for i in range(1, MineSweeper.rows + 1):
            for j in range(1, MineSweeper.cols + 1):  # циклы по всем кнопкам, кроме крайних
                btn = self.buttons[i][j]
                if btn.is_mine:  # если кнопка заминирована
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    @staticmethod
    def get_mines_places(exclude_number: int):  # определяем, какие кнопки будут заминированы
        indexes = list(range(1, MineSweeper.cols * MineSweeper.rows + 1))  # список с порядковыми номерами всех кнопок
        indexes.remove(exclude_number)  # удаляем номер кнопки, на которую мы нажали в начале игры
        shuffle(indexes)  # перемешиваем элементы в списке
        return indexes[:MineSweeper.mines]  # возвращаем срез с необходимым количеством рандомных элементов

    def insert_mines(self, number: int):  # минирование кнопок
        index_mines = self.get_mines_places(number)  # получаем номера заминированных кнопок
        print(index_mines)  # печатаем их на консоль
        for i in range(1, MineSweeper.rows + 1):
            for j in range(1, MineSweeper.cols + 1):  # циклы по кнопкам, кроме крайних
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True  # изменяем состояние кнопки, она становится заминированной

    def count_mines_in_buttons(self):  # подсчет соседних заминированных ячеек
        for i in range(1, MineSweeper.rows + 1):
            for j in range(1, MineSweeper.cols + 1):  # циклы по кнопкам, кроме крайних
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:  # если кнопка не заминирована
                    for row_d in [-1, 0, 1]:
                        for col_d in [-1, 0, 1]:  # циклы для перебора всех соседей с разницей в 1 координату
                            neighbour = self.buttons[i + row_d][j + col_d]
                            if neighbour.is_mine:  # если эта соседняя ячейка заминирована
                                count_bomb += 1  # увеличиваем счетчик соседних мин
                btn.count_bomb = count_bomb  # каждой кнопке присваиваем количество заминированных соседей

    def start(self):  # метод для старта игры
        self.create_widgets()  # создаем необходимые виджеты для игры
        MineSweeper.window.mainloop()  # вызываем обработчик событий у основного окна


game = MineSweeper()  # создаем экземпляр класса MineSweeper
game.start()  # у данного экземпляра вызываем метод start