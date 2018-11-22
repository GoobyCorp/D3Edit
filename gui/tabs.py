import tkinter as tk
from tkinter import ttk
from settings import currency_list


class Notebook(ttk.Notebook):
    def __init__(self, parent, account):
        self.account = account
        self.tabs = ttk.Notebook(parent)
        self.account_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.hero_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.stash_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.tabs.add(self.account_tab, text="Account")
        self.tabs.add(self.hero_tab, text="Heroes")
        self.tabs.add(self.stash_tab, text="Stash")
        self.tabs.pack(expan=1, fill="both")
        # dictionary holding textvariables for Entry fields
        self.scvalues = {}
        self.hcvalues = {}
        self.heroes = None
        self.active_hid = None
        self.active_hero_name = "No - Hero"
        self.active_hero_data = {}
        self.active_hero_frame = ttk.Frame(self.hero_tab, style="TNotebook", borderwidth=0)
        self.heroframes = None
        self.active_stash_frame = None
        self.active_stash = tk.StringVar(value='SC')
        self.stash_data = None
        self.item_list_frame = None
        self.item_frame = None
        self.configure_account_tab()
        self.configure_stash_frame()
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

    def load_hero_frame(self, event=None):
        if event:
            self.active_hero_frame.destroy()
            self.active_hero_frame = ttk.Frame(self.hero_tab, style="TNotebook", borderwidth=0)
            self.active_hero_frame.grid(column=0, row=1)
        c = ttk.Combobox(self.active_hero_frame, textvariable=self.active_hero_name,
                         values=self.heroes, state='readonly')
        c.grid(column=1, row=0)
        c.bind("<<ComboboxSelected>>", self.load_hero_frame)
        self.active_hid = self.active_hero_name.get().split(" - ")[1]
        current_hero_data = self.account.heroes[self.active_hid]
        self.active_hero_data['Name'] = tk.StringVar(value=current_hero_data.digest.hero_name)
        self.active_hero_data['Level'] = tk.StringVar(value=current_hero_data.digest.level)
        self.active_hero_data['Highest Solo Rift'] = tk.StringVar(
            value=current_hero_data.digest.highest_solo_rift_completed)
        row = 1
        for key, value in self.active_hero_data.items():
            ttk.Label(self.active_hero_frame, text=key).grid(column=0, row=row, sticky='W')
            ttk.Entry(self.active_hero_frame, textvariable=self.active_hero_data[key]).grid(column=1, row=row)
            row = row + 1
        self.active_hero_frame.grid(column=0, row=0)

    def configure_hero_tab(self):
        self.heroes = ['{1} - {0}'.format(h, d.digest.hero_name) for h, d in self.account.heroes.items()]
        for hero in self.heroes:
            if hero.endswith(self.account.last_played_hero_id):
                self.active_hero_name = tk.StringVar(value=hero)
            else:
                self.active_hero_name = tk.StringVar(value=self.heroes[0])
        self.load_hero_frame()

    def hero_tab_message(self, message):
        ttk.Label(self.active_hero_frame, text=message).grid(column=1, row=98)

    def configure_stash_frame(self, event=None):
        if self.active_stash_frame:
            self.active_stash_frame.destroy()
        self.active_stash_frame = ttk.Frame(self.stash_tab, style="TNotebook", borderwidth=0)
        self.active_stash_frame.grid(column=0, row=0)
        c = ttk.Combobox(self.active_stash_frame, textvariable=self.active_stash, values=['SC', 'HC'], state='readonly')
        c.grid(column=0, row=0, sticky='NW', columnspan=2)
        c.bind("<<ComboboxSelected>>", self.configure_stash_frame)
        if self.active_stash.get() == 'SC':
            try:
                self.stash_data = self.account.asd.partitions[0].items.ListFields()[0][1]
            except IndexError:
                self.stash_data = None
        elif self.active_stash.get() == 'HC':
            try:
                self.stash_data = self.account.asd.partitions[1].items.ListFields()[0][1]
            except IndexError:
                self.stash_data = None
        else:
            assert "incorrect stash selected, stash has to be either SC or HC."
        if self.stash_data:
            self.load_item_list_frame(self.stash_data, self.active_stash_frame)

    def load_item_list_frame(self, itemlist, parent):
        if self.item_list_frame:
            self.item_list_frame.destroy()
        self.item_list_frame = ttk.Frame(parent, style="TNotebook", borderwidth=0)
        self.item_list_frame.grid(column=0, row=1, sticky='NESW')
        ttk.Label(self.item_list_frame, text="Item List:").grid(column=0, row=1, sticky='W')
        scrollbar = ScrollbarItems(itemlist, parent=self.item_list_frame)
        scrollbar.grid(column=0, row=2)
        scrollbar.listbox.bind('<Double-1>', lambda x: self.loaditemfromsb(itemlist, scrollbar, self.item_list_frame))

    def loaditemfromsb(self, itemlist, scrollbar, parent):
        index = scrollbar.listbox.curselection()[0]
        item = scrollbar.indexmap[index]
        print(item)
        self.load_item_frame(item, parent)

    def load_item_frame(self, item, parent):
        if self.item_frame:
            self.item_frame.destroy()
        self.item_frame = ttk.Frame(parent, style="TNotebook", borderwidth=0)
        self.item_frame.grid(row=2, column=1, sticky='NES')
        ttk.Label(self.item_frame, text=item).grid(sticky='NES')


class ScrollbarItems(ttk.Frame):
    def __init__(self, options, parent=None):
        ttk.Frame.__init__(self, parent)
        self.indexmap = {}
        self.parent = parent
        self.makewidgets(options)

    def makewidgets(self, options):
        sb = tk.Scrollbar(self)
        listing = tk.Listbox(self, relief='sunken')
        sb.config(command=listing.yview)
        listing.config(yscrollcommand=sb.set, height=35)
        sb.grid(row=0, column=1, sticky='ns')
        listing.grid(row=0, column=0, sticky='ns')
        curr_index = 0
        for item in options:
            sq_index = item.square_index
            listing.insert(curr_index, sq_index)
            self.indexmap[curr_index] = item
            curr_index = curr_index + 1
        self.listbox = listing
