import tkinter as tk
from tkinter import ttk, messagebox
from crud import create_sale, read_sales, update_sale, delete_sale, get_total_revenue, get_sales_data_for_graph
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Penjualan")
        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        # Input Form
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(pady=10)

        ttk.Label(self.form_frame, text="Tanggal Pembelian").grid(row=0, column=0, padx=5, pady=5)
        self.entry_tanggal = ttk.Entry(self.form_frame)
        self.entry_tanggal.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Jenis Produk").grid(row=1, column=0, padx=5, pady=5)
        self.entry_jenis = ttk.Entry(self.form_frame)
        self.entry_jenis.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Jumlah Order").grid(row=2, column=0, padx=5, pady=5)
        self.entry_jumlah = ttk.Entry(self.form_frame)
        self.entry_jumlah.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Harga Satuan").grid(row=3, column=0, padx=5, pady=5)
        self.entry_harga = ttk.Entry(self.form_frame)
        self.entry_harga.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Total Harga").grid(row=4, column=0, padx=5, pady=5)
        self.entry_total = ttk.Entry(self.form_frame)
        self.entry_total.grid(row=4, column=1, padx=5, pady=5)
        self.entry_total.config(state='readonly')  # Make this read-only

        self.entry_jumlah.bind('<KeyRelease>', self.update_total)
        self.entry_harga.bind('<KeyRelease>', self.update_total)

        self.btn_add = ttk.Button(self.form_frame, text="Add Sale", command=self.add_sale)
        self.btn_add.grid(row=5, column=0, padx=5, pady=5)

        self.btn_update = ttk.Button(self.form_frame, text="Update Sale", command=self.update_sale)
        self.btn_update.grid(row=5, column=1, padx=5, pady=5)

        self.btn_delete = ttk.Button(self.form_frame, text="Delete Sale", command=self.delete_sale)
        self.btn_delete.grid(row=5, column=2, padx=5, pady=5)

        self.btn_graph = ttk.Button(self.form_frame, text="View Graph", command=self.view_graph)
        self.btn_graph.grid(row=6, column=0, padx=5, pady=5)

        self.btn_back = ttk.Button(self.form_frame, text="Back", command=self.go_back)
        self.btn_back.grid(row=6, column=1, padx=5, pady=5)

        # Sales Data Table
        self.table_frame = ttk.Frame(self.root)
        self.table_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Tanggal", "Jenis", "Jumlah", "Harga", "Total"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tanggal", text="Tanggal Pembelian")
        self.tree.heading("Jenis", text="Jenis Produk")
        self.tree.heading("Jumlah", text="Jumlah Order")
        self.tree.heading("Harga", text="Harga Satuan")
        self.tree.heading("Total", text="Total Harga")

        self.tree.pack()

        self.lbl_total_revenue = ttk.Label(self.table_frame, text="Total Revenue: ")
        self.lbl_total_revenue.pack()

        # Variable to hold selected ID for updates
        self.selected_id = None

    def update_total(self, event=None):
        try:
            jumlah = float(self.entry_jumlah.get() or 0)
            harga = float(self.entry_harga.get() or 0)
            total = jumlah * harga
            self.entry_total.config(state='normal')
            self.entry_total.delete(0, tk.END)
            self.entry_total.insert(0, f"{total:.2f}")
            self.entry_total.config(state='readonly')
        except ValueError:
            self.entry_total.config(state='normal')
            self.entry_total.delete(0, tk.END)
            self.entry_total.config(state='readonly')

    def add_sale(self):
        tanggal = self.entry_tanggal.get()
        jenis = self.entry_jenis.get()
        jumlah = self.entry_jumlah.get()
        harga = self.entry_harga.get()
        total = self.entry_total.get()
        create_sale(tanggal, jenis, jumlah, harga, total)
        self.load_sales()

    def update_sale(self):
        if self.selected_id:
            tanggal = self.entry_tanggal.get()
            jenis = self.entry_jenis.get()
            jumlah = self.entry_jumlah.get()
            harga = self.entry_harga.get()
            total = self.entry_total.get()
            update_sale(self.selected_id, tanggal, jenis, jumlah, harga, total)
            self.selected_id = None
            self.load_sales()

    def delete_sale(self):
        if self.selected_id:
            delete_sale(self.selected_id)
            self.selected_id = None
            self.load_sales()

    def load_sales(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        sales = read_sales()
        for sale in sales:
            # Assuming sale is a tuple in the format (id, tanggal_pembelian, jenis_produk, jumlah_order, harga_satuan, total_harga)
            self.tree.insert("", tk.END, values=sale)
        total_revenue = get_total_revenue()
        self.lbl_total_revenue.config(text=f"Total Revenue: {total_revenue}")


    def view_graph(self):
        data = get_sales_data_for_graph()
        dates, totals = zip(*data) if data else ([], [])
        plt.figure(figsize=(10, 6))
        plt.plot(dates, totals, marker='o')
        plt.title("Sales Revenue")
        plt.xlabel("Tanggal Pembelian")
        plt.ylabel("Total Harga")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Embed plot in Tkinter window
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def go_back(self):
        self.entry_tanggal.delete(0, tk.END)
        self.entry_jenis.delete(0, tk.END)
        self.entry_jumlah.delete(0, tk.END)
        self.entry_harga.delete(0, tk.END)
        self.entry_total.delete(0, tk.END)
        self.load_sales()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item, 'values')[0]
            self.selected_id = item_id
            for child in self.tree.get_children():
                if self.tree.item(child, 'values')[0] == item_id:
                    item_values = self.tree.item(child, 'values')[1:]
                    self.entry_tanggal.delete(0, tk.END)
                    self.entry_tanggal.insert(0, item_values[0])
                    self.entry_jenis.delete(0, tk.END)
                    self.entry_jenis.insert(0, item_values[1])
                    self.entry_jumlah.delete(0, tk.END)
                    self.entry_jumlah.insert(0, item_values[2])
                    self.entry_harga.delete(0, tk.END)
                    self.entry_harga.insert(0, item_values[3])
                    self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
