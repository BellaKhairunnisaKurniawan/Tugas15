import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your actual password
        database="infopenjualan"
    )

def create_sale(tanggal, jenis, jumlah, harga, total):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO datapenjualan (tanggal_pembelian, jenis_produk, jumlah_order, harga_satuan, total_harga) VALUES (%s, %s, %s, %s, %s)",
        (tanggal, jenis, jumlah, harga, total)
    )
    connection.commit()
    connection.close()

def read_sales():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM datapenjualan")
    sales = cursor.fetchall()  # Returns a list of tuples
    connection.close()
    return sales

def update_sale(id, tanggal, jenis, jumlah, harga, total):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE datapenjualan SET tanggal_pembelian=%s, jenis_produk=%s, jumlah_order=%s, harga_satuan=%s, total_harga=%s WHERE id=%s",
        (tanggal, jenis, jumlah, harga, total, id)
    )
    connection.commit()
    connection.close()

def delete_sale(id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM datapenjualan WHERE id=%s", (id,))
    connection.commit()
    connection.close()

def get_total_revenue():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(total_harga) FROM datapenjualan")
    total = cursor.fetchone()[0] or 0
    connection.close()
    return total

def get_sales_data_for_graph():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT tanggal_pembelian, SUM(total_harga) FROM datapenjualan GROUP BY tanggal_pembelian")
    data = cursor.fetchall()  # Returns a list of tuples
    connection.close()
    return data
