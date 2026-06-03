# Source - https://stackoverflow.com/a/65821591
# Posted by Sobhy Elgraidy
# Retrieved 2026-05-26, License - CC BY-SA 4.0

# from tkinter import *

# from tkinter import ttk

# lst = ['C', 'C++', 'Java',
#        'Python', 'Perl',
#        'PHP', 'ASP', 'JS']


# def check_input(event):
#     value = event.widget.get()

#     if value == '':
#         combo_box['values'] = lst
#     else:
#         data = []
#         for item in lst:
#             if value.lower() in item.lower():
#                 data.append(item)

#         combo_box['values'] = data


# root = Tk()

# # creating Combobox
# combo_box = ttk.Combobox(root)
# combo_box['values'] = lst
# combo_box.bind('<KeyRelease>', check_input)
# combo_box.pack()

# root.mainloop()


# Source - https://stackoverflow.com/a/55652875
# Posted by User1493
# Retrieved 2026-05-26, License - CC BY-SA 4.0

import tkinter as tk
import tkentrycomplete

root = tk.Tk()
box_value = tk.StringVar()

def fun():
    print(box_value.get())
combo = tkentrycomplete.AutocompleteCombobox(textvariable=box_value)
test_list = ['apple', 'banana', 'cherry', 'grapes']
combo.set_completion_list(test_list)
combo.place(x=140, y=50)
button = tk.Button(text='but', command=fun)
button.place(x=140,y=70)

root.mainloop()
