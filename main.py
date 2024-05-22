from flask import Flask, render_template, g, abort, request, jsonify
import sqlite3

app = Flask(__name__)

# Chuyển từ tên riêng sang url
def convert_name_to_url(name):
    return name.lower().replace(' ', '-')

# Chuyển từ url sang tên riêng
def convert_url_to_name(url):
    words = str(url).split('-')
    # Chuyển đổi từng từ thành viết hoa chữ cái đầu tiên
    words = [word.capitalize() for word in words]
    name = ' '.join(words)
    return name

def get_navbar_information():
    # Mở kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('Database/database.db')
    conn.row_factory = sqlite3.Row  # Thiết lập row_factory để trả về từ điển thay vì tuple
    cursor = conn.cursor()
    
    # Lấy thông tin user_id từ bảng users (đây là một ví dụ, bạn cần điều chỉnh cho phù hợp với cấu trúc của cơ sở dữ liệu của bạn)
    # cursor.execute("SELECT user_id FROM users WHERE ...")
    # user_id = cursor.fetchone()[0]  # Giả sử user_id là cột đầu tiên trong kết quả

    if False: ## Chưa đăng nhập
        user_id = 0
    else:
        user_id = 0

    # Truy vấn để lấy thông tin giỏ hàng dựa trên user_id
    cursor.execute("SELECT * FROM Cart WHERE user_id IS ? OR user_id = ?", (user_id, user_id))
    cart = cursor.fetchone()

    total_quantity = 0
    total_amount = 0

    # Lấy thông tin về các mặt hàng trong giỏ hàng dựa vào cart['id']
    if cart:
        # Nếu có giỏ hàng tương ứng, truy vấn để lấy thông tin chi tiết của các mặt hàng trong giỏ hàng dựa trên cart_id và product_id
        cursor.execute("""
            SELECT products.*, CartItems.quantity
            FROM CartItems
            INNER JOIN Products ON CartItems.product_id = products.id
            WHERE CartItems.cart_id = ?
        """, (cart['id'],))
        cart_items = [dict(row) for row in cursor.fetchall()]

        # Tính tổng số lượng hàng và tổng số tiền
        for item in cart_items:
            total_quantity += item['quantity']
            total_amount += item['quantity'] * item['price']

        # Cập nhật giá trị total_quantity và total_amount vào bảng Cart
        cursor.execute("""
            UPDATE cart
            SET total_quantity = ?,
                total_amount = ?
            WHERE id = ?
        """, (total_quantity, total_amount, cart['id']))
        conn.commit()

    # Đóng kết nối đến cơ sở dữ liệu
    conn.close()

    # Trả về thông tin đã thu thập được
    return user_id, cart, cart_items

# Hàm để kết nối cơ sở dữ liệu
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database/database.db')
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
    cursor = db.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    for product in products:
        product['url'] = '/shop/products/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Chọn ra 3 sản phẩm tiêu biểu (Tùy chọn tiêu chí)
    top_priced_products = sorted(products, key=lambda x: x['final_price'], reverse=True)[:3]

    user_id, cart, cart_items = get_navbar_information()

    return render_template("home.html", user_id = user_id, cart = cart, cart_items = cart_items, top_products = top_priced_products)

# Route để hiển thị danh sách sản phẩms
@app.route("/shop")
def shop():
    db = get_db()
    cursor = db.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]
    categories = db.execute('SELECT DISTINCT category FROM products').fetchall()
    
    for product in products:
        product['url'] = '/shop/products/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Tìm sản phẩm bán chạy nhất
    best_selling_product = max(products, key=lambda x: x['bought']) if products else None

    # Tạo url cho categories
    categories = [{'category': row['category'], 'category_url': '/shop/' + convert_name_to_url(row['category'])} for row in categories]

    return render_template('shop.html', categories=categories, products=products, best_selling_product=best_selling_product)

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

    cursor = db.execute('SELECT * FROM products WHERE LOWER(REPLACE(category, " ", "-")) = ?', (category_name,))
    categories = db.execute('SELECT DISTINCT category FROM products').fetchall()
    
    products_by_category = [dict(row) for row in cursor.fetchall()]
    for product in products_by_category:
        product['url'] = '/shop/products/' + product['url']
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)

    # Tạo title hoàn chỉnh với tên trang web và tên danh mục
    title = convert_url_to_name(category_name)

    # Tạo url cho categories
    categories = [{'category': row['category'], 'category_url': '/shop/' + convert_name_to_url(row['category'])} for row in categories]
    
    return render_template('category.html', title = title, categories=categories, category_name=category_name, products_by_category=products_by_category)

# Route để hiển thị chi tiết sản phẩm
@app.route('/shop/products/<product_name>')
def product_detail(product_name):
    db = get_db()
    cursor = db.execute('SELECT * FROM products WHERE url = ?', (product_name,))
    product = cursor.fetchone()
    if product:
        # Chuyển đổi đối tượng Row thành dictionary
        product = dict(product)
        # Tính giá sau khi giảm giá
        product['final_price'] = product['price'] * (1 - product['discount'] / 100)
    else:
        abort(404)
    return render_template('product-detail.html', product=product)

# Route update cart_quantity
@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    try:
        conn = sqlite3.connect('Database/database.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE CartItems
            SET quantity = ?
            WHERE product_id = ?
        ''', (quantity, product_id))
        
        conn.commit()
        conn.close()

        print("Cart quantity updated")
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
