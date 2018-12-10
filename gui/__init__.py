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
        self.style.configure('TCombobox', postoffset=(0,0,400,0))

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
        s = ttk.Button(self.tabs.account_tab, text="Save all changes", command=self.save_account)
        s.grid(column=1, row=99)
        self.tabs.configure_stash_frame()

    def save_account(self):
        for partition, data in self.tabs.part_textvars.items():
            partition = int(partition)
            plvl = getattr(data['plvl'], 'get')
            plvl = int(plvl())
            plvl_touple = (-4093, plvl)
            rift = getattr(data['rift'], 'get')
            rift = int(rift())
            rift_touple = (-4077, rift)
            # Saving corrupted saves...
            attrlist = {}
            for attr in self.account.asd.partitions[partition].saved_attributes.attributes:
                if not attr.value == -4093:
                    attrlist[str(attr.key)] = attr.value
            self.account.asd.partitions[partition].saved_attributes.Clear()
            for attr, value in attrlist.items():
                self.account.set_attribute(partition, (int(attr), int(value)))
            self.account.set_attribute(partition, plvl_touple)
            self.account.set_attribute(partition, rift_touple)
            self.account.asd.partitions[partition].alt_level = plvl
            pcurrencies = self.account.asd.partitions[partition].currency_data.currency
            for currency in pcurrencies:
                amount = int(getattr(data['currencies'][str(currency.id)], 'get')())
                currency.count = amount

        self.account.commit_account_changes()
        # TODO: change this to just a toast confirming saved changes.
        self.destroy_loaded_view()
        self.draw_welcome("Account data saved.")

    def savehero(self):
        hid = self.tabs.active_hid
        name = getattr(self.tabs.active_hero_data['Name'], 'get')
        level = getattr(self.tabs.active_hero_data['Level'], 'get')
#        rift = getattr(self.tabs.active_hero_data['Highest Solo Rift'], 'get')
        self.account.heroes[hid].digest.hero_name = name()
        self.account.heroes[hid].digest.level = int(level())
#        self.account.heroes[hid].digest.highest_solo_rift_completed = int(rift())
        attrs = self.account.heroes[hid].saved_attributes.attributes
        at_found = False
        for at in attrs:
            if at.key == -4016:
                at.value = int(level())
                at_found = True
        if not at_found:
            newat = attrs.add()
            newat.key = -4016
            newat.value = int(level())
        saved = self.account.commit_hero_changes(hid)
        self.tabs.hero_tab_message("Hero saved as: {}".format(saved.split('/')[-1]))

    def start(self):
        self.main_window.mainloop()
        sys.exit(0)
