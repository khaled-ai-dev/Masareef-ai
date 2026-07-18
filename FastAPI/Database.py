import sqlite3

Database_Name = "Database/transactions.db"

def Create_Database():
    Connection = sqlite3.connect(Database_Name)
    Cursor = Connection.cursor()

    Cursor.execute("""
                   CREATE TABLE IF NOT EXISTS transactions (

                   id INTEGER PRIMARY KEY AUTOINCREMENT,

                   Merchant TEXT,

                   category TEXT,

                   amount REAL,

                   transaction_type TEXT,

                   transaction_date TEXT,

                   original_sms TEXT)

                   """)
    

    Connection.commit()
    Connection.close()


def Save_Transaction(merchant, category, amount, transaction_type, transaction_date, Original_SMS):
    Connection = sqlite3.connect(Database_Name)
    Cursor = Connection.cursor()
    Cursor.execute("""INSERT INTO transactions (Merchant, category, amount, transaction_type, transaction_date, Original_SMS)
                      VALUES (?, ?, ?, ?, ?, ?)""", #? placeholders are better here, since its the safest way in sqlite3 to insert data & handles the arabic text correctly.
                    (merchant, category, amount, transaction_type, transaction_date, Original_SMS))
    Connection.commit()
    Connection.close()