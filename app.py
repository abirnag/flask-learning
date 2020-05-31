from flask import Flask
from flask_restful import Api 
from flask_jwt import JWT
from resources.user import UserRegister
from security import authenticate,identity
from resources.item import Item, ItemList


app = Flask(__name__)
app.secret_key="jsonwebtokensecret"
api = Api(app)
jwt = JWT(app,authenticate,identity)  #/auth



api.add_resource(Item,'/items/<string:name>')
api.add_resource(UserRegister,'/register')
api.add_resource(ItemList,'/items')
app.run(port=5000,debug=True)  