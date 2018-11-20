import save_manager
import sys
import tkinter as tk
from settings import currency_list
from tkinter import filedialog
from tkinter import ttk


class D3Edit(object):
    def __init__(self):
        message = None
        try:
            from google import protobuf
            del protobuf
        except ImportError:
            protobuf = None
            message = "Could not import protobuff, please install the protobuf python package."
        self.current_file = None
        self.scvalues = {}
        self.hcvalues = {}
        self.sccurrencies = None
        self.hccurrencies = None
        self.scparagon = None
        self.hcparagon = None
        self.main_window = None
        self.style = None
        self.account = None
        self.previous_file = None
        self.wcoords = None
        self.setupframe()
        self.draw_welcome(message)

    def setupframe(self):
        self.main_window = tk.Tk()
        self.main_window.title("D3Edit")
        self.main_window.minsize(600, 450)
        if self.wcoords:
            self.main_window.geometry("+{0}+{1}".format(self.wcoords[0], self.wcoords[1]))
        self.style = ttk.Style(self.main_window)
        self.style.theme_use('default')
        self.style.configure("TLabel", foreground="black", background="white")

    def draw_welcome(self, message=None):
        if not message:
            message = "Account not loaded, please load an account file to begin."
        message_label = ttk.Label(self.main_window, text=message, style="TLabel")
        message_label.grid(column=0, row=0, sticky='NEW')
        message_label.configure(anchor='center')
        open_file = ttk.Button(self.main_window, text="Open File", command=self.openfile)
        open_file.place(rely=0.5, relx=0.5, anchor='center')

    def destroy_loaded_view(self):
        self.wcoords = (self.main_window.winfo_x(), self.main_window.winfo_y())
        self.main_window.destroy()
        self.setupframe()

    def openfile(self):
        selected_file = filedialog.askopenfilename(initialdir=".", title="Select account.dat file")
        if selected_file:
            if self.current_file:
                self.previous_file = self.current_file
            self.current_file = selected_file
            self.loadaccount(self.current_file)

    def loadaccount(self, file):
        self.account = save_manager.SaveData(file)
        self.account.output_file = file
        self.destroy_loaded_view()
        self.draw_account_view()

    def savechanges(self):
        for currency in self.account.asd.partitions[0].currency_data.currency:
            amount = getattr(self.scvalues[str(currency.id)], 'get')
            currency.count = int(amount())
        for currency in self.account.asd.partitions[1].currency_data.currency:
            amount = getattr(self.hcvalues[str(currency.id)], 'get')
            currency.count = int(amount())
        scplvl = getattr(self.scvalues['plvl'], 'get')
        hcplvl = getattr(self.hcvalues['plvl'], 'get')
        self.account.asd.partitions[0].alt_level = int(scplvl())
        self.account.asd.partitions[1].alt_level = int(hcplvl())
        self.account.commit_all_changes()
        self.destroy_loaded_view()
        self.draw_welcome("Account data saved.")

    def draw_account_view(self):
        message_label = ttk.Label(self.main_window, text=self.current_file, style="TLabel")
        message_label.grid(column=0, row=0)
        ttk.Label(text=self.current_file, style="TLabel").grid(column=0, row=0)
        self.sccurrencies = self.account.asd.partitions[0].currency_data.currency
        self.hccurrencies = self.account.asd.partitions[1].currency_data.currency
        startcol = 0
        startrow = 3
        ttk.Label(self.main_window, text="Softcore").grid(column=0, row=2, sticky='E', padx=128)
        ttk.Label(self.main_window, text="Hardcore").grid(column=1, row=2, sticky='W')
        self.scparagon = self.account.asd.partitions[0].alt_level
        self.scvalues['plvl'] = tk.StringVar(value=self.scparagon)
        self.hcparagon = self.account.asd.partitions[1].alt_level
        self.hcvalues['plvl'] = tk.StringVar(value=self.hcparagon)
        ttk.Label(self.main_window, text="Paragon Level").grid(column=startcol, row=startrow, sticky='W')
        ttk.Entry(self.main_window, textvariable=self.scvalues['plvl']).grid(column=startcol, row=startrow, sticky='E')
        for currency in self.sccurrencies:
            startrow = startrow + 1
            currid = str(currency.id)
            self.scvalues[currid] = tk.StringVar(value=currency.count)
            ttk.Label(self.main_window, text=currency_list[currid]).grid(column=startcol, row=startrow, sticky='W')
            ttk.Entry(self.main_window, textvariable=self.scvalues[currid])\
                .grid(column=startcol, row=startrow, sticky='E')
        startcol = 1
        startrow = 3
        ttk.Entry(self.main_window, textvariable=self.hcvalues['plvl']).grid(column=startcol, row=startrow, sticky='W')
        for currency in self.hccurrencies:
            startrow = startrow + 1
            currid = str(currency.id)
            self.hcvalues[currid] = tk.StringVar(value=currency.count)
            ttk.Label(self.main_window, text=currency_list[currid]).grid(column=startcol, row=startrow, sticky='W')
            ttk.Entry(self.main_window, textvariable=self.hcvalues[currid])\
                .grid(column=startcol, row=startrow, sticky='E')
        ttk.Button(self.main_window, text="Save all changes",
                   command=self.savechanges).grid(column=0, row=99, sticky='E', padx=40)

    def start(self):
        self.main_window.mainloop()
        sys.exit(0)
