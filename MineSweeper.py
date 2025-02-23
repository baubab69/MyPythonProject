import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror


COLORS = {
    0:'white',
    1:'blue',
    2:'red',
    3:'green',
    4:'#FF8A00',
    5:'#FF00FE',
    6:'#8DD16F',
    7:'#8D5C6F',
    8:'pink'
}


class MyButton(tk.Button):


    def __init__(self, master, x, y, number=0, count_bomb = 0, *args, **kwargs):
        super(MyButton, self).__init__(master, font = 'Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mines = False
        self.count_bomb = count_bomb
        self.is_open = False

    def __repr__(self):
        return f'MyButton {self.x} {self.y} {self.number} {self.is_mines}'
    

class MineSweeper:

    window = tk.Tk()
    ROW = 15
    COLUMN = 10
    MINES = 15
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW+2):
            temp = []
            for j in range(MineSweeper.COLUMN+2):
                btn = MyButton(MineSweeper.window, width = 3, x = i, y = j, number = 0)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                btn.bind('<Button-3>', self.right_click)
            self.buttons.append(temp)  

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
            cur_btn['disabledforeground'] = ['red']
        elif cur_btn['text'] == '🚩':
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ''

    def click(self, clicked_button: MyButton):
        if MineSweeper.IS_GAME_OVER:
            return 
        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False
        if clicked_button.is_mines:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Вы проиграли!')
            for i in range(1, MineSweeper.ROW+1):
                for j in range(1, MineSweeper.COLUMN+1):
                    btn = self.buttons[i][j]
                    if btn.is_mines:
                        btn['text'] = '*'
        elif clicked_button.count_bomb in COLORS:
            color = COLORS.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn] 
        while queue:
            cur_btn = queue.pop()
            color = COLORS.get(cur_btn.count_bomb, 'black')

            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            
            else:
                cur_btn.config(text='', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)
            
            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx - dy) == 1:
                        #     continue

                        next_x, next_y = x + dx, y + dy
                        if 1 <= next_x <= MineSweeper.ROW and 1 <= next_y <= MineSweeper.COLUMN:
                            next_btn = self.buttons[next_x][next_y]
                            if not next_btn.is_open and next_btn not in queue:
                                queue.append(next_btn)

    def reload(self):
        for child in self.window.winfo_children():
            child.destroy()
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def create_win_settings(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        
        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        row_entry.insert(0, MineSweeper.ROW)
        tk.Label(win_settings, text='Количество столбьцов').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        column_entry.insert(0, MineSweeper.COLUMN)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        mines_entry.insert(0, MineSweeper.MINES)

        save_btn = tk.Button(win_settings, text='Применить', 
                  command=lambda : self.change_settings(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы выели неправильное занчение!')
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMN = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()
    def create_widgets(self):
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_win_settings)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)
        count = 1
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMN+1):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, stick = 'NWES') 
                btn.number = count
                count += 1

        for i in range(1, MineSweeper.ROW+1):
            tk.Grid.rowconfigure(self.window, i, weight = 1)
        for i in range(1, MineSweeper. COLUMN+1):
            tk.Grid.columnconfigure(self.window, i, weight = 1)
        
    def start(self):
        self.create_widgets()
        MineSweeper.window.title('Mine Sweeper')
        MineSweeper.window.mainloop()

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMN+1):
                btn = self.buttons[i][j]
                if btn.is_mines:
                    print('b', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):
        index_mines = self.get_mines_place(number)
        print(index_mines)
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMN+1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mines = True 

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW+1):
            for j in range(1, MineSweeper.COLUMN+1):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mines:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mines:
                                count_bomb += 1
                btn.count_bomb = count_bomb     

    @staticmethod
    def get_mines_place(excludet_number: int):
        indexes = list(range(1, MineSweeper.ROW * MineSweeper.COLUMN + 1))
        indexes.remove(excludet_number)
        shuffle(indexes)
        return indexes[:MineSweeper.MINES]

game = MineSweeper()
game.start() 
