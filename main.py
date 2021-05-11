import tkinter
from tkinter import ttk
from settings_database import cursor, connection
from psycopg2 import Error

window = Tk()
window.title("Домашняя бухгалтерия")
window.geometry("800x600")

if connection:
    label_connection = Label(text="Подключение к базе данных прошло успешно!")
    label_connection.place(x=15, y=1)
    label_connection.config(fg="Green")


def receipt_seller():
    cursor.execute("SELECT name_seller FROM receipt GROUP BY name_seller")
    data = []
    for item in cursor.fetchall():
        data.append(*item)
    return data


receipt_seller()

comboBox = ttk.Combobox(window, width=65)
comboBox["values"] = receipt_seller()
comboBox.place(x=15, y=25)


def get_all_info():
    value = comboBox.get()
    cursor.execute(
        f"SELECT date_receipt, time_receipt, name_seller, total_sum FROM receipt WHERE name_seller='{value}' GROUP BY name_seller, time_receipt, date_receipt, total_sum")
    return cursor


def get_seller():
    list_date = Listbox()
    for date_item in get_all_info():
        list_date.insert(END, date_item[0])
    list_date.place(x=15, y=75)
    list_date.config(width=15, height=5)
    list_time = Listbox()
    for time_item in get_all_info():
        list_time.insert(END, time_item[1])
    list_time.place(x=100, y=75)
    list_time.config(width=15, height=5)


btn = Button(window, text="Get", command=get_seller)
btn.place(x=500, y=22)

window.mainloop()
