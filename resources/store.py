from flask_restful import Resource,reqparse
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store: 
            return store.json()
        else: 
            return {"message":"No matching store found"},404

    def post(self,name):
        store = StoreModel.find_by_name(name)
        if store: 
            return {"message", "Store is already there"},400
        else:
            s= StoreModel(name)
            try:
                s.save_to_db()
            except:
                return {"message":"Internal Server Error"},500
            return s.json(),201


    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store: 
            return store.delete()
        else: 
            return {"message":"No matching store found"},404


class StoreList(Resource):
    def get(self):
        return list(map(lambda x :x.json(),StoreModel.query.all()))

