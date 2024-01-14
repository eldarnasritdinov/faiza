import sqlite3

conn = sqlite3.connect('food.db')
c = conn.cursor()

c.execute(
    """
          CREATE TABLE IF NOT EXISTS orders
          (
          [customer_id] INTEGER PRIMARY KEY AUTOINCREMENT, 
          [customer_name] TEXT,
          [dish_name] TEXT,
          [arrival_time] TEXT
          )
          """
)

conn.commit()

conn.close()