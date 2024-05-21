ecute('SELECT id FROM Cart WHERE user_id = 0')
# existing_cart = cursor.fetchone()

# # Nếu không có giỏ hàng nào với user_id là 0, tạo một giỏ hàng mới với user_id là 0
# if not existing_cart:
#     cursor.execute('INSERT INTO Cart (user_id) VALUES (0)')
#     conn.commit()  # Chắc chắn lưu thay đổi vào cơ sở dữ liệu

#     # Lấy cart_id của giỏ hàng mới được tạo
#     cart_id = cursor.lastrowid
# else:
#     # Nếu có giỏ hàng với user_id là 0, sử dụng giỏ hàng đó
#     cart_id = existing_cart['id']

# # Thêm các mục vào giỏ hàng
# def get_product_price(product_id):
#     conn = sqlite3.connect('database/database.db')
#     cursor = conn.cursor()

#     cursor.execute('SELECT price FROM Products WHERE id = ?', (product_id,))
#     row = cursor.fetchone()
    
#     if row:
#         price = row[0]
#     else:
#         price = None

#     conn.close()
    
#     return price

# products_to_add = [
#     (1, 2),  # Sản phẩm có id = 1 với số lượng là 2
#     (3, 1),  # Sản phẩm có id = 3 với số lượng là 1
#     # Thêm các sản phẩm khác tương tự ở đây nếu cần
# ]

# for product_id, quantity in products_to_add:
#     price = get_product_price(product_id)
#     if price is not None:
#         cursor.execute('''
#             INSERT INTO CartItems (cart_id, product_id, quantity, price)
#             VALUES (?, ?, ?, ?)
#         ''', (cart_id, product_id, quantity, quantity * price))
#     else:
#         print(f"