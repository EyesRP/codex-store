from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# قاعدة بيانات المنتجات
products_db = [
    {
        "id": 1, 
        "name": "نظام حماية متطور ضد الثغرات", 
        "category": "FiveM", 
        "price": 45, 
        "description": "حماية كاملة لسيرفرك مع لوحة تحكم وإدارة للباندات متطورة وتحديثات مستمرة ضد أحدث الثغرات."
    },
    {
        "id": 2, 
        "name": "بوت تذاكر ودعم فني متكامل", 
        "category": "Discord", 
        "price": 20, 
        "description": "بوت بايثون مخصص لإدارة التذاكر، الترحيب، وسجلات الحماية بدقة عالية مع لوحة تحكم سهلة."
    },
    {
        "id": 3, 
        "name": "نظام ميكانيكي وكراج (Cars & Tuning)", 
        "category": "FiveM", 
        "price": 30, 
        "description": "كراج تفاعلي مع نظام تعديل سيارات احترافي وخفيف على السيرفر وموافق لأحدث إصدارات FiveM."
    }
]

# قاعدة بيانات وهمية على السيرفر لتخزين الحسابات المسجلة
users_db = []

@app.route('/')
def home():
    return render_template('index.html', products=products_db, current_category=None)

@app.route('/category/<string:cat_name>')
def category_view(cat_name):
    filtered_products = [p for p in products_db if p['category'].lower() == cat_name.lower()]
    return render_template('index.html', products=filtered_products, current_category=cat_name)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products_db if p['id'] == product_id), None)
    if product is None:
        abort(404)
    return render_template('product.html', product=product)

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/payment')
def payment_page():
    return render_template('payment.html')

# API لإنشاء حساب جديد وحفظه في السيرفر
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    # التأكد من عدم وجود البريد مسبقاً
    existing_user = next((u for u in users_db if u['email'] == email), None)
    if existing_user:
        return jsonify({"success": False, "message": "البريد الإلكتروني مسجل مسبقاً!"})

    # حفظ المستخدم الجديد
    new_user = {
        "name": name,
        "email": email,
        "phone": phone,
        "password": password
    }
    users_db.append(new_user)
    return jsonify({"success": True, "message": "تم إنشاء الحساب بنجاح!", "user": {"name": name, "email": email}})

# API لتسجيل الدخول والتحقق من الحسابات المخزنة
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # البحث عن المستخدم في السيرفر
    user = next((u for u in users_db if u['email'] == email and u['password'] == password), None)
    if user:
        return jsonify({"success": True, "message": "تم تسجيل الدخول بنجاح!", "user": {"name": user['name'], "email": user['email']}})
    else:
        return jsonify({"success": False, "message": "البريد الإلكتروني أو كلمة المرور غير صحيحة!"})

if __name__ == '__main__':
    app.run(debug=True)