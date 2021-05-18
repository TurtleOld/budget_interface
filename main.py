import datetime
import tkinter
from tkinter import ttk, END
from settings_database import cursor, connection

window = tkinter.Tk()
window.title("Домашняя бухгалтерия")
window.geometry("910x400")
window.iconbitmap(r"ico\victory_43837.ico")

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


comboBox = ttk.Combobox(window, width=65)
comboBox["values"] = receipt_seller()
comboBox.place(x=15, y=25)

# Entry date
entry_date = tkinter.Entry(window)
now_date = datetime.datetime.now().date()
entry_date.insert(END, now_date)
entry_date.place(x=515, y=26)


def get_all_from_database():
    value = comboBox.get()
    value_date = entry_date.get()
    cursor.execute(
        "SELECT date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt WHERE name_seller=%s AND date_receipt=%s GROUP BY date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt",
        (value, value_date,))
    return cursor


def show_all_info_receipt():
    columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
    tree = ttk.Treeview(show="headings", columns=columns)
    tree.heading("#1", text="Дата")
    tree.column("#1", width=75)
    tree.heading("#2", text="Время")
    tree.column("#2", width=75)
    tree.heading("#3", text="Название продукта")
    tree.column("#3", width=350)
    tree.heading("#4", text="Цена")
    tree.column("#4", width=75)
    tree.heading("#5", text="Количество")
    tree.column("#5", width=75)
    tree.heading("#6", text="Сумма за товар")
    tree.column("#6", width=110)
    tree.heading("#7", text="Сумма чека")
    tree.column("#7", width=110)

    for item in get_all_from_database():
        tree.insert("", END, values=item)
    tree.place(relx=0.013, rely=0.13)

    scroll = tkinter.Scrollbar(window, orient="vertical", command=tree.yview)
    scroll.place(x=884, y=53, height=225)
    tree.configure(yscrollcommand=scroll.set)


btn_get_info_all = tkinter.Button(window, text="Показать", command=show_all_info_receipt)
btn_get_info_all.place(x=15, y=300)


# Получение итоговой суммы по всем чекам за весь период
def total_sum():
    cursor.execute("SELECT sum(amount) FROM receipt")
    for item_total_sum in cursor.fetchall():
        for item_total_sum_prev in item_total_sum:
            return item_total_sum_prev


label_total_sum = tkinter.Label(window, text=f"Итог по всем чека за весь период: {total_sum()}")
label_total_sum.place(x=580, y=1)


# Получение всех чеков
def get_all_receipt():
    cursor.execute(
        "SELECT date_receipt, time_receipt, name_product, price, quantity, amount, total_sum FROM receipt GROUP BY date_receipt, time_receipt, name_product, price, quantity, amount, total_sum ORDER BY date_receipt")
    columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7")
    tree = ttk.Treeview(show="headings", columns=columns)
    tree.heading("#1", text="Дата")
    tree.column("#1", width=75)
    tree.heading("#2", text="Время")
    tree.column("#2", width=75)
    tree.heading("#3", text="Название продукта")
    tree.column("#3", width=350)
    tree.heading("#4", text="Цена")
    tree.column("#4", width=75)
    tree.heading("#5", text="Количество")
    tree.column("#5", width=75)
    tree.heading("#6", text="Сумма за товар")
    tree.column("#6", width=110)
    tree.heading("#7", text="Сумма чека")
    tree.column("#7", width=110)

    for item in cursor:
        tree.insert("", END, values=item)
    tree.place(relx=0.013, rely=0.13)

    scroll = tkinter.Scrollbar(window, orient="vertical", command=tree.yview)
    scroll.place(x=884, y=53, height=225)
    tree.configure(yscrollcommand=scroll.set)


btn_show_all_receipt = tkinter.Button(window, text="Показать все чеки", command=get_all_receipt)
btn_show_all_receipt.place(x=165, y=300)

window.mainloop()
