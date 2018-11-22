import save_manager
import sys
import tkinter as tk
from gui import tabs
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
        self.main_window = None
        self.style = None
        self.account = None
        self.previous_file = None
        self.wcoords = None
        self.tabs = None
        self.setupframe()
        self.draw_welcome(message)

    def setupframe(self, wcoords=None):
        self.main_window = tk.Tk()
        self.main_window.title("D3Edit")
        self.main_window.minsize(600, 450)
        if wcoords:
            self.main_window.geometry("+{0}+{1}".format(wcoords[0], wcoords[1]))
        self.style = ttk.Style(self.main_window)
        self.style.theme_use('default')
        self.style.configure("TLabel", foreground="black", background="white")
        self.style.configure("TNotebook", background="white")

    def draw_welcome(self, message=None):
        if not message:
            message = "Account not loaded, please load an account file to begin."
        message_label = ttk.Label(self.main_window, text=message, style="TLabel")
        message_label.grid(column=0, row=0, sticky='NEW')
        message_label.configure(anchor='center')
        open_file = ttk.Button(self.main_window, text="Open File", command=self.openfile)
        open_file.place(rely=0.5, relx=0.5, anchor='center')

    def destroy_loaded_view(self):
        wcoords = (self.main_window.winfo_x(), self.main_window.winfo_y())
        self.main_window.destroy()
        self.setupframe(wcoords)

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
        self.tabs = tabs.Notebook(self.main_window, account=self.account)
        if self.account.heroes:
            self.tabs.configure_hero_tab()
            ttk.Button(self.tabs.hero_tab, text="Save Hero", command=self.savehero).grid(column=0, row=99)
        s = ttk.Button(self.tabs.account_tab, text="Save all changes", command=self.savechanges)
        s.grid(column=1, row=99)

    def savechanges(self):
        for currency in self.account.asd.partitions[0].currency_data.currency:
            amount = getattr(self.tabs.scvalues[str(currency.id)], 'get')
            currency.count = int(amount())
        for currency in self.account.asd.partitions[1].currency_data.currency:
            amount = getattr(self.tabs.hcvalues[str(currency.id)], 'get')
            currency.count = int(amount())
        scplvl = getattr(self.tabs.scvalues['plvl'], 'get')
        scplvl = int(scplvl())
        hcplvl = getattr(self.tabs.hcvalues['plvl'], 'get')
        hcplvl = int(hcplvl())
        self.account.set_attribute(0, (-4093, scplvl))
        self.account.set_attribute(1, (-4093, hcplvl))
        self.account.asd.partitions[0].alt_level = scplvl
        self.account.asd.partitions[1].alt_level = hcplvl
        self.account.commit_account_changes()
        self.destroy_loaded_view()
        self.draw_welcome("Account data saved.")

    def savehero(self):
        hid = self.tabs.active_hid
        name = getattr(self.tabs.active_hero_data['Name'], 'get')
        level = getattr(self.tabs.active_hero_data['Level'], 'get')
        rift = getattr(self.tabs.active_hero_data['Highest Solo Rift'], 'get')
        self.account.heroes[hid].digest.hero_name = name()
        self.account.heroes[hid].digest.level = int(level())
        self.account.heroes[hid].digest.highest_solo_rift_completed = int(rift())
        saved = self.account.commit_hero_changes(hid)
        self.tabs.hero_tab_message("Hero saved as: {}".format(saved.split('/')[-1]))

    def start(self):
        self.main_window.mainloop()
        sys.exit(0)
