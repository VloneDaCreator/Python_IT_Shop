import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import csv
from tkinter import messagebox

root = tk.Tk()
root.title("Магазин за компютърна техника")
root.configure(padx=40, pady=40)

def show_Products():
    win = tk.Toplevel(root)
    win.title("Продукти")
    win.geometry("600x400")

    tree = ttk.Treeview(win, columns=("ProductID", "ProductName", "CategoryID"), show="headings")
    tree.heading("ProductID", text="Код на продукта")
    tree.heading("ProductName", text="Име на продукта")
    tree.heading("CategoryID", text="Категория")

    tree.column("ProductID", width=80, anchor="center")
    tree.column("ProductName", width=250, anchor="w")
    tree.column("CategoryID", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    try:
        with open("Products.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                tree.insert("", "end", values=(row[0], row[1], row[2]))
    except Exception as e:
        messagebox.showerror("Грешка", f"Неуспешно отваряне на файла:\n{e}")

def show_Sells():
    win = tk.Toplevel(root)
    win.title("Продажби")
    win.geometry("700x500")

    filter_frame = tk.Frame(win)
    filter_frame.pack()

    tk.Label(filter_frame, text="Филтър по дата:").pack(side="left", padx=5)

    cal = Calendar(filter_frame, date_pattern="yyyy-mm-dd", selectmode="day", width=12)
    cal.pack(side="left", padx=5)

    def load_sells(filter_date=None):
        for i in tree.get_children():
            tree.delete(i)
        try:
            with open("Sells.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if not row:
                        continue
                    if filter_date and row[1] != filter_date:
                        continue
                    total = float(row[2]) * float(row[3])
                    tree.insert("", "end", values=(row[0], row[1], f"{float(row[2]):.2f} лв.", row[3], f"{total:.2f} лв."))
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно отваряне на файла:\n{e}")

    def filter_by_date():
        selected_date = cal.get_date()
        try:
            year, month, day = map(int, selected_date.split("-"))
            formatted_date = f"{day}.{month}.{year}"
            load_sells(formatted_date)
        except Exception as e:
            messagebox.showerror("Грешка", f"Невалидна дата:\n{e}")

    tk.Button(filter_frame, text="Филтрирай", command=filter_by_date).pack(side="left", padx=10)
    tk.Button(filter_frame, text="Покажи всички", command=lambda: load_sells(None)).pack(side="left", padx=10)

    tree = ttk.Treeview(win, columns=("ProductID", "Date", "Price", "Quantity", "Total"), show="headings")
    tree.heading("ProductID", text="Код на продукта")
    tree.heading("Date", text="Дата")
    tree.heading("Price", text="Цена")
    tree.heading("Quantity", text="Количество")
    tree.heading("Total", text="Общо")

    tree.column("ProductID", width=80, anchor="center")
    tree.column("Date", width=100, anchor="center")
    tree.column("Price", width=100, anchor="center")
    tree.column("Quantity", width=150, anchor="center")
    tree.column("Total", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    load_sells()

def show_AddSells():
    win = tk.Toplevel(root)
    win.title("Добави продажба")
    win.geometry("600x500")

    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=2)
    win.grid_columnconfigure(2, weight=1)

    tk.Label(win, text="Код на продукт:").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    product_id_entry = tk.Entry(win)
    product_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="Дата (ДД.ММ.ГГГГ):").grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    date_entry = tk.Entry(win)
    date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="Цена:").grid(row=4, column=1, padx=10, pady=10, sticky="ew")
    price_entry = tk.Entry(win)
    price_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(win, text="Количество:").grid(row=6, column=1, padx=10, pady=10, sticky="ew")
    quantity_entry = tk.Entry(win)
    quantity_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

    def save_sell():
        product_id = product_id_entry.get().strip()
        date = date_entry.get().strip()
        price = price_entry.get().strip()
        quantity = quantity_entry.get().strip()

        if not (product_id and date and price and quantity):
            messagebox.showerror("Грешка", "Всички полета са задължителни!")
            return

        try:
            float(price)
            int(quantity)
        except ValueError:
            messagebox.showerror("Грешка", "Цена трябва да е число, количество - цяло число!")
            return

        try:
            with open("Sells.csv", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([product_id, date, price, quantity])
            messagebox.showinfo("Успех", "Продажбата е добавена успешно!")
            win.destroy()
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно записване във файла:\n{e}")

    tk.Button(win, text="Запази", command=save_sell).grid(row=8, column=1, pady=10, sticky="ew")

    tree = ttk.Treeview(win, columns=("ProductID", "ProductName", "CategoryID"), show="headings")
    tree.heading("ProductID", text="Код на продукта")
    tree.heading("ProductName", text="Име на продукта")
    tree.heading("CategoryID", text="Категория")

    tree.column("ProductID", width=80, anchor="center")
    tree.column("ProductName", width=200, anchor="w")
    tree.column("CategoryID", width=100, anchor="center")

    tree.grid(row=9, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    win.grid_rowconfigure(9, weight=1)

    try:
        with open("Products.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if not row: continue
                tree.insert("", "end", values=(row[0], row[1], row[2]))
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("Грешка", f"Неуспешно отваряне на файла:\n{e}")

def show_Search():
    win = tk.Toplevel(root)
    win.title("Търсене по категория")
    win.geometry("500x400")

    tk.Label(win, text="Изберете категория:").pack(pady=10)

    categories = {}
    try:
        with open("Types.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    categories[row[0]] = row[1]
    except Exception as e:
        messagebox.showerror("Грешка", f"Неуспешно зареждане на категории:\n{e}")
        return

    category_names = list(categories.values())

    selected_category = tk.StringVar()
    category_combobox = ttk.Combobox(win, textvariable=selected_category, values=category_names, state="readonly")
    category_combobox.pack()

    tree = ttk.Treeview(win, columns=("ProductID", "ProductName", "CategoryID"), show="headings")
    tree.heading("ProductID", text="Код на продукта")
    tree.heading("ProductName", text="Име на продукта")
    tree.heading("CategoryID", text="Категория")

    tree.column("ProductID", width=80, anchor="center")
    tree.column("ProductName", width=200, anchor="w")
    tree.column("CategoryID", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def search_by_category():
        selected_name = selected_category.get()
        for i in tree.get_children():
            tree.delete(i)

        if not selected_name:
            messagebox.showerror("Грешка", "Моля, изберете категория!")
            return
        category_id = None
        for key, value in categories.items():
            if value == selected_name:
                category_id = key
                break

        try:
            with open("Products.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                found = False
                for row in reader:
                    if row[2] == category_id:
                        tree.insert("", "end", values=(row[0], row[1], selected_name))
                        found = True
                if not found:
                    messagebox.showinfo("Резултат", "Няма продукти в тази категория.")
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно отваряне на файла:\n{e}")

    tk.Button(win, text="Търси", command=search_by_category).pack(pady=10)

def show_EditProducts():
    win = tk.Toplevel(root)
    win.title("Редактиране на продукт")
    win.geometry("700x600")

    tree = ttk.Treeview(win, columns=("ProductID", "ProductName", "CategoryID"), show="headings")
    tree.heading("ProductID", text="Код на продукта")
    tree.heading("ProductName", text="Име на продукта")
    tree.heading("CategoryID", text="Категория")

    tree.column("ProductID", width=80, anchor="center")
    tree.column("ProductName", width=250, anchor="w")
    tree.column("CategoryID", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_products():
        for i in tree.get_children():
            tree.delete(i)
        try:
            with open("Products.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if not row: continue
                    tree.insert("", "end", values=(row[0], row[1], row[2]))
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно отваряне на файла:\n{e}")

    load_products()

    form_frame = tk.Frame(win)
    form_frame.pack()

    tk.Label(form_frame, text="Код на продукта:").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(form_frame, text="Име на продукта:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(form_frame, text="Категория:").grid(row=2, column=0, padx=5, pady=5)

    product_id_entry = tk.Entry(form_frame)
    product_name_entry = tk.Entry(form_frame)
    category_id_entry = tk.Entry(form_frame)

    product_id_entry.grid(row=0, column=1, padx=5, pady=5)
    product_name_entry.grid(row=1, column=1, padx=5, pady=5)
    category_id_entry.grid(row=2, column=1, padx=5, pady=5)

    def on_tree_select(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        if values:
            product_id_entry.delete(0, tk.END)
            product_id_entry.insert(0, values[0])
            product_name_entry.delete(0, tk.END)
            product_name_entry.insert(0, values[1])
            category_id_entry.delete(0, tk.END)
            category_id_entry.insert(0, values[2])

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def save_changes():
        pid = product_id_entry.get().strip()
        pname = product_name_entry.get().strip()
        cid = category_id_entry.get().strip()
        if not (pid and pname and cid):
            messagebox.showerror("Грешка", "Всички полета са задължителни!")
            return
        products = []
        found = False
        try:
            with open("Products.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row and row[0] == pid:
                        products.append([pid, pname, cid])
                        found = True
                    else:
                        products.append(row)
            if not found:
                messagebox.showerror("Грешка", "Продукт с този ProductID не е намерен!")
                return
            with open("Products.csv", "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(products)
            messagebox.showinfo("Успех", "Продуктът е редактиран успешно!")
            load_products()
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно записване във файла:\n{e}")

    def delete_product():
        pid = product_id_entry.get().strip()
        if not pid:
            messagebox.showerror("Грешка", "Моля, изберете продукт за изтриване!")
            return
        products = []
        found = False
        try:
            with open("Products.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row and row[0] == pid:
                        found = True
                        continue
                    products.append(row)
            if not found:
                messagebox.showerror("Грешка", "Продукт с този ProductID не е намерен!")
                return
            with open("Products.csv", "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(products)
            messagebox.showinfo("Успех", "Продуктът е изтрит успешно!")
            load_products()
            product_id_entry.delete(0, tk.END)
            product_name_entry.delete(0, tk.END)
            category_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно записване във файла:\n{e}")

    def add_product():
        pid = product_id_entry.get().strip()
        pname = product_name_entry.get().strip()
        cid = category_id_entry.get().strip()
        if not (pid and pname and cid):
            messagebox.showerror("Грешка", "Всички полета са задължителни!")
            return
        try:
            with open("Products.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if row and row[0] == pid:
                        messagebox.showerror("Грешка", "Вече съществува продукт с този ProductID!")
                        return
            with open("Products.csv", "a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([pid, pname, cid])
            messagebox.showinfo("Успех", "Продуктът е добавен успешно!")
            load_products()
            product_id_entry.delete(0, tk.END)
            product_name_entry.delete(0, tk.END)
            category_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Грешка", f"Неуспешно записване във файла:\n{e}")

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Запази промените", command=save_changes, width=18).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Изтрий продукт", command=delete_product, width=18).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Добави продукт", command=add_product, width=18).grid(row=0, column=2, padx=10)

def show_WriteTXT():
    win = tk.Toplevel(root)
    win.title("Запис в текстов файл")
    win.geometry("400x150")

    def write_report():
        try:
            product_to_category = {}
            with open("Products.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 3:
                        product_to_category[row[0]] = row[2]

            category_names = {}
            with open("Types.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if len(row) >= 2:
                        category_names[row[0]] = row[1]

            category_sales = {}
            with open("Sells.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    product_id = row[0]
                    price = float(row[2])
                    quantity = int(row[3])
                    total = price * quantity
                    category_id = product_to_category.get(product_id, "Unknown")
                    category_sales[category_id] = category_sales.get(category_id, 0) + total

            with open("Oborot.txt", "w", encoding="utf-8") as f:
                for cat_id, total in category_sales.items():
                    cat_name = category_names.get(cat_id, "Непозната категория")
                    f.write(f"{cat_name}: {total:.2f} лв.\n")
                f.write("\nОбщо: ")
                f.write(f"{sum(category_sales.values()):.2f} лв.\n")

            messagebox.showinfo("Успех", "Оборотът по категории е записан в 'Oborot.txt'.")

        except Exception as e:
            messagebox.showerror("Грешка", f"Грешка при създаване на отчета:\n{e}")

    tk.Label(win, text="Натисни бутона за запис на оборота в текстов файл:").pack(pady=20)
    tk.Button(win, text="Запиши отчет", command=write_report, font=("Arial", 12)).pack(pady=20)

btn_opts = {"width": 20, "height": 3, "font": ("Arial", 14), "bd": 5}

tk.Button(root, text="Списък с продукти", command=show_Products, **btn_opts).grid(row=0, column=0, padx=20, pady=15)
tk.Button(root, text="Списък с продажби", command=show_Sells,**btn_opts).grid(row=0, column=1, padx=20, pady=15)
tk.Button(root, text="Добави продажба", command=show_AddSells,**btn_opts).grid(row=0, column=2, padx=20, pady=15)
tk.Button(root, text="Търсене на продукт", command=show_Search,**btn_opts).grid(row=1, column=0, padx=20, pady=15)
tk.Button(root, text="Редактиране на продукт", command=show_EditProducts,**btn_opts).grid(row=1, column=1, padx=20, pady=15)
tk.Button(root, text="Запис на оборот", command=show_WriteTXT, **btn_opts).grid(row=1, column=2, padx=20, pady=15)

root.mainloop()