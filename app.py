from flask import Flask, render_template
from db import get_connection

app = Flask(__name__)


def get_products_from_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, price, sold, rating, img, link, added_at FROM lazada_products ORDER BY added_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


@app.route("/")
def home():
    products = get_products_from_db()
    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
