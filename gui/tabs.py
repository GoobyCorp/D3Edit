import db
import tkinter as tk
from tkinter import ttk
from save_manager import item_handler


# noinspection PyAttributeOutsideInit
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
        self.active_stash = tk.StringVar(value='SC - Non Season')
        self.safemode = tk.IntVar(value=1)
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
        ttk.Label(self.account_frame, text="Rift Level").grid(column=0, row=2, sticky='W')
        currency_list = db.get_currency_list()
        for ids, currency in currency_list:
            ttk.Label(self.account_frame, text=currency).grid(column=0, row=(int(ids) + 5), sticky='W')
        offset = 0
        if self.active_partition.get() == "Season":
            offset = 2
        for m in (0, 1):
            coffset = str(offset + m)
            column = (1 + m)
            cp = self.part_textvars[coffset]
            ttk.Entry(self.account_frame, textvariable=cp['plvl']).grid(column=column, row=1, sticky='E')
            ttk.Entry(self.account_frame, textvariable=cp['rift']).grid(column=column, row=2, sticky='E')
            cc = cp['currencies']
            for ids in cc.keys():
                idi = int(ids)
                ttk.Entry(self.account_frame, textvariable=cc[ids]).grid(column=column, row=(idi + 5), sticky='E')

    def get_partition_data(self, partition):
        partition_id = str(partition.partition_id)
        self.part_textvars[partition_id] = {}
        current_partition = self.part_textvars[partition_id]
        current_partition['plvl'] = tk.StringVar(value=partition.alt_level)
        current_partition['rift'] = tk.StringVar(value=0)
        for attr in partition.saved_attributes.attributes:
            if attr.key == -4077:
                current_partition['rift'] = tk.StringVar(value=attr.value)
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
        # noinspection PyUnresolvedReferences
        self.active_hid = self.active_hero_name.get().split(" - ")[1]
        current_hero_data = self.account.heroes[self.active_hid]
        self.active_hero_data['Name'] = tk.StringVar(value=current_hero_data.digest.hero_name)
        self.active_hero_data['Level'] = tk.StringVar(value=current_hero_data.digest.level)
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

    # noinspection PyUnusedLocal
    def configure_stash_frame(self, event=None):
        if self.active_stash_frame:
            self.active_stash_frame.destroy()
        self.active_stash_frame = tk.Frame(self.stash_tab, bg='white')
        self.active_stash_frame.grid(column=0, row=1)
        stashvalues = ['SC - Non Season', 'HC - Non Season', 'SC - Season', 'HC - Season'] + self.heroes
        c = ttk.Combobox(self.active_stash_frame, textvariable=self.active_stash, values=stashvalues, state='readonly')
        c.grid(column=0, row=0, sticky='NW')
        c.bind("<<ComboboxSelected>>", self.configure_stash_frame)
        active_stash = self.active_stash.get()
        if active_stash == 'SC - Non Season':
            try:
                self.stash_data = self.account.asd.partitions[0].items.items
            except IndexError:
                self.stash_data = None
        elif active_stash == 'HC - Non Season':
            try:
                self.stash_data = self.account.asd.partitions[1].items.items
            except IndexError:
                self.stash_data = None
        elif active_stash == 'SC - Season':
            try:
                self.stash_data = self.account.asd.partitions[2].items.items
            except IndexError:
                self.stash_data = None
        elif active_stash == 'HC - Season':
            try:
                self.stash_data = self.account.asd.partitions[3].items.items
            except IndexError:
                self.stash_data = None
        else:
            hero_id = self.active_stash.get().split(' - ')[1]
            self.stash_data = self.account.heroes[hero_id].items.items
        if self.stash_data:
            self.load_item_list_frame(self.stash_data, self.active_stash_frame)

    def safemode_toggle(self):
        if self.item_frame:
            if self.safemode.get() == 1:
                try:
                    self.valid_values = [db.get_affix_from_id(x)[0][3] for x in self.entry['legal_affixes']]
                except KeyError:
                    self.valid_values = [x[3] for x in db.get_affix_all()]
                print("Safemode ON!")
            else:
                self.valid_values = [x[3] for x in db.get_affix_all()]
                print("Safemode OFF!")
            self.load_item_frame(self.item_list_frame)

    def load_item_list_frame(self, itemlist, parent):
        if self.item_list_frame:
            self.item_list_frame.destroy()
        self.item_list_frame = ttk.Frame(parent, style="TNotebook", borderwidth=0)
        self.item_list_frame.grid(column=0, row=1, sticky='NESW')
        ttk.Label(self.item_list_frame, text="Item List:").grid(column=0, row=1, sticky='W')
        parent.columnconfigure(1, weight=1)
        self.decodeditems = item_handler.decode_itemlist(itemlist)
        self.item_scrollbar = ScrollbarItems(self.decodeditems, parent=self.item_list_frame)
        self.item_scrollbar.grid(column=0, row=3)
        self.item_scrollbar.listbox.bind('<Double-1>', lambda x: self.load_item_frame(self.item_list_frame))

    def load_item_frame(self, parent):
        if self.item_frame:
            self.item_frame.destroy()
        self.index = self.item_scrollbar.listbox.curselection()[0]
        self.entry = self.item_scrollbar.indexmap[self.index]
        self.item_main_frame = tk.Frame(parent, bg='white')
        self.item_main_frame.grid(row=0, column=1, sticky='WN', rowspan=10)
        seframe = tk.Frame(self.item_main_frame, bg='white')
        cb = tk.Checkbutton(seframe, text="Safe Edit Mode", variable=self.safemode, onvalue=1, offvalue=0,
                            command=self.safemode_toggle)
        cb.grid(column=0, row=0, sticky='W')
        tl = tk.Label(seframe, text=' (Try to show only affixes that make sense)')
        tl.grid(column=1, row=0, sticky='W')
        seframe.grid(column=0, row=0, columnspan=2, sticky='WN')
        self.item_frame = tk.Frame(self.item_main_frame, bg='white')
        self.item_frame.grid(row=1, column=0, sticky='WN')
        # INSIDE ABOVE FRAME
        if self.entry == 'No Item':
            addid = tk.StringVar(value='0')
            affixnum = tk.StringVar(value='0')
            lab = ttk.Label(self.item_frame, text="Add item with ID:")
            lab.grid(column=0, row=6)
            ent = ttk.Entry(self.item_frame, textvariable=addid)
            ent.grid(column=1, row=6)
            lab = ttk.Label(self.item_frame, text="Number of Affixes:")
            lab.grid(column=0, row=7)
            ent2 = ttk.Entry(self.item_frame, textvariable=affixnum)
            ent2.grid(column=1, row=7)
            ttk.Label(self.item_frame, text="Note: If there's no space in the inventory no item will be added").grid(column=0, row=8, columnspan=2)
            sb = ttk.Button(self.item_frame, text="Add Item", command=lambda: self.additem(addid.get(), affixnum.get()))
            sb.grid(column=0, row=9)
            return
        row = 0
        v = tk.StringVar()
        v.set(self.entry['name'])
        l = int(len(self.entry['name'])*0.9)
        e = tk.Entry(self.item_frame, readonlybackground='white', fg='black', textvariable=v, bd=0, width=l,
                     state='readonly', highlightthickness=0)
        e.grid(row=row, sticky='W', columnspan=2)
        if self.safemode.get() == 1:
            try:
                self.valid_values = [db.get_affix_from_id(x)[0][3] for x in self.entry['legal_affixes']]
            except KeyError:
                self.valid_values = [x[3] for x in db.get_affix_all()]
        else:
            self.valid_values = [x[3] for x in db.get_affix_all()]
        category = self.entry['category']
        quality = self.entry['item'].generator.item_quality_level
        row = row + 1
        ttk.Label(self.item_frame, text=self.entry['slot']).grid(column=0, row=row, sticky='W')
        if (category == 'Gems') and (quality == 9):
            row = row + 1
            ttk.Label(self.item_frame, text="Legendary Gem Level: ").grid(column=0, row=row)
            ttk.Entry(self.item_frame, textvariable=self.entry['jewel_rank']).grid(column=1, row=row)
        elif self.entry['stackable']:
            row = row + 1
            ttk.Label(self.item_frame, text="Stack Size: ").grid(column=0, row=row)
            ttk.Entry(self.item_frame, textvariable=self.entry['stack_size']).grid(column=1, row=row)
        try:
            enchanted = self.entry['enchanted']
        except KeyError:
            enchanted = False
        crow = row
        self.cbs = []
        for affix, description in self.entry['affixes']:
            crow = crow + 1
            if enchanted:
                # noinspection PyUnresolvedReferences
                if affix == enchanted[0][0]:
                    ttk.Label(self.item_frame, text="Enchanted").grid(column=1, row=crow, sticky='NES')
                    description = enchanted[1]
            cb = ttk.Combobox(self.item_frame, textvariable=description, values=self.valid_values, state='readonly')
            cb.grid(row=crow, sticky='W')
            cb.bind("<<ComboboxSelected>>", lambda x: self.set_item_affixes(x, row))
            self.cbs.append(cb)
            self.size_affix_combobox()
        button_frame = ttk.Frame(self.item_frame)
        button_frame.grid(column=0, row=99)
        sb = ttk.Button(button_frame, text="Save Item", command=self.saveitem)
        sb.grid(column=0, row=97)
        cb = ttk.Button(button_frame, text="Duplicate Item",
                        command=lambda: self.additem(affixnum=0, ids=0, item=self.entry['item']))
        cb.grid(column=1, row=97)
        rb = ttk.Button(button_frame, text="Reroll Item", command=self.reroll_item)
        rb.grid(column=0, row=98)
        ttk.Label(button_frame, text="(generate new random seed)").grid(column=1, row=98)
        delb = ttk.Button(button_frame, text="Delete Item", command=self.deleteitem)
        delb.grid(column=0, row=99)

    def size_affix_combobox(self):
        lenlist = [len(a[1].get()) for a in self.entry['affixes']]
        self.cbl = max(lenlist)
        for cb in self.cbs:
            cb.config(width=self.cbl)

    def set_item_affixes(self, event, row):
        wg = event.widget
        # this is a pretty crappy way of doing it, TODO: rewrite
        affix_changing = int(wg.grid_info()['row']) - (row + 1)
        prev_affix = self.entry['affixes'][affix_changing][0]
        try:
            rerolled_affix = self.entry['enchanted'][0][0]
        except KeyError:
            rerolled_affix = False
        enchanted_affix = False
        if prev_affix == rerolled_affix and prev_affix != 0:
            enchanted_affix = True
            new_val = self.entry['enchanted'][1].get()
        else:
            new_val = self.entry['affixes'][affix_changing][1].get()
        new_val_ids = [x[0] for x in db.get_affix_from_effect(new_val)]
        new_id = new_val_ids[0]
        if enchanted_affix:
            self.entry['item'].generator.enchanted_affix_new = new_id
        else:
            self.entry['item'].generator.base_affixes[affix_changing] = new_id
        self.size_affix_combobox()

    def additem(self, ids, affixnum, amount=1, item=None):
        if not item:
            newitem = item_handler.generate_item(ids, affixnum)
        else:
            newitem = item
        active_stash = self.active_stash.get()
        account_stash = ['SC - Non Season', 'HC - Non Season', 'HC - Season', 'SC - Season']
        if active_stash in account_stash:
            p = account_stash.index(active_stash)
            available_slots = [i for i in range(0, 20)]
            saved_attr = self.account.asd.partitions[p].saved_attributes.attributes
            for attribute in saved_attr:
                if attribute.key == -4096:
                    available_slots = [i for i in range(0, attribute.value)]
            for i in self.stash_data:
                try:
                    available_slots.remove(i.square_index)
                except ValueError:
                    print("Item collition detected, two items in the same inventory slot!")
                    print("{0}, {1}".format(i.square_index, i.generator.seed))
            if available_slots:
                newitem.item_slot = 544
                it = self.stash_data.add()
                it.CopyFrom(newitem)
                it.square_index = available_slots[-1]
            else:
                print("Inventory is full!")
            self.account.commit_account_changes()
        else:
            hero_id = self.active_stash.get().split(' - ')[1]
            available_slots = [i for i in range(0, 60)]
            for i in self.stash_data:
                if i.item_slot == 272:
                    try:
                        available_slots.remove(i.square_index)
                    except ValueError:
                        print("Item collition detected, two items in the same inventory slot!")
                        print("{0}, {1}".format(i.square_index, i.generator.seed))
            if available_slots:
                newitem.item_slot = 272
                it = self.stash_data.add()
                it.CopyFrom(newitem)
                it.square_index = available_slots[-1]
            self.account.commit_hero_changes(hero_id)
        self.load_item_list_frame(self.stash_data, self.active_stash_frame)

    def reroll_item(self):
        print("Seed before: {}".format(self.entry['item'].generator.seed))
        self.entry['item'] = item_handler.reroll_item(self.entry['item'])
        print("Seed after: {}".format(self.entry['item'].generator.seed))

    def saveitem(self):
        if self.entry['jewel_rank'] != 0:
            self.entry['item'].generator.jewel_rank = int(self.entry['jewel_rank'].get())
        if self.entry['stackable']:
            self.entry['item'].generator.stack_size = int(self.entry['stack_size'].get())
        target = self.index - 1  # This is an index relative to the itemlist
        self.stash_data[target].CopyFrom(self.entry['item'])
        active_stash = self.active_stash.get()
        account_stash = ['SC - Non Season', 'HC - Non Season', 'HC - Season', 'SC - Season']
        if active_stash in account_stash:
            self.account.commit_account_changes()
        else:
            hero_id = self.active_stash.get().split(' - ')[1]
            self.account.commit_hero_changes(hero_id)
        message_label = ttk.Label(self.item_frame, text="Item Saved!", style="TLabel")
        message_label.grid(column=0, row=98, sticky='NEW')

    def deleteitem(self):
        iname = self.entry['name']
        target = self.index - 1
        active_stash = self.active_stash.get()
        account_stash = ['SC - Non Season', 'HC - Non Season', 'HC - Season', 'SC - Season']
        if self.safemode.get() == 0:
            print("Deleting item : {}".format(iname))
            del self.stash_data[target]
            if active_stash in account_stash:
                self.account.commit_account_changes()
            else:
                hero_id = self.active_stash.get().split(' - ')[1]
                self.account.commit_hero_changes(hero_id)
            self.item_frame.destroy()
            self.load_item_list_frame(self.stash_data, self.active_stash_frame)
        else:
            message_label = ttk.Label(self.item_frame, text="Disable safe mode first!", style="TLabel")
            message_label.grid(column=0, row=97, sticky='NEW')


# noinspection PyAttributeOutsideInit
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
        sb.grid(row=0, column=1, sticky='ns')
        listing.grid(row=0, column=0, sticky='ns')
        listing.insert(0, ' ++ Add Item ++ ')
        self.indexmap.append('No Item')
        lswid = 30
        for item in items:
            curr_index = len(self.indexmap)
            label = item['name']
            if not isinstance(label, str):
                label = label['name']
            if "ID: " in label:
                label = label.split("ID: ")[0]
            if ": " in label:
                label = label.split(": ")[1]
            listing.insert(curr_index, label)
            if (len(label)*0.75) > lswid:
                lswid = int((len(label)*0.75))
            self.indexmap.append(item)
        listing.config(yscrollcommand=sb.set, height=35, width=lswid)
        self.listbox = listing
