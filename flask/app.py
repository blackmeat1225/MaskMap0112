from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#建立一個模擬資料庫
products = [
                {
                    "id": 1,
                    "name": "原子筆（藍）",
                    "price": 15,
                    "qty": 120
                },
                {
                    "id": 2,
                    "name": "自動鉛筆 0.5mm",
                    "price": 45,
                    "qty": 80
                },
                {
                    "id": 3,
                    "name": "橡皮擦",
                    "price": 10,
                    "qty": 200
                },
                {
                    "id": 4,
                    "name": "A4 筆記本",
                    "price": 60,
                    "qty": 50
                }
            ]

#用id找產品 找不到就回傳None
def find_product(pid: int):
    for p in products:
        if p['id'] == pid:
            return p
    return None

#產品建檔
@app.route('/add_product', methods=['POST'])
def add_product():
    #從前端接收資料
    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except Exception:
        return jsonify({"error":"請傳遞正確的JOSN格式!"})

    name = data.get('name')
    price = data.get('price')
    qty = data.get('qty')

    #確認資料欄位是否正確
    if not name or not price or not qty:
        return jsonify({"error":"請提供商品名稱或價格或數量!"})
    
    #產品名稱必須為字串
    if not isinstance(name, str):
        return jsonify({"error":"產品名稱必須為字串!"})
    
    #價格必須為數字
    if not isinstance(price, (int, float)):
        return jsonify({"error":"價格必須為數字!"})
    
    #驗證產品名稱是否已經存在
    for p in products:
        if p['name'] == name:
            return jsonify({"error":"產品名稱已存在, 請重新命名!"})

    #將資料寫入products
    porduct = {
        "id": len(products) + 1,
        "name": name,
        "price": price,
        "qty": qty
    }
    products.append(porduct)


    return jsonify({"message":"產品新增成功", "product": porduct, "products": products})

#取得所以產品資料
@app.route('/products', methods=["GET"])
def get_all_products():
    return jsonify({"products":products})

#更新產品
@app.route('/products/<int:pid>', methods=['PUT'])
def update_product(pid):
    #從前端接收資料
    try:
        data = request.get_json()
        if data is None:
            raise ValueError
    except Exception:
        return jsonify({"error":"請傳遞正確的JOSN格式!"})
    
    #至少更新品名或價格
    name = data.get('name', None)
    price = data.get('price', None)
    if name is None and price is None:
        return jsonify({"error":"至少提供name 或 price 執行更新!"})

    if name is not None and not isinstance(name, str):
        return jsonify({"error":"品名一定要是文字格式!"})
    if price is not None and not isinstance(price, (int, float)):
        return jsonify({"error":"價格一定要是數字格式!"})

    #尋找要更新的產品
    target = find_product(pid)
    if target is None:
        return jsonify({"error":"找不到此筆產品!"})
    # else:
    #     return jsonify({"prdouct":target})

    #避免更新到重複的品名
    if name is not None:
        for p in products:
            if['id'] != pid and p['name'] == name:
                return jsonify({"error":"品名存在不可以重複!"})

    #執行更新
    if name is not None:
        target["name"] = name

    if price is not None:
        target["pric"] = price

    return jsonify({"message":"更新成功", "product":target})

#刪除產品
@app.route('/products/<int:pid>', methods=['DELETE'])
def deletet_product(pid):
    target = find_product(pid)
    if target is None:
        return jsonify({"error":"找不到此產品"})

    products.remove(target)

    return jsonify({"message":"刪除成功", "deleted":target, "count":len(products)})

@app.route('/home01')
def home01():
    return 'hello home01'

if __name__ == '__main__':
    app.run(debug=True)