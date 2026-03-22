from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price INTEGER,
        image TEXT,
        stock INTEGER,
        category TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        qty INTEGER,
        price INTEGER,
        status TEXT
    )
    """)

    conn.commit()

    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        products = [
            ("Rice", 60, "", 20, "Food"),
            ("Oil", 120, "", 15, "Food"),
            ("Sugar", 45, "", 25, "Food"),
            ("Salt", 20, "", 40, "Food"),
            ("Milk", 50, "", 30, "Food"),
            ("Bread", 30, "", 25, "Food"),
            ("Soap", 35, "", 30, "Daily"),
            ("Shampoo", 120, "", 10, "Daily"),
            ("Toothpaste", 80, "", 20, "Daily"),
            ("Detergent", 150, "", 15, "Daily"),

            ("Tea", 100, "", 20, "Food"),
            ("Coffee", 200, "", 15, "Food"),
            ("Biscuits", 25, "", 40, "Food"),
            ("Chips", 30, "", 50, "Food"),
            ("Maggi", 15, "", 60, "Food"),
            ("Butter", 55, "", 20, "Food"),
            ("Cheese", 90, "", 15, "Food"),
            ("Handwash", 70, "", 25, "Daily"),
            ("Facewash", 120, "", 20, "Daily"),
            ("Perfume", 250, "", 10, "Daily")
        ]
        c.executemany("INSERT INTO products VALUES (NULL,?,?,?,?,?)", products)
        conn.commit()

    conn.close()


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form["username"]
        session["cart"] = {}
        return redirect("/catalog")
    return render_template("login.html")


# ---------------- CATALOG ----------------
@app.route("/catalog")
def catalog():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    data = c.fetchall()
    conn.close()

    products = [{
        "id": str(d[0]),
        "name": d[1],
        "price": d[2],
        "image": d[3],
        "stock": d[4]
    } for d in data]

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template("catalog.html",
                           products=products,
                           cart_count=cart_count)


# ---------------- ADD TO CART ----------------
@app.route("/add", methods=["POST"])
def add():
    pid = str(request.form["product_id"])
    cart = session.get("cart", {})

    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart

    return redirect("/catalog")


# ---------------- CART ----------------
@app.route("/cart", methods=["GET", "POST"])
def cart():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    cart = session.get("cart", {})
    items = []
    total = 0

    for pid, qty in cart.items():
        c.execute("SELECT * FROM products WHERE id=?", (pid,))
        row = c.fetchone()

        if row:
            subtotal = row[2] * qty
            items.append({
                "id": pid,
                "name": row[1],
                "qty": qty,
                "price": row[2],
                "subtotal": subtotal
            })
            total += subtotal

    final = total

    if request.method == "POST":
        discount = int(request.form["discount"])
        final = int(total - (total * discount / 100))
        session["final"] = final
        return redirect("/payment")

    conn.close()
    return render_template("cart.html",
                           items=items,
                           total=total,
                           final=final)


# ---------------- QUANTITY ----------------
@app.route("/increase/<pid>")
def increase(pid):
    cart = session.get("cart", {})
    cart[pid] = cart.get(pid, 0) + 1
    session["cart"] = cart
    return redirect("/cart")


@app.route("/decrease/<pid>")
def decrease(pid):
    cart = session.get("cart", {})
    if pid in cart:
        cart[pid] -= 1
        if cart[pid] <= 0:
            del cart[pid]
    session["cart"] = cart
    return redirect("/cart")


# ---------------- PAYMENT ----------------
@app.route("/payment", methods=["GET", "POST"])
def payment():
    total = session.get("final", 0)

    if request.method == "POST":
        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        cart = session.get("cart", {})

        for pid, qty in cart.items():
            c.execute("SELECT * FROM products WHERE id=?", (pid,))
            row = c.fetchone()

            if row:
                c.execute("INSERT INTO orders VALUES (NULL,?,?,?,?)",
                          (row[1], qty, row[2]*qty, "Pending"))

        conn.commit()
        session["cart"] = {}
        conn.close()

        return redirect("/orders")

    return render_template("payment.html", total=total)


# ---------------- ORDERS ----------------
@app.route("/orders")
def orders():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    data = c.fetchall()
    conn.close()

    orders = [{
        "name": d[1],
        "qty": d[2],
        "price": d[3],
        "status": d[4]
    } for d in data]

    return render_template("orders.html", orders=orders)


# ---------------- DELIVERY ----------------
@app.route("/delivery")
def delivery():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    data = c.fetchall()
    conn.close()

    orders = [{
        "id": d[0],
        "name": d[1],
        "status": d[4]
    } for d in data]

    return render_template("delivery.html", orders=orders)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    status = request.form["status"]

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE orders SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()

    return redirect("/delivery")


@app.route("/clear_orders")
def clear_orders():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
    return redirect("/delivery")


# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)