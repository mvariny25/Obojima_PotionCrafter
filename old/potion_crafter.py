import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np
import time
import keyboard as kb


root = Tk()
root.geometry("600x600")
dropdownID = None

def show1():
    lbl1.config(text = cb1.get())

def show2():
    lbl2.config(text = cb2.get())

def show3():
    lbl3.config(text = cb3.get())
    


class SearchableComboBox():
    def __init__(self, options) -> None:
        self.dropdown_id = None
        self.options = options

        # Create a Text widget for the entry field
        wrapper = tk.Frame(root)
        wrapper.pack()

        self.entry = tk.Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown) 
        self.entry.pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(root, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(tk.END, option)

# def on_entry_key(event, widget, full_list):
#     typed_value = widget.get().strip().lower()
#     if not typed_value:
#         # If the entry is empty, display all options
#         widget.delete(0, tk.END)
#         for option in full_list:
#             widget.insert(tk.END, option)
#     else:
#         # Filter options based on the typed value
#         widget.delete(0, tk.END)
#         filtered_options = [option for option in full_list if option.lower().startswith(typed_value)]
#         for option in filtered_options:
#             widget.insert(tk.END, option)
#     show_dropdown(event, widget)

def on_select(self, event):
    selected_index = self.listbox.curselection()
    if selected_index:
        selected_option = self.listbox.get(selected_index)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, selected_option)

def show_dropdown(event, widget,dropdownID=None):
    # Listbox.place(in_=Listbox.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
    # Listbox.lift()

    # Show dropdown for 2 seconds
    # time.sleep(0.005)
    
    if dropdownID: # Cancel any old events
        widget.after_cancel(dropdownID)
    # dropdownID = widget.after_cancel(lambda: hide_dropdown(widget))

def hide_dropdown(self):
    self.place_forget()

def on_type(event, widget, full_list, dropdownID=None):
    
    
    # s = time.time()
    # while time.time()-s <=2:
        # pass
    typed_text = widget.get().lower()
    # while kb.is_pressed('ctrl'):
    # time.sleep(0.5)
    if typed_text == '':
        widget['values'] = full_list
    else:
        filtered_data = [item for item in full_list if typed_text in item.lower()]
        widget['values'] = filtered_data
        
        
        # if time.time()-s >= 0.005:
        # time.sleep(1)
        # down = widget.event_generate('<Control-Key-Down>')
        # show_dropdown(down, widget['values'])
        # widget.event_generate('<M1>')

    # widget.after(10, lambda: widget.tk.call(widget._w, "post"))

    
    # 3. The "Magic" line: This opens the dropdown menu (posts it)
    # without taking focus away from the text cursor.
    # This avoids the "ImportError" and the "one key at a time" issue.
    try:
        widget.tk.call(widget._w, "post")
    except:
        pass
    show_dropdown(event, widget, dropdownID)
    # This is the "Fluid" fix: 
    # We only open the dropdown if the list isn't empty, 
    # but we don't 'Down' arrow (which steals focus).
    #
    # try:
    #     widget.tk.call(widget._w, "post") 
    #     # time.sleep(5)
    #     # widget.focus()
    #     # widget.selection_clear()
    # except TclError:
    #     pass

def calculate_ingredients(ins, pots):

    # Clean inputs: remove empty/default selections
    ins_list = [x for x in ins if isinstance(x, str) and x.strip() and x != 'Select an Ingredient']
    if len(ins_list) != 3:
        return "Please provide 3 ingredients"

    mask = (
    pots[['i1_name', 'i2_name', 'i3_name']]
        .apply(set, axis=1)
        .eq({ins[0], ins[1], ins[2]})
    )

    res = pots.loc[mask, 'list_of_potions']
    if res.empty:
        return "No potion found"
    else:
        return res.iloc[0]


if __name__ == "__main__":
    # opt = StringVar(value="Amber")
    pots = pd.read_json('potions.json')
    # ins = ['Amber', 'Apper Carrot', 'Blue Back Salmon']
    ingredients = pd.read_json('ingredients.json')
    
    l = ingredients['ingredient'].unique().tolist()
    # Button(root, text = 'Ingredient 1', command=show).pack()
    # OptionMenu(root, opt, *ingredients['ingredient']).pack()
    
    # wrapper = tk.Frame(root)
    # wrapper.pack()
    # entry = tk.Entry(wrapper, width=24)
    
    # cb = ttk.Combobox(root, values=ingredients['ingredient'].unique())
    cb1 = ttk.Combobox(root, values=l, takefocus=True)
    # cb1 = ttk.Combobox()
    cb1.set('')
    # ttk.tree
    
    # cb1.bind("<KeyRelease>", on_entry_key)
    # cb1.pack(side=tk.LEFT)
    cb1.grid(row=0, column=0, padx=10, pady=10)
    # cb1.pack()
    btn1 = Button(root, text='Ingredient 1', command=show1)
    btn1.grid(row=1, column=0)

    cb2 = ttk.Combobox(root, values=l)
    cb2.set('')
    cb2.grid(row=0, column=1, padx=10, pady=10)
    # cb2.pack()
    btn2 = Button(root, text='Ingredient 2', command=show2)
    btn2.grid(row=1, column=1)


    cb3 = ttk.Combobox(root, values=l)
    cb3.set('')
    cb3.grid(row=0, column=2)
    # cb3.pack()
    btn3 = Button(root, text='Ingredient 3', command=show3)
    btn3.grid(row=1, column=2)
    # print(pots['i1_name'].unique())
    # cb1.bind()
    # cb1.bind('<KeyRelease>', lambda event: on_type(event, cb1, l))
    down = cb1.event_generate('<Control-Key-Down>')
    # text = cb1.bind('<KeyPress>', lambda event: type(event, cb1))
    cb1.bind('<FocusIn>', lambda event: show_dropdown(down, cb1))
    cb1.bind('<KeyRelease>', lambda event: on_type(event, cb1, l))
    
    # cb1.bind('M1+<KeyPress>', lambda event:show_dropdown(event,cb1))
    # cb1.bind("M1", lambda event: show_dropdown(down, cb1)) 

    cb2.bind('<KeyRelease>', lambda event: on_type(event, cb2, l))
    cb3.bind('<KeyRelease>', lambda event: on_type(event, cb3, l))

    lbl1 = Label(root, text=" ")
    lbl1.grid(row=2, column=0, padx=10, pady=10)

    lbl2 = Label(root, text=" ")
    lbl2.grid(row=2, column=1, padx=10, pady=10)

    lbl3 = Label(root, text=" ")
    lbl3.grid(row=2, column=2, padx=10, pady=10)

    print(lbl1.cget("text"))
    pot = Button(root, text = 'Calculate Potion!', command = lambda: lbl.config(text = calculate_ingredients([lbl1.cget("text"), lbl2.cget("text"), lbl3.cget("text")], pots)))
    pot.grid(row=3, column=1, padx=10, pady=10)
    lbl = Label(root, text=" ")
    lbl.grid(row=4, column=1, padx=10, pady=10)

    
    # lbl.pack()
    root.mainloop()
    # # print(pots.head())
    # # print(pots['i1_name']['Amber'])
    # potion = calculate_ingredients(ins)
    # print(potion)
    # item = pots[(pots['i1_name'] == ins[0]) & (pots['i2_name'] == ins[1]) & (pots['i3_name'] == ins[2])]
    # # print((pots['i1_name']['i2_name']['i3_name']).isin(ins))
    # print(item['list_of_potions'].values[0])