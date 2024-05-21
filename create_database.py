import sqlite3

conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# Tạo bảng Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Tạo bảng Products
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    discount REAL NOT NULL,
    bought REAL NOT NULL,
    inventory REAL,
    image_url TEXT NOT NULL
)
''')

# Tạo bảng Cart
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cart (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    total_quantity INTEGER NOT NULL,
    total_amount INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id)
)
''')

# Tạo bảng CartItems
cursor.execute('''
CREATE TABLE IF NOT EXISTS CartItems (
    id INTEGER PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES Cart(id),
    FOREIGN KEY (product_id) REFERENCES Products(id)
)
''')

################################################################################################################

# # Thêm một vài sản phẩm mẫu
# cursor.execute("INSERT INTO Products (name, url, category, description, price, discount, bought, inventory, image_url) VALUES ('Gift Card', 'gift-card', 'Gift Cards', 'Description of Product 1', 25.99, 0.0, 10, 100, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f06b4_acme-gift-card.jpg')")
# cursor.execute("INSERT INTO Products (name, url, category, description, price, discount, bought, inventory, image_url) VALUES ('Tin Coffee Tumbler', 'tin-coffee-tumbler', 'Accessories', 'Description of Product 2', 35.99, 0.0, 20, 200, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f067d_ryan-holloway-JyDmUaXMib4-unsplash.jpg')")
# cursor.execute("INSERT INTO Products (name, url, category, description, price, discount, bought, inventory, image_url) VALUES ('Blue Canvas Pack', 'blue-canvas-pack' ,'Packs', 'Description of Product 3', 95.00, 50.0, 30, 300, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f0669_denisse-leon-J7CjWufjmg4-unsplash.jpg')")
# cursor.execute("INSERT INTO Products (name, url, category, description, price, discount, bought, inventory, image_url) VALUES ('Green Canvas Pack', 'green-canvas-pack', 'Packs', 'Description of Product 4', 39.99, 0.0, 30, 300, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f0646_jakob-owens-O_bhy3TnSYU-unsplash.jpg')")
# cursor.execute("INSERT INTO Products (name, url, category, description, price, discount, bought, inventory, image_url) VALUES ('Product 5', 'product-5', 'Tents', 'Description of Product 5', 200.99, 0.0, 100, 1000, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f06ae_patrick-hendry-eDgUyGu93Yw-unsplash.jpg')")

# Kiểm tra xem có giỏ hàng nào với user_id là 0 hay không
cursor.execute('SELECT id FROM Cart WHERE user_id = 0')
existing_cart = cursor.fetchone()

# # Nếu không có giỏ hàng nào với user_id là 0, tạo một giỏ hàng mới với user_id là 0
if not existing_cart:
    cursor.execute('''
        INSERT INTO Cart (user_id, total_quantity, total_amount)
        VALUES (?, 0, 0)
    ''', (0,))
    conn.commit()  # Chắc chắn lưu thay đổi vào cơ sở dữ liệu

    # Lấy cart_id của giỏ hàng mới được tạo
    cart_id = cursor.lastrowid
else:
    # Nếu có giỏ hàng với user_id là 0, sử dụng giỏ hàng đó
    cart_id = existing_cart['id']

# Thêm các mục vào giỏ hàng
def get_product_price(product_id):
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM Products WHERE id = ?', (product_id,))
    row = cursor.fetchone()
    
    if row:
        price = row[0]
    else:
        price = None

    conn.close()
    
    return price

products_to_add = [
    (1, 2),  # Sản phẩm có id = 1 với số lượng là 2
    (3, 1),  # Sản phẩm có id = 3 với số lượng là 1
    # Thêm các sản phẩm khác tương tự ở đây nếu cần
]

for product_id, quantity in products_to_add:
    price = get_product_price(product_id)
    if price is not None:
        cursor.execute('''
            INSERT INTO CartItems (cart_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (cart_id, product_id, quantity, quantity * price))
    else:
        print(f"Không tìm thấy giá cho sản phẩm có id {product_id}.")


conn.commit()
conn.close()