import tkinter as tk

root = tk.Tk()
temp_f_number = tk.DoubleVar()
temp_c_number = tk.DoubleVar()

tk.Label(root, text="F").grid(row=0, column=0)
tk.Label(root, text="C").grid(row=0, column=1)

temp_f = tk.Entry(root, textvariable=temp_f_number)
temp_c = tk.Entry(root, textvariable=temp_c_number)

temp_f.grid(row=1, column=0)
temp_c.grid(row=1, column=1)

update_in_progress = False

def update_c(*args):
    global update_in_progress
    if update_in_progress: return
    try:
        temp_f_float = temp_f_number.get()
    except ValueError:
        return
    new_temp_c = round((temp_f_float - 32) * 5 / 9, 2)
    update_in_progress = True
    temp_c_number.set(new_temp_c)
    update_in_progress = False

def update_f(*args):
    global update_in_progress
    if update_in_progress: return
    try:
        temp_c_float = temp_c_number.get()
    except ValueError:
        return
    new_temp_f = round(temp_c_float * 9 / 5 + 32, 2)
    update_in_progress = True
    temp_f_number.set(new_temp_f)
    update_in_progress = False

temp_f_number.trace("w", update_c)
temp_c_number.trace("w", update_f)

root.mainloop()