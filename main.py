import tkinter
from tkinter import ttk, END
from settings_database import cursor, connection

window = tkinter.Tk()
window.title("Домашняя бухгалтерия")
window.geometry("800x600")

if connection:
    label_connection = tkinter.Label(text="Подключение к базе данных прошло успешно!")
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


def get_all_from_database():
    value = comboBox.get()
    cursor.execute(
        f"SELECT date_receipt, time_receipt, name_product, total_sum FROM receipt WHERE name_seller='{value}' GROUP BY date_receipt, time_receipt, name_product, total_sum ORDER BY date_receipt")
    return cursor


def get_all_info_receipt():
    columns = ("#1", "#2", "#3")
    tree = ttk.Treeview(show="headings", columns=columns)
    tree.heading("#1", text="Дата")
    tree.column("#1", width=75)
    tree.heading("#2", text="Время")
    tree.column("#2", width=75)
    tree.heading("#3", text="Название продукта")
    tree.column("#3", width=350)

    for item in get_all_from_database():
        tree.insert("", END, values=item)
    tree.place(relx=0.02, rely=0.1)

    scroll = tkinter.Scrollbar(window, orient="vertical", command=tree.yview)
    scroll.place(x=520, y=65, height=220)
    tree.configure(yscrollcommand=scroll.set)


btn = tkinter.Button(window, text="Get", command=get_all_info_receipt)
btn.place(x=500, y=22)

window.mainloop()
