import save_manager
import sys
import tkinter as tk
from settings import currency_list
from tkinter import filedialog
from tkinter import ttk


class D3Edit(object):
    def __init__(self):
        self.current_file = None
        self.main_window = tk.Tk()
        self.main_window.title("D3Edit")
        self.drawn_elements = []
        self.draw_first_view()

    def draw_first_view(self):
        self.first_label = ttk.Label(self.main_window, text="Account not loaded, please load an account file to begin.")
        self.first_label.grid(column=0, row=0)
        self.drawn_elements.append(self.first_label)
        self.open_button = ttk.Button(self.main_window, text="Open File", command=self.openfile)
        self.open_button.grid(column=0, row=1)
        self.drawn_elements.append(self.open_button)

    def destroy_loaded_view(self):
        while len(self.drawn_elements):
            item = self.drawn_elements.pop()
            item.destroy()

    def openfile(self):
        selected_file = filedialog.askopenfilename(initialdir=".", title="Select account.dat file")
        if selected_file:
            if self.current_file:
                self.previous_file = self.current_file
            self.current_file = selected_file
            self.first_label.configure(text=self.current_file)
            self.loadaccount(self.current_file)

    def loadaccount(self, file):
        self.account = save_manager.SaveData(file)
        self.destroy_loaded_view()
        self.draw_account_view()

    def draw_account_view(self):
        self.account_header = ttk.Label(text=self.current_file).grid(column=0, row=0)
        self.drawn_elements.append(self.account_header)
        self.currency_button = ttk.Button(self.main_window, text="Currencies").grid(column=0, row=1)
        self.drawn_elements.append(self.currency_button)
        self.sccurrencies = self.account.asd.partitions[0].currency_data.currency
        self.currtitles = {}
        self.currvalues = {}
        self.currvalentry = {}
        startcol = 0
        startrow = 2
        print(currency_list)
        for currency in self.sccurrencies:
            currid = str(currency.id)
            self.currvalues[currid] = tk.StringVar(value=currency.count)
            self.currtitles[currid] = ttk.Label(self.main_window, text=currency_list[currid])\
                .grid(column=startcol, row=startrow, sticky='W')
            self.currvalentry[currid] = ttk.Entry(
                self.main_window, textvariable=self.currvalues[currid])\
                .grid(column=(startcol + 1), row=startrow, sticky='W')
            startrow = startrow + 1
        self.drawn_elements.append(self.currtitles)
        self.drawn_elements.append(self.currvalentry)

    def start(self):
        self.main_window.mainloop()
        self.stop_gui()

    def stop_gui(self):
        sys.exit(0)
