from flask import Flask, render_template, g, abort
import sqlite3

app = Flask(__name__)

# Hàm để kết nối cơ sở dữ liệu
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database/products.db')
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
    db = get_db()
    cursor = db.execute('SELECT id, name, url, price, discount, category, bought, image_url FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    for product in products:
        product['url'] = '/shop/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Chọn ra 3 sản phẩm tiêu biểu (Tùy chọn tiêu chí)
    top_priced_products = sorted(products, key=lambda x: x['final_price'], reverse=True)[:3]

    return render_template("home.html", top_products = top_priced_products)

# Route để hiển thị danh sách sản phẩm
@app.route("/shop")
def shop():
    db = get_db()
    cursor = db.execute('SELECT id, name, url, price, discount, category, bought, image_url FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    for product in products:
        product['url'] = '/shop/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Tìm sản phẩm bán chạy nhất
    best_selling_product = max(products, key=lambda x: x['bought']) if products else None

    return render_template('shop.html', products=products, best_selling_product=best_selling_product)

# Route để hiển thị phần liên lạc (Contacts)
@app.route("/contact")
def contact():
    return render_template('contact.html')

# Route để hiển thị phần thanh toán (Checkout)
@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

# Route để hiển thị danh sách sản phẩm theo danh mục
@app.route('/shop/<category_name>')
def category(category_name):
    db = get_db()

    cursor = db.execute('SELECT id, name, url, price, discount, category, bought, image_url FROM products WHERE LOWER(REPLACE(category, " ", "-")) = ?', (category_name,))
    products_by_category = [dict(row) for row in cursor.fetchall()]
    for product in products_by_category:
        product['url'] = '/shop/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Tạo title hoàn chỉnh với tên trang web và tên danh mục
    words = str(category_name).split('-')
    # Chuyển đổi từng từ thành viết hoa chữ cái đầu tiên
    words = [word.capitalize() for word in words]
    title = ' '.join(words)
    

    return render_template('category.html', title = title, category_name=category_name, products_by_category=products_by_category)



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
