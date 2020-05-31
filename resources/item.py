from flask_restful import Resource,Api, reqparse
from flask_jwt import JWT, jwt_required
from .user import UserRegister
from security import authenticate,identity
from models.item import ItemModel





class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float, required=True, help='Field should contain value')
    
    @jwt_required()
    def get(self, name):
        filteredItem = ItemModel.findItemByName(name)
        if filteredItem is None:
            return {"error":"Item is not found"},404
        else : 
            return filteredItem.json()
    def post(self,name):
        data= Item.parser.parse_args() 
        filteredItem = ItemModel.findItemByName(name)
        if filteredItem==None:
            item =ItemModel(name=name, price= data['price'])
            ItemModel.saveItem(item)
            return item.json(),201
        else: 
            return {"error":"item is already exists"},400
        
    def put(self, name):
        data= Item.parser.parse_args()       
        filteredItem = ItemModel.findItemByName(name)
        if filteredItem==None:
            item =ItemModel(name=name, price= data['price'])
            ItemModel.saveItem(item)
            return {"message":"item is created"},201
        else: 
            item =ItemModel(name=name, price= data['price'])
            item=ItemModel.update(item)
            return {"message":"item is updated"}
    def delete(self,name):
        filteredItem = ItemModel.findItemByName(name)
        if filteredItem:
            ItemModel.remove(filteredItem)            
        else:
            return {"error":"item is already exists"},400
        


class ItemList(Resource):
    def get(self):
        return ItemModel.findAll()
