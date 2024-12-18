import sqlite3

connection = sqlite3.connect('module_14_4.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON Products(id)')

    for i in range(1, 5):
        cursor.execute("INSERT INTO Products(title, description, price) VALUES (?, ?, ?)",
                         (f"Название: {i}", f"Описание: {i}", f"Цена: {i*1000}"))

    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('module_14_4.db')
    cursor = connection.cursor()
    products = cursor.execute('SELECT * FROM Products').fetchall()
    connection.commit()
    connection.close()
    return products