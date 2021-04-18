from os import stat
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps

app = Flask(__name__)
#connect db
#mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false
app.secret_key="secretkey"

app.config['MONGO_URI'] = 'mongodb://localhost:27017/e_commerce'

mongo = PyMongo(app)
@app.route('/')
def index():
    return "Ecommerce site"
#add cart
@app.route('/cart/create', methods=['POST'])
def create_cart():         
    _json = request.json
    name = _json['cart_name']
    if request.method == 'POST':
        mongo.db.shopping_cart.insert({'cart_name':name})
        resp = jsonify("Cart Added succesfully")
        resp.status_code = 200
        
        return resp
    else:
        return "error in creating cart"

 # show all cart
              
@app.route('/cart',methods=['GET'])
def cart():
    if request.method == 'GET':
     details = mongo.db.shopping_cart.find()
     resp = dumps(details) 
     
    return resp

#get all item in a cart
@app.route('/cart/<uid>/item',methods=['GET'])
def items(uid):
    if uid and request.method == 'GET':
     details = mongo.db.shopping_cart.find({'cart_id':uid})
     resp = dumps(details) 
    
    return resp

#add item in cart
@app.route('/cart/<uid>/item/add',methods=['POST'])
def add_item(uid):
    _json=request.json
    item_price = _json['item_price']
    item_name = _json['item_name']
    
    if request.method == 'POST':
        mongo.db.shopping_cart.insert({"cart_id":uid,'item_name':item_name,'item_price':item_price})
        resp = jsonify("Item Added succesfully")
        resp.status_code = 200
        
        return resp
    else:
        return not_found()  

#delete item from cart
@app.route('/item/<item_id>/delete',methods=['DELETE'])
def delete_item(item_id):
    if request.method == 'DELETE':
     mongo.db.shopping_cart.delete_one({'_id':item_id})
     resp = jsonify("details related to this id is deleted")
     resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error = None):
    message={
        'status':400,
        'message':'Not found' + request.url 
           }
    resp=jsonify(message)
    resp.status_code = 404
    return resp
                      
    

if __name__ == '__main__':
    app.run(debug=True)
