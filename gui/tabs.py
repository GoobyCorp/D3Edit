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
        self.affixfilter = tk.StringVar()
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
        c = ttk.Combobox(self.account_tab, width=30, textvariable=self.active_partition,
                         values=copt, state='readonly')
        c.grid(column=0, row=0, sticky='W')
        c.bind("<<ComboboxSelected>>", self.populate_account_frame)
        self.populate_account_frame()

    def populate_account_frame(self, event=None):
        if event:
            self.account_frame.destroy()
            self.account_frame = ttk.Frame(self.account_tab, style="TNotebook", borderwidth=0)
        self.account_frame.grid(column=0, row=2)
        ttk.Label(self.account_frame, text="Softcore").grid(column=1, row=1)
        ttk.Label(self.account_frame, text="Hardcore").grid(column=2, row=1)
        ttk.Label(self.account_frame, text="Paragon Level").grid(column=0, row=2, sticky='E')
        ttk.Label(self.account_frame, text="Rift Level").grid(column=0, row=3, sticky='E')
        currency_list = db.get_currency_list()
        for ids, currency in currency_list:
            ttk.Label(self.account_frame, text=currency).grid(column=0, row=(int(ids) + 6), sticky='E')
        offset = 0
        if self.active_partition.get() == "Season":
            offset = 2
        for m in (0, 1):
            coffset = str(offset + m)
            column = (1 + m)
            cp = self.part_textvars[coffset]
            ttk.Entry(self.account_frame, textvariable=cp['plvl']).grid(column=column, row=2, sticky='E')
            ttk.Entry(self.account_frame, textvariable=cp['rift']).grid(column=column, row=3, sticky='E')
            cc = cp['currencies']
            for ids in cc.keys():
                idi = int(ids)
                ttk.Entry(self.account_frame, textvariable=cc[ids]).grid(column=column, row=(idi + 6), sticky='E')
        ttk.Label(self.account_frame, text="==========================================================").grid(column=0, row=98, columnspan=4, sticky='W')

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
            self.active_hero_frame.grid(column=0, row=1, sticky='WE')
        c = ttk.Combobox(self.active_hero_frame, width = 30, textvariable=self.active_hero_name, values=self.heroes, state='readonly')
        c.grid(column=0, row=0, columnspan=2, sticky='W')
        c.bind("<<ComboboxSelected>>", self.load_hero_frame)
        ttk.Label(self.active_hero_frame, text=" ").grid(column=1, row=1)
        # noinspection PyUnresolvedReferences
        self.active_hid = self.active_hero_name.get().split(" - ")[1]
        current_hero_data = self.account.heroes[self.active_hid]
        self.active_hero_data['Name'] = tk.StringVar(value=current_hero_data.digest.hero_name)
        self.active_hero_data['Level'] = tk.StringVar(value=current_hero_data.digest.level)
        row = 2
        for key, value in self.active_hero_data.items():
            ttk.Label(self.active_hero_frame, text=key).grid(column=0, row=row, sticky='E')
            ttk.Entry(self.active_hero_frame, textvariable=self.active_hero_data[key]).grid(column=1, row=row)
            row = row + 1
        ttk.Label(self.active_hero_frame, text="==========================================").grid(column=0,row=row, columnspan=4, sticky='W')
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
        ttk.Label(self.active_hero_frame, text=message).grid(column=0, columnspan=2, row=1)

    # noinspection PyUnusedLocal
    def configure_stash_frame(self, event=None):
        if self.active_stash_frame:
            self.active_stash_frame.destroy()
        self.active_stash_frame = tk.Frame(self.stash_tab, bg='white')
        self.active_stash_frame.grid(column=0, row=1)
        stashvalues = ['SC - Non Season', 'HC - Non Season', 'SC - Season', 'HC - Season'] + self.heroes
        c = ttk.Combobox(self.active_stash_frame, width=30, textvariable=self.active_stash, values=stashvalues, state='readonly')
        c.grid(column=0, row=0, sticky='W')
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
        self.item_scrollbar.listbox.config(width=50)

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
            self.item_frame = AddItemFrame(
                account=self.account, parent=self.item_main_frame, bg='white', stash=self.active_stash.get(), nb=self)
            self.item_frame.grid(column=0, row=1, sticky='WN')
            return
        row = 0
        v = tk.StringVar()
        v.set(self.entry['name'])
        itemIDframe = tk.Frame(self.item_frame, bg='white')
        e = tk.Entry(itemIDframe, readonlybackground='white', fg='black', textvariable=v, bd=0,
                     state='readonly', highlightthickness=0)
        e.grid(column=0, row=0, sticky='W')
        itemIDframe.grid(column=0, row=0, columnspan=100, sticky='W')
        if self.safemode.get() == 1:
            try:
                self.valid_values = [db.get_affix_from_id(x)[0][3] for x in self.entry['legal_affixes']]
            except KeyError:
                self.valid_values = [x[3] for x in db.get_affix_all()]
        else:
            self.valid_values = [x[3] for x in db.get_affix_all()]
        category = self.entry['category']
        row = row + 1
        #Slot
        ttk.Label(self.item_frame, text=self.entry['slot']).grid(column=0, row=row, sticky='W')
        slotrow=row
        if category == 'Legendary Gems':
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
        #Label: Affix | Checked
        if self.entry['affixes']:
            ttk.Label(self.item_frame, text="Affix").grid(column=3,row=slotrow)
            ttk.Label(self.item_frame, text=" | ").grid(column=4,row=slotrow)
            ttk.Label(self.item_frame, text="Checked").grid(column=5, row=slotrow)
        for affix, description, checked in self.entry['affixes']:
            crow = crow + 1
            labelAffix = affix
            labelChecked = checked
            if enchanted:
                # noinspection PyUnresolvedReferences
                if affix == enchanted[0][0]:
                    ttk.Label(self.item_frame, text="Enchanted").grid(column=1, row=crow, sticky='NES')
                    description = enchanted[1]
                    labelAffix = enchanted[0][1]
                    labelChecked = enchanted[2]
            cb = ttk.Combobox(self.item_frame, width=50, textvariable=description, values=self.valid_values, state='readonly')
            cb.grid(row=crow, sticky='W')
            cb.bind("<<ComboboxSelected>>", lambda x: self.set_item_affixes(x, row))
            self.cbs.append(cb)
            self.size_affix_combobox()
            #Show Affix
            s_labelAffix = ttk.Label(self.item_frame, text=labelAffix).grid(column=3, row=crow)
            s_labelSp = ttk.Label(self.item_frame, text=" | ").grid(column=4,row=crow)
            s_labelChecked = ttk.Label(self.item_frame, text=labelChecked).grid(column=5, row=crow, sticky='E')
        if self.affixfilter.get():
            self.update_affixes()
        button_frame = tk.Frame(self.item_frame, background='white')
        button_frame.grid(column=0, row=99, sticky='NW')
        if self.cbs:
            search = ttk.Entry(button_frame, textvariable=self.affixfilter)
            search.grid(column=1, row=0)
            search.bind("<KeyRelease>", self.update_affixes)
            search.bind("<space>", self.update_affixes)
            ttk.Label(button_frame, text="Affix Filter:").grid(column=0, row=0)
        sb = ttk.Button(button_frame, text="Save Item", command=self.saveitem)
        sb.grid(column=0, row=97)
        cb = ttk.Button(button_frame, text="Duplicate Item",
                        command=lambda: self.additem(target_stash=self.active_stash.get(), affixnum=0, ids=0,
                                                     item=self.entry['item']))
        cb.grid(column=1, row=97)
        rb = ttk.Button(button_frame, text="Reroll Item", command=self.reroll_item)
        rb.grid(column=0, row=98)
        ttk.Label(button_frame, text="(generate new random seed)").grid(column=1, row=98)
        delb = ttk.Button(button_frame, text="Delete Item", command=self.deleteitem)
        delb.grid(column=0, row=99)
        #Set to Primal
        xb = ttk.Button(button_frame, text="Set item to Primal", command=self.set_flag)
        xb.grid(column=1, row=99)

        e.grid(column=0, row=0, sticky='W', columnspan=10)
        #Add to show some stats

        #s_labelFlag = ttk.Label(button_frame, text=self.entry['item'].generator.flags).grid(column=1, row=100)

    def update_affixes(self, event=None):
        fil = self.affixfilter.get()
        for cb in self.cbs:
            valid_values = []
            for value in self.valid_values:
                if fil.lower() in value.lower():
                    valid_values.append(value)
            valid_values = set(valid_values)
            cb.config(values=list(valid_values))

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

    def additem(self, **kwargs):
        self.account.additem(**kwargs)
        self.load_item_list_frame(self.stash_data, self.active_stash_frame)

    def reroll_item(self):
        print("Seed before: {}".format(self.entry['item'].generator.seed))
        self.entry['item'] = item_handler.reroll_item(self.entry['item'])
        print("Seed after: {}".format(self.entry['item'].generator.seed))

    def set_flag(self):
        self.entry['item'] = item_handler.set_flag(self.entry['item'])
        message_label = ttk.Label(self.item_frame, text="Item set to Primal, don't forget to save item.", style="TLabel")
        message_label.grid(column=0, row=98, sticky='NEW')

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
            if item['primal']:
                label = label + '   **Primal**'
            if item['ancient']:
                label = label + '   *Ancient*'
            listing.insert(curr_index, label)
            if (len(label)*0.75) > lswid:
                lswid = int((len(label)*0.75))
            self.indexmap.append(item)
        listing.config(yscrollcommand=sb.set, height=35, width=lswid)
        self.listbox = listing


class AddItemFrame(tk.Frame):
    def __init__(self, account, stash, parent=None, nb=None, **kwargs):
        tk.Frame.__init__(self, master=parent, **kwargs)
        self.nb = nb
        self.stash = stash
        self.account = account
        self.parent = parent
        self.qual = tk.StringVar()
        self.cat = tk.StringVar()
        self.addid = tk.StringVar(value='0')
        self.affixnum = tk.StringVar(value='0')
        self.chosenitem = tk.StringVar(value="Please choose a category")
        self.itemcb = None
        self.draw_gui()

    def draw_gui(self):
        lab = ttk.Label(self, text="Add item with ID:")
        lab.grid(column=0, row=6)
        ent = ttk.Entry(self, textvariable=self.addid)
        ent.grid(column=1, row=6)
        lab = ttk.Label(self, text="Add item from Category:")
        lab.grid(column=2, row=6)
        cb = ttk.Combobox(self, textvariable=self.cat, width=50, values=[x[0] for x in list(set(db.get_categories()))],
                          state='readonly')
        cb.grid(column=3, row=6, sticky='W')
        cb.bind("<<ComboboxSelected>>", self.update_item_options)
        lab = ttk.Label(self, text="Number of Affixes:")
        lab.grid(column=0, row=7)
        ent2 = ttk.Entry(self, textvariable=self.affixnum)
        ent2.grid(column=1, row=7)
        lab = ttk.Label(self, text="Specific Item:")
        lab.grid(column=2, row=7)
        self.itemcb = ttk.Combobox(self, width=50, textvariable=self.chosenitem, values=[], state='readonly')
        self.itemcb.grid(column=3, row=7)
        self.itemcb.bind("<<ComboboxSelected>>", self.update_item_id)
        lab = ttk.Label(self, text="Quality:")
        lab.grid(column=0, row=8)
        cb = ttk.Combobox(self, width=50, textvariable=self.qual, values=[x[1] for x in db.get_quality_levels()],
                          state='readonly')
        cb.grid(column=1, row=8, sticky='W')
        self.qual.set("Legendary/Set")
        ttk.Label(self, text="Note: If there's no space in the inventory no item will be added") \
            .grid(column=0, row=20, columnspan=2)
        sb = ttk.Button(self, text="Add Item", command=lambda: self.additem())
        sb.grid(column=0, row=21)

    def update_item_options(self, event=None):
        items = db.get_items_from_category(self.cat.get())
        itemcbvalues = [x[0] for x in items]
        self.itemcbgbids = [x[1] for x in items]
        self.itemcb.config(values=itemcbvalues)
        self.chosenitem.set(itemcbvalues[0])

    def update_item_id(self, event=None):
        index = self.itemcb.current()
        gbid = self.itemcbgbids[index]
        self.addid.set(gbid)

    def additem(self):
        self.account.additem(ids=self.addid.get(), affixnum=self.affixnum.get(),
                             target_stash=self.stash, quality=self.qual.get())
        if self.nb:
            self.nb.load_item_list_frame(self.nb.stash_data, self.nb.active_stash_frame)
