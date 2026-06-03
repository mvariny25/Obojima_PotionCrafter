from tkinter import *
import pandas as pd
import numpy as np
import time
import pickle
from pathlib import Path

win = Tk()
win.geometry("1280x720")
win.title("Obojima Potion Crafter")

def format_potion_output(row):
    found_potions = []

    if pd.notna(row['C_potion']) and row['C_potion'] != "":
        found_potions.append(f"Combat Potion: {row['C_potion']}")

    if pd.notna(row['U_potion']) and row['U_potion'] != "":
        found_potions.append(f"Utility Potion: {row['U_potion']}")
    
    if pd.notna(row['W_potion']) and row['W_potion'] != "":
        found_potions.append(f"Whimsy Potion: {row['W_potion']}")

    return "\n".join(found_potions) if found_potions else "No potion found"

print('Loading Potions... \n')
start_time = time.time()

if Path('potion_lookup.pkl').exists():
    print('Loading potion lookup from cache...')
    with open('potion_lookup.pkl', 'rb') as f:
        potion_lookup = pickle.load(f)
        pots = potion_lookup.values() 
else:
    pots = pd.read_json('potions.json')

    potion_lookup = {
        frozenset([row['i1_name'], row['i2_name'], row['i3_name']]): format_potion_output(row)
        for _, row in pots.itterrows()
    }

    with open('potion_lookup.pkl', 'wb') as f:
        pickle.dump(potion_lookup,f)
    print('Potion lookup created and cached!')

end_time = time.time()
print(f'Potions Loaded! {end_time - start_time:.2f} s\n')

if Path('ingredients.pkl').exists():
    print('Loading ingredients from cache...')
    with open('ingredients.pkl', 'rb') as f:
        ingredients = pickle.load(f)
else:
    ingredients = pd.read_json('ingredients.json')
    with open('ingredients.pkl', 'wb') as f:
        pickle.dump(ingredients, f)
    print('Ingredients loaded and cached!')


l = ingredients['ingredient'].unique().tolist()

values = l


def check(event, entry_widget, listbox_widget):
    typed = entry_widget.get()

    if typed == '':
        filtered_data = values
    else:
        filtered_data = [item for item in values if typed.lower() in item.lower()]

    update_listbox(filtered_data, listbox_widget)

def update_listbox(data, listbox_widget):
    listbox_widget.delete(0, END)
    for value in data:
        listbox_widget.insert(END, value)

def on_select(event, entry_widget, listbox_widget):
    selection = listbox_widget.curselection()
    if selection:
        selected_item = listbox_widget.get(selection[0])
        entry_widget.delete(0, END)
        entry_widget.insert(0, selected_item)

def calculate_ingredients(ins, pots):
    ins_list = [x for x in ins if isinstance(x, str) and x.strip() and x != 'Select an Ingredient']

    if len(ins_list) != 3:
        return "Please provide 3 ingredients"
    
    target_recipe = frozenset(ins_list)

    return potion_lookup.get(target_recipe, "No potion can be made with these three ingredients!")

def display_potion():

    current_ingredients = [entry1.get(), entry2.get(), entry3.get()]

    result = calculate_ingredients(current_ingredients, pots)

    result_text.set(result)


Label(win, text='Obojima Potion Crafter\nType to search, double click to select', font=('Arial', 16, 'bold'), bg = 'lightblue').pack(pady=15)

main_container = Frame(win)
main_container.pack(pady=10)

left_frame = Frame(main_container)
left_frame.grid(row=0, column=0, padx=20)

Label(left_frame, text='Selection1:').pack(pady=5)
entry1 = Entry(left_frame, width=15, font=('Arial', 12))
entry1.pack(pady=5)

menu1 = Listbox(left_frame, height=10, font=('Arial', 10))
menu1.pack(fill=X)

entry1.bind('<KeyRelease>', lambda e: check(e, entry1, menu1))
menu1.bind('<Double-Button-1>', lambda e: on_select(e, entry1, menu1))

mid_frame = Frame(main_container)
mid_frame.grid(row=0, column=1, padx=20)

Label(mid_frame, text='Selection1:').pack(pady=5)
entry2 = Entry(mid_frame, width=15, font=('Arial', 12))
entry2.pack(pady=5)

menu2 = Listbox(mid_frame, height=10, font=('Arial', 10))
menu2.pack(fill=X)

entry2.bind('<KeyRelease>', lambda e: check(e, entry2, menu2))
menu2.bind('<Double-Button-1>', lambda e: on_select(e, entry2, menu2))

right_frame = Frame(main_container)
right_frame.grid(row=0, column=2, padx=20)

Label(right_frame, text='Selection1:').pack(pady=5)
entry3 = Entry(right_frame, width=15, font=('Arial', 12))
entry3.pack(pady=5)

menu3 = Listbox(right_frame, height=10, font=('Arial', 10))
menu3.pack(fill=X)

entry3.bind('<KeyRelease>', lambda e: check(menu3))
menu3.bind('<Double-Button-1>', lambda e: on_select(e, entry3, menu3))


result_text = StringVar()
result_text.set('Your potion will appear here...')

txt_frame = Frame(main_container)
txt_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=15)

Label(txt_frame, textvariable=result_text, font=('Arial', 14, 'bold'), fg='darkgreen', justify='center').pack(pady=5)

bot_frame = Frame(main_container)
bot_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

pot = Button(bot_frame, text='Calculate Potion!', font=('Arial', 12), command=display_potion)
pot.pack(pady=5)

update_listbox(values,menu1)
update_listbox(values,menu2)
update_listbox(values,menu3)

win.mainloop()