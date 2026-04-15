from flask import Flask, render_template, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Create DB + Sample Data
def init_db():
    conn = sqlite3.connect("food.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS food
                 (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)''')

    # Sample food items
    conn.execute("INSERT OR IGNORE INTO food VALUES (1,'Pizza',250)")
    conn.execute("INSERT OR IGNORE INTO food VALUES (2,'Burger',120)")
    conn.execute("INSERT OR IGNORE INTO food VALUES (3,'Pasta',180)")
    conn.execute("INSERT OR IGNORE INTO food VALUES (4,'Fries',100)")
    conn.commit()
    conn.close()

init_db()

# HOME PAGE
@app.route('/')
def index():
    conn = sqlite3.connect("food.db")
    items = conn.execute("SELECT * FROM food").fetchall()
    conn.close()
    return render_template('index.html', items=items)

# ADD TO CART
@app.route('/add/<int:id>')
def add(id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(id)
    session.modified = True
    return redirect('/')

# VIEW CART
@app.route('/cart')
def cart():
    if 'cart' not in session:
        return render_template('cart.html', items=[], total=0)

    conn = sqlite3.connect("food.db")
    cart_items = []
    total = 0

    for i in session['cart']:
        item = conn.execute("SELECT * FROM food WHERE id=?", (i,)).fetchone()
        cart_items.append(item)
        total += item[2]

    conn.close()
    return render_template('cart.html', items=cart_items, total=total)

# REMOVE ITEM
@app.route('/remove/<int:id>')
def remove(id):
    if 'cart' in session and id in session['cart']:
        session['cart'].remove(id)
        session.modified = True
    return redirect('/cart')

# ORDER
@app.route('/order')
def order():
    session.pop('cart', None)
    return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)