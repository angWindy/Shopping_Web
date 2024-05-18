from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)

# Hàm để kết nối cơ sở dữ liệu
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('products.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Đóng kết nối cơ sở dữ liệu khi kết thúc request
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Route để hiển thị trang chủ
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Route để hiển thị danh sách sản phẩm
@app.route("/shop")
def shop():
    db = get_db()
    # cursor = db.execute('SELECT id, name, price, category, image_url FROM products')
    # products = cursor.fetchall()
    return render_template('shop.html')

# Route để hiển thị phần liên lạc (Contacts)
@app.route("/contact")
def contact():
    return render_template('contact.html')

# Route để hiển thị phần thanh toán (Checkout)
@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

# Route để hiển thị chi tiết sản phẩm
# @app.route('/shop/<int:product_id>')
# def product_detail(product_id):
#     db = get_db()
#     cursor = db.execute('SELECT * FROM products WHERE id = ?', (product_id,))
#     product = cursor.fetchone()
#     if product is None:
#         abort(404)
#     return render_template('Shop/product-detail.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
