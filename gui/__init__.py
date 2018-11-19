import save_manager
import sys
import tkinter as tk
from settings import currency_list
from tkinter import filedialog
from tkinter import ttk


class D3Edit(object):
    def __init__(self):
        message = None
        self.current_file = None
        self.main_window = tk.Tk()
        self.main_window.title("D3Edit")
        try:
            from google import protobuf
            del protobuf
        except:
            message = "Could not import protobuff, please install the protobuf python package."
        self.draw_welcome(message)

    def draw_welcome(self, message=None):
        if not message:
            message = "Account not loaded, please load an account file to begin."
        self.first_label = ttk.Label(self.main_window, text=message)
        self.first_label.grid(column=0, row=0)
        self.open_button = ttk.Button(self.main_window, text="Open File", command=self.openfile)
        self.open_button.grid(column=0, row=1)

    def destroy_loaded_view(self):
        self.main_window.destroy()
        self.main_window = tk.Tk()
        self.main_window.title("D3Edit")

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
        self.account.output_file = file
        self.destroy_loaded_view()
        self.draw_account_view()

    def savecurrencies(self):
        for currency in self.account.asd.partitions[0].currency_data.currency:
            amount = getattr(self.scvalues[str(currency.id)], 'get')
            currency.count = int(amount())
        self.account.commit_all_changes()
        self.destroy_loaded_view()
        self.draw_welcome("Account data saved.")

    def draw_account_view(self):
        self.account_header = ttk.Label(text=self.current_file).grid(column=0, row=0)
        self.currency_button = ttk.Button(self.main_window, text="Save Softcore Currencies",
                                          command=self.savecurrencies).grid(column=0, row=1)
        self.sccurrencies = self.account.asd.partitions[0].currency_data.currency
        self.scvalues = {}
        startcol = 0
        startrow = 2
        for currency in self.sccurrencies:
            currid = str(currency.id)
            self.scvalues[currid] = tk.StringVar(value=currency.count)
            ttk.Label(self.main_window, text=currency_list[currid]).grid(column=startcol, row=startrow, sticky='W')
            ttk.Entry(self.main_window, textvariable=self.scvalues[currid])\
                .grid(column=startcol, row=startrow, sticky='E')
            startrow = startrow + 1

    def start(self):
        self.main_window.mainloop()
        self.stop_gui()

    def stop_gui(self):
        sys.exit(0)
