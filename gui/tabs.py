import tkinter as tk
from tkinter import ttk
from settings import currency_list


class Notebook(ttk.Notebook):
    def __init__(self, parent, account):
        self.account = account
        self.tabs = ttk.Notebook(parent)
        self.account_tab = ttk.Frame(self.tabs, style="TNotebook")
        self.hero_tab = ttk.Frame(self.tabs, style="TNotebook")
        self.tabs.add(self.account_tab, text="Account")
        self.tabs.add(self.hero_tab, text="Heroes")
        self.tabs.pack(expan=1, fill="both")
        # dictionary holding textvariables for Entry fields
        self.scvalues = {}
        self.hcvalues = {}
        self.active_hero = None
        self.active_hero_data = {}
        self.active_hero_frame = tk.Frame(self.hero_tab)
        self.active_hero_frame.grid(column=0, row=1)
        self.heroframes = None
        self.configure_account_tab()
        self.configure_hero_tab()
        self.populate_sc_data()
        self.populate_hc_data()

    def configure_account_tab(self):
        ttk.Label(self.account_tab, text="Softcore").grid(column=1, row=0, sticky='E', padx=128)
        ttk.Label(self.account_tab, text="Hardcore").grid(column=2, row=0, sticky='W')
        ttk.Label(self.account_tab, text="Paragon Level").grid(column=0, row=1, sticky='W')
        for id, currency in currency_list.items():
            ttk.Label(self.account_tab, text=currency).grid(column=0, row=(int(id) + 5), sticky='W')

    def populate_sc_data(self):
        self.scvalues['plvl'] = tk.StringVar(value=self.account.asd.partitions[0].alt_level)
        ttk.Entry(self.account_tab, textvariable=self.scvalues['plvl']).grid(column=1, row=1, sticky='E')
        sccurrency = self.account.asd.partitions[0].currency_data.currency
        for currency in sccurrency:
            id = currency.id
            idstr = str(currency.id)
            self.scvalues[idstr] = tk.StringVar(value=currency.count)
            ttk.Entry(self.account_tab, textvariable=self.scvalues[idstr]).grid(column=1, row=(id + 5), sticky='E')

    def populate_hc_data(self):
        self.hcvalues['plvl'] = tk.StringVar(value=self.account.asd.partitions[1].alt_level)
        ttk.Entry(self.account_tab, textvariable=self.hcvalues['plvl']).grid(column=2, row=1, sticky='E')
        hccurrency = self.account.asd.partitions[1].currency_data.currency
        for currency in hccurrency:
            id = currency.id
            idstr = str(currency.id)
            self.hcvalues[idstr] = tk.StringVar(value=currency.count)
            ttk.Entry(self.account_tab, textvariable=self.hcvalues[idstr]).grid(column=2, row=(id + 5), sticky='E')

    def generate_hero_frame(self, event=None):
        if event:
            self.active_hero_frame.destroy()
            self.active_hero_frame = tk.Frame(self.hero_tab)
            self.active_hero_frame.grid(column=0, row=1)
        c = ttk.Combobox(self.active_hero_frame, textvariable=self.active_hero, values=self.heroes, state='readonly')
        c.grid(column=1, row=0)
        c.bind("<<ComboboxSelected>>", self.generate_hero_frame)
        active_hid = self.active_hero.get().split(" - ")[1]
        current_hero_data = self.account.heroes[active_hid]
        self.active_hero_data['name'] = tk.StringVar(value=current_hero_data.digest.hero_name)
        self.active_hero_data['level'] = tk.StringVar(value=current_hero_data.digest.level)
        self.active_hero_data['rift'] = tk.StringVar(value=current_hero_data.digest.highest_solo_rift_completed)
        hnamelabel = ttk.Label(self.active_hero_frame, text="Name")
        hnameentry = ttk.Entry(self.active_hero_frame, textvariable=self.active_hero_data['name'])
        hlevellabel = ttk.Label(self.active_hero_frame, text="Level")
        hlevelentry = ttk.Entry(self.active_hero_frame, textvariable=self.active_hero_data['level'])
        hriftlabel = ttk.Label(self.active_hero_frame, text="Highest Solo Rift")
        hriftentry = ttk.Entry(self.active_hero_frame, textvariable=self.active_hero_data['rift'])
        hnamelabel.grid(column=0, row=1, sticky='W')
        hnameentry.grid(column=1, row=1, sticky='W')
        hlevellabel.grid(column=0, row=2, sticky='W')
        hlevelentry.grid(column=1, row=2, sticky='W')
        hriftlabel.grid(column=0, row=3, sticky='W')
        hriftentry.grid(column=1, row=3, sticky='W')
        self.active_hero_frame.grid(column=0, row=0, sticky='NEWS')

    def configure_hero_tab(self):
        self.heroes = ['{1} - {0}'.format(h, d.digest.hero_name) for h, d in self.account.heroes.items()]
        for hero in self.heroes:
            if hero.endswith(self.account.last_played_hero_id):
                self.active_hero = tk.StringVar(value=hero)
            else:
                self.active_hero = tk.StringVar(value=hero[0])
        self.generate_hero_frame()
