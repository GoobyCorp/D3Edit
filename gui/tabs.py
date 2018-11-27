import tkinter as tk
from tkinter import ttk
from save_manager import item_handler
from settings import currency_list


class Notebook(ttk.Notebook):
    def __init__(self, parent, account):
        self.account = account
        self.tabs = ttk.Notebook(parent)
        self.account_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.account_frame = ttk.Frame(self.account_tab, style="TNotebook", borderwidth=0)
        self.hero_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.stash_tab = ttk.Frame(self.tabs, style="TNotebook", borderwidth=0)
        self.tabs.add(self.account_tab, text="Account")
        self.tabs.add(self.hero_tab, text="Heroes")
        self.tabs.add(self.stash_tab, text="Stash and Inventories")
        self.tabs.pack(expan=1, fill="both")
        # dictionary holding textvariables for Entry fields
        self.part_textvars = {}
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
        self.active_partition = tk.StringVar(value="Non Season")
        self.configure_account_tab()

    def configure_account_tab(self):
        for partition in self.account.asd.partitions:
            self.get_partition_data(partition)
        copt = ['Non Season', 'Season']
        c = ttk.Combobox(self.account_tab, textvariable=self.active_partition,
                         values=copt, state='readonly')
        c.grid(column=1, row=0)
        c.bind("<<ComboboxSelected>>", self.populate_account_frame)
        self.populate_account_frame()

    def populate_account_frame(self, event=None):
        if event:
            self.account_frame.destroy()
            self.account_frame = ttk.Frame(self.account_tab, style="TNotebook", borderwidth=0)
        self.account_frame.grid(column=1, row=1)
        ttk.Label(self.account_frame, text="Softcore").grid(column=1, row=1, sticky='E', padx=128)
        ttk.Label(self.account_frame, text="Hardcore").grid(column=2, row=1, sticky='W')
        ttk.Label(self.account_frame, text="Paragon Level").grid(column=0, row=1, sticky='W')
        for ids, currency in currency_list.items():
            ttk.Label(self.account_frame, text=currency).grid(column=0, row=(int(ids) + 5), sticky='W')
        offset = 0
        if self.active_partition.get() == "Season":
            offset = 2
        for m in (0, 1):
            coffset = str(offset + m)
            column = (1 + m)
            cp = self.part_textvars[coffset]
            ttk.Entry(self.account_frame, textvariable=cp['plvl']).grid(column=column, row=1, sticky='E')
            cc = cp['currencies']
            for ids in cc.keys():
                idi = int(ids)
                ttk.Entry(self.account_frame, textvariable=cc[ids]).grid(column=column, row=(idi + 5), sticky='E')

    def get_partition_data(self, partition):
        partition_id = str(partition.partition_id)
        self.part_textvars[partition_id] = {}
        current_partition = self.part_textvars[partition_id]
        current_partition['plvl'] = tk.StringVar(value=partition.alt_level)
        current_clist = current_partition['currencies'] = {}
        pcurrency_list = partition.currency_data.currency
        for currency in pcurrency_list:
            ids = currency.id
            idstr = str(ids)
            current_clist[idstr] = tk.StringVar(value=currency.count)

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
        stashvalues = ['SC', 'HC'] + self.heroes
        c = ttk.Combobox(self.active_stash_frame, textvariable=self.active_stash, values=stashvalues, state='readonly')
        c.grid(column=0, row=0, sticky='NW', columnspan=2)
        c.bind("<<ComboboxSelected>>", self.configure_stash_frame)
        if self.active_stash.get() == 'SC':
            try:
                self.stash_data = self.account.asd.partitions[0].items.items
            except IndexError:
                self.stash_data = None
        elif self.active_stash.get() == 'HC':
            try:
                self.stash_data = self.account.asd.partitions[1].items.items
            except IndexError:
                self.stash_data = None
        else:
            hero_id = self.active_stash.get().split(' - ')[1]
            self.stash_data = self.account.heroes[hero_id].items.items
        if self.stash_data:
            self.load_item_list_frame(self.stash_data, self.active_stash_frame)

    def load_item_list_frame(self, itemlist, parent):
        if self.item_list_frame:
            self.item_list_frame.destroy()
        self.item_list_frame = ttk.Frame(parent, style="TNotebook", borderwidth=0)
        self.item_list_frame.grid(column=0, row=1, sticky='NESW')
        ttk.Label(self.item_list_frame, text="Item List:").grid(column=0, row=1, sticky='W')
        parent.columnconfigure(1, weight=1)
        self.decodeditems = item_handler.decode_itemlist(itemlist)
        scrollbar = ScrollbarItems(self.decodeditems, parent=self.item_list_frame)
        scrollbar.grid(column=0, row=2)
        scrollbar.listbox.bind('<Double-1>', lambda x: self.load_item_frame(scrollbar, self.item_list_frame))

    def load_item_frame(self, scrollbar, parent):
        if self.item_frame:
            self.item_frame.destroy()
        index = scrollbar.listbox.curselection()[0]
        entry = scrollbar.indexmap[index]
        self.item_frame = ttk.Frame(parent, style="TNotebook", borderwidth=0)
        self.item_frame.grid(row=2, column=1, sticky='NES')
        # INSIDE ABOVE FRAME
        row = 0
        ttk.Label(self.item_frame, text=entry['name']).grid(row=row, sticky='NWS')
        for affix in entry['affixes']:
            row = row + 1
            ttk.Label(self.item_frame, text=affix['effect']).grid(row=row, sticky='NES')


class ScrollbarItems(ttk.Frame):
    def __init__(self, items, parent=None):
        ttk.Frame.__init__(self, parent)
        self.indexmap = []
        self.parent = parent
        self.makewidgets(items)

    def makewidgets(self, items):
        sb = tk.Scrollbar(self)
        listing = tk.Listbox(self, relief='sunken')
        sb.config(command=listing.yview)
        listing.config(yscrollcommand=sb.set, height=35)
        sb.grid(row=0, column=1, sticky='ns')
        listing.grid(row=0, column=0, sticky='ns')
        for item in items:
            curr_index = len(self.indexmap)
            label = item['name']
            if not isinstance(label, str):
                label = label['name']
            listing.insert(curr_index, label)
            self.indexmap.append(item)
        self.listbox = listing
