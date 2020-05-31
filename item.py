from flask_restful import Resource,Api, reqparse 
from flask_jwt import JWT, jwt_required
from user import UserRegister
from security import authenticate,identity
from db import Db
db = Db()


items = []

class ItemEntity:
    def __init__(self,**args):
        self.name=args['name']
        self.price =args['price']
    @classmethod
    def saveItem(cls,data):
        create_item_query = "INSERT INTO ITEMS VALUES(?,?)"
        res= db.execute_and_commit(create_item_query,data.name, data.price)
        print(res)
        db.connection_close()
        return True
    @classmethod
    def findItemByName(cls,name):
        select_query = "SELECT * FROM ITEMS WHERE name=?"
        res=db.execute_and_commit(select_query,name)
        item = res.fetchone()
        db.connection_close()
        if item : 
            return ItemEntity(name=item[0], price = item[1])
        else:
            return None
    @classmethod
    def update(cls, data):
        update_query = "UPDATE ITEMS SET PRICE=? WHERE NAME=?"
        res = db.execute_and_commit(update_query,data.price,data.name)
        item = res.fetchone()
        db.connection_close()
        if item : 
            return ItemEntity(name=item[0], price = item[1])
        else:
            return None
        

    @classmethod
    def remove(cls,data):
        db.execute_and_commit("DELETE FROM ITEMS WHERE NAME=?",data.name)
        db.connection_close()
    
    @classmethod
    def findAll(cls):
        res = db.execute_and_commit("SELECT * FROM ITEMS")
        result = list(map(lambda row: ItemEntity(name=row[0],price=row[1]).convert_to_dict(),res))
        db.connection_close()
        return result

    def convert_to_dict(self):
        return {'name':self.name,'price':self.price}




class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float, required=True, help='Field should contain value')
    
    @jwt_required()
    def get(self, name):
        filteredItem = ItemEntity.findItemByName(name)
        if filteredItem is None:
            return {"error":"Item is not found"},404
        else : 
            return filteredItem.convert_to_dict()
    def post(self,name):
        data= Item.parser.parse_args() 
        filteredItem = ItemEntity.findItemByName(name)
        if filteredItem==None:
            item =ItemEntity(name=name, price= data['price'])
            ItemEntity.saveItem(item)
            return item.convert_to_dict(),201
        else: 
            return {"error":"item is already exists"},400
        
    def put(self, name):
        data= Item.parser.parse_args()       
        filteredItem = ItemEntity.findItemByName(name)
        if filteredItem==None:
            item =ItemEntity(name=name, price= data['price'])
            ItemEntity.saveItem(item)
            return {"message":"item is created"},201
        else: 
            item =ItemEntity(name=name, price= data['price'])
            item=ItemEntity.update(item)
            return {"message":"item is updated"}
    def delete(self,name):
        filteredItem = ItemEntity.findItemByName(name)
        if filteredItem:
            ItemEntity.remove(filteredItem)            
        else:
            return {"error":"item is already exists"},400
        


class ItemList(Resource):
    def get(self):
        return ItemEntity.findAll()
