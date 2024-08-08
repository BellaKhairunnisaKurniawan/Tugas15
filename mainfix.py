import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", 
        database="infopenjualan"
    )

def create_sale(date, category, quantity, unit_price, total):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO datapenjualan (tanggal_pembelian, jenis_produk, jumlah_order, harga_satuan, total_harga) VALUES (%s, %s, %s, %s, %s)",
        (date, category, quantity, unit_price, total)
    )
    connection.commit()
    connection.close()

def read_sales(start_date=None, end_date=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    if start_date and end_date:
        cursor.execute("SELECT * FROM datapenjualan WHERE tanggal_pembelian BETWEEN %s AND %s", (start_date, end_date))
    else:
        cursor.execute("SELECT * FROM datapenjualan")
    sales = cursor.fetchall()
    connection.close()
    return sales

def update_sale(id, date, category, quantity, unit_price, total):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE datapenjualan SET tanggal_pembelian=%s, jenis_produk=%s, jumlah_order=%s, harga_satuan=%s, total_harga=%s WHERE id=%s",
        (date, category, quantity, unit_price, total, id)
    )
    connection.commit()
    connection.close()

def delete_sale(id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM datapenjualan WHERE id=%s", (id,))
    connection.commit()
    connection.close()

def get_sales_data_for_graph(start_date=None, end_date=None):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    query = """
        SELECT DATE_FORMAT(tanggal_pembelian, '%Y-%m-%d') as date, jenis_produk, SUM(total_harga) 
        FROM datapenjualan
    """
    
    if start_date and end_date:
        query += " WHERE tanggal_pembelian BETWEEN %s AND %s"
    
    query += " GROUP BY date, jenis_produk ORDER BY date"
    
    if start_date and end_date:
        cursor.execute(query, (start_date, end_date))
    else:
        cursor.execute(query)
    
    data = cursor.fetchall()
    connection.close()
    return data

class SalesApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Data Penjualan")
        self.geometry("900x600")

        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        menu_frame = tk.Frame(paned_window, bg="#f0f0f0", width=150)
        menu_frame.pack_propagate(False)
        paned_window.add(menu_frame)

        content_frame = tk.Frame(paned_window)
        content_frame.pack(fill=tk.BOTH, expand=True)
        paned_window.add(content_frame)

        self.frames = {}
        for F in (StartPage, InsertPage, UpdatePage, DeletePage, ShowPage, GraphPage):
            page_name = F.__name__
            frame = F(parent=content_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        self.create_menu_buttons(menu_frame)

    def create_menu_buttons(self, parent):
        tk.Label(parent, text="Menu", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Button(parent, text="Insert Data", command=lambda: self.show_frame("InsertPage")).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(parent, text="Update Data", command=lambda: self.show_frame("UpdatePage")).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(parent, text="Delete Data", command=lambda: self.show_frame("DeletePage")).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(parent, text="Show Data", command=lambda: self.show_frame("ShowPage")).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(parent, text="Show Graph", command=lambda: self.show_frame("GraphPage")).pack(pady=10, padx=10, fill=tk.X)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "ShowPage":
            frame.show_data()  # Refresh data 

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#e0e0e0")

        title_label = tk.Label(self, text="Home Page", font=("Helvetica", 24, "bold"), bg="#e0e0e0")
        title_label.pack(side="top", fill="x", pady=20)

        tk.Label(self, text="Welcome to the Sales Data Management System", font=("Helvetica", 14), bg="#e0e0e0").pack(pady=10)

class InsertPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#e0f7fa")

        title_label = tk.Label(self, text="Insert Data", font=("Helvetica", 24, "bold"), bg="#e0f7fa")
        title_label.pack(side="top", fill="x", pady=20)

        self.date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()

        form_frame = tk.Frame(self, bg="#b2ebf2")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg="#b2ebf2").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.date_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Category", bg="#b2ebf2").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.category_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Quantity", bg="#b2ebf2").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.quantity_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Unit Price", bg="#b2ebf2").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.unit_price_var).grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self, text="Submit", command=self.insert_data, bg="#4caf50", fg="white").pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), bg="#f44336", fg="white").pack(pady=10)

    def insert_data(self):
        date = self.date_var.get()
        category = self.category_var.get()
        try:
            quantity = int(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            total = quantity * unit_price
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Unit Price must be a number.")
            return

        create_sale(date, category, quantity, unit_price, total)
        messagebox.showinfo("Success", "Data inserted successfully")
        self.reset_fields()
        self.controller.show_frame("ShowPage")  # Refresh the ShowPage

    def reset_fields(self):
        self.date_var.set("")
        self.category_var.set("")
        self.quantity_var.set("")
        self.unit_price_var.set("")

class UpdatePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#c8e6c9")

        title_label = tk.Label(self, text="Update Data", font=("Helvetica", 24, "bold"), bg="#c8e6c9")
        title_label.pack(side="top", fill="x", pady=20)

        self.id_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()

        form_frame = tk.Frame(self, bg="#a5d6a7")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="ID", bg="#a5d6a7").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.id_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg="#a5d6a7").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.date_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Category", bg="#a5d6a7").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.category_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Quantity", bg="#a5d6a7").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.quantity_var).grid(row=3, column=1, padx=10, pady=10, sticky="w")
        tk.Label(form_frame, text="Unit Price", bg="#a5d6a7").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.unit_price_var).grid(row=4, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self, text="Submit", command=self.update_data, bg="#4caf50", fg="white").pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), bg="#f44336", fg="white").pack(pady=10)

    def update_data(self):
        id = self.id_var.get()
        date = self.date_var.get()
        category = self.category_var.get()
        try:
            quantity = int(self.quantity_var.get())
            unit_price = float(self.unit_price_var.get())
            total = quantity * unit_price
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and Unit Price must be a number.")
            return

        update_sale(id, date, category, quantity, unit_price, total)
        messagebox.showinfo("Success", "Data updated successfully")
        self.reset_fields()
        self.controller.show_frame("ShowPage")  # Refresh the ShowPage

    def reset_fields(self):
        self.id_var.set("")
        self.date_var.set("")
        self.category_var.set("")
        self.quantity_var.set("")
        self.unit_price_var.set("")

class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#ffccbc")

        title_label = tk.Label(self, text="Delete Data", font=("Helvetica", 24, "bold"), bg="#ffccbc")
        title_label.pack(side="top", fill="x", pady=20)

        self.id_var = tk.StringVar()

        form_frame = tk.Frame(self, bg="#ffab91")
        form_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="ID", bg="#ffab91").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(form_frame, textvariable=self.id_var).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Button(self, text="Delete", command=self.delete_data, bg="#d32f2f", fg="white").pack(pady=20)
        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), bg="#f44336", fg="white").pack(pady=10)

    def delete_data(self):
        id = self.id_var.get()
        delete_sale(id)
        messagebox.showinfo("Success", "Data deleted successfully")
        self.id_var.set("")
        self.controller.show_frame("ShowPage")  # Refresh the ShowPage

class ShowPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#fff9c4")

        title_label = tk.Label(self, text="Show Data", font=("Helvetica", 24, "bold"), bg="#fff9c4")
        title_label.pack(side="top", fill="x", pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Date", "Category", "Quantity", "Unit Price", "Total Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Unit Price", text="Unit Price")
        self.tree.heading("Total Price", text="Total Price")
        self.tree.pack(fill=tk.BOTH, expand=True)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), bg="#fbc02d", fg="white").pack(pady=10)

    def show_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        sales = read_sales()
        for sale in sales:
            self.tree.insert("", "end", values=sale)

class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#e1bee7")

        title_label = tk.Label(self, text="Show Graph", font=("Helvetica", 24, "bold"), bg="#e1bee7")
        title_label.pack(side="top", fill="x", pady=20)

        self.canvas_frame = tk.Frame(self, bg="#d1c4e9")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        tk.Button(self, text="Back to Home", command=lambda: controller.show_frame("StartPage"), bg="#f06292", fg="white").pack(pady=10)
        tk.Button(self, text="Refresh Graph", command=self.show_graph, bg="#ab47bc", fg="white").pack(pady=10)

        self.show_graph()  

    def show_graph(self):
        data = get_sales_data_for_graph()
        if not data:
            messagebox.showwarning("No Data", "No data available to plot.")
            return

        dates = list(sorted(set(d[0] for d in data)))
        categories = list(sorted(set(d[1] for d in data)))
        
        income_by_category = {category: [0] * len(dates) for category in categories}
        
        date_index = {date: idx for idx, date in enumerate(dates)}

        for row in data:
            date, category, total = row
            if date in date_index and category in income_by_category:
                income_by_category[category][date_index[date]] = total

        fig, ax = plt.subplots(figsize=(12, 8))
        
        bar_width = 0.8 / len(categories)
        index = range(len(dates))
        
        for i, category in enumerate(categories):
            bar_positions = [pos + i * bar_width for pos in index]
            ax.bar(bar_positions, income_by_category[category], width=bar_width, label=category)

        ax.set_xlabel('Date')
        ax.set_ylabel('Total Pendapatan (Rp)')
        ax.set_title('Total Pendapatan by Category Over Time')
        ax.set_xticks([pos + (bar_width * (len(categories) / 2)) for pos in index])
        ax.set_xticklabels(dates, rotation=45, ha='right')
        ax.legend(title="Product Category")
        ax.grid(axis='y')

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.canvas_widget = FigureCanvasTkAgg(fig, self.canvas_frame)
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas_widget.draw()

if __name__ == "__main__":
    app = SalesApp()
    app.mainloop()
