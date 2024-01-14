"""
1. Возможность удалять заказы
2. Добавить время заказа
3. Сделать красиво
4. Отменить заказ
5. Добавить в эту же базу таблицу блюд и брать блюда оттуда
6. Добавить страницу для админа, чтобы добавлять или удалять блюда

ADVANCED
7. Возможность выбора нескольких блюд
"""


from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("food.db", check_same_thread=False)
c = conn.cursor()

# список блюд
DISHES = [
    "Ramen",
    "Laghman",
    "Plov",
    "Khachapuri",
    "Pizza",
    "Sushi",
    "Spaghetti"
]

@app.route("/")
def index():
    """
    Первая страница
    """
    return render_template('index.html', dishes = DISHES)

@app.route("/register", methods=["POST"])
def register():
    """
    Страница регистрации
    """
    # забираем имя и блюда заказа
    name = request.form.get("name")
    dish = request.form.get("dish")
    time = request.form.get("time")

    # записываем заказ в базу
    c.execute("INSERT INTO orders(customer_name, dish_name, arrival_time) VALUES (?, ?, ?)", (name, dish, time))
    conn.commit()
    
    # рендерим новую страничку принятия заказа
    return render_template('register.html', name=name, dish=dish, time=time)

@app.route("/orders")
def orders():
    """
    Возвращает повару все принятые заказы
    """
    foods = c.execute("SELECT * FROM orders")
    foods = foods.fetchall()
    return render_template('orders.html', foods=foods)

@app.route("/admin")
def admin():

    foods = c.execute("SELECT * FROM orders")
    foods = foods.fetchall()
    return render_template('admin.html', foods=foods)

@app.route("/delete_order", methods=["POST"])
def delete_order():
    if request.method == "POST":
        order_id = request.form.get("order_id")
        if order_id:
            conn = sqlite3.connect('food.db')
            c = conn.cursor()
            
            c.execute("DELETE FROM orders WHERE customer_id=?", (order_id,))
            
            conn.commit()
            conn.close()
            
    return redirect("/admin")

# Если программа запущена напрямую, то запустить приложение
if __name__ == '__main__':
    app.run(debug=True)