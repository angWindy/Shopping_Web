import sqlite3

# Kết nối đến cơ sở dữ liệu (tạo mới nếu chưa tồn tại)
conn = sqlite3.connect('database/products.db')
cursor = conn.cursor()

# Tạo bảng products với cấu trúc mới nếu chưa tồn tại
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    discount REAL NOT NULL,
    bought REAL NOT NULL,
    inventory REAL,
    image_url TEXT NOT NULL
)
''')

# Thêm một vài sản phẩm mẫu
cursor.execute("INSERT INTO products (name, category, description, price, discount, bought, inventory, image_url) VALUES ('Gift Card', 'Gift Cards', 'Description of Product 1', 25.99, 0.0, 10, 100, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f06b4_acme-gift-card.jpg')")
cursor.execute("INSERT INTO products (name, category, description, price, discount, bought, inventory, image_url) VALUES ('Tin Coffee Tumbler', 'Accessories', 'Description of Product 2', 35.99, 0.0, 20, 200, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f067d_ryan-holloway-JyDmUaXMib4-unsplash.jpg')")
cursor.execute("INSERT INTO products (name, category, description, price, discount, bought, inventory, image_url) VALUES ('Blue Canvas Pack', 'Packs', 'Description of Product 3', 95.00, 50.0, 30, 300, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f0669_denisse-leon-J7CjWufjmg4-unsplash.jpg')")
cursor.execute("INSERT INTO products (name, category, description, price, discount, bought, inventory, image_url) VALUES ('Green Canvas Pack', 'Packs', 'Description of Product 4', 39.99, 15.0, 30, 300, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f0646_jakob-owens-O_bhy3TnSYU-unsplash.jpg')")
cursor.execute("INSERT INTO products (name, category, description, price, discount, bought, inventory, image_url) VALUES ('Product 5', 'Tents', 'Description of Product 5', 200.99, 0.0, 100, 1000, 'https://assets-global.website-files.com/6644881a99e1e50c056f0640/6644881a99e1e50c056f06ae_patrick-hendry-eDgUyGu93Yw-unsplash.jpg')")

conn.commit()
conn.close()
