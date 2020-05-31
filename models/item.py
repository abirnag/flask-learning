from db import Db


db = Db()

class ItemModel:
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
            return ItemModel(name=item[0], price = item[1])
        else:
            return None
    @classmethod
    def update(cls, data):
        update_query = "UPDATE ITEMS SET PRICE=? WHERE NAME=?"
        res = db.execute_and_commit(update_query,data.price,data.name)
        item = res.fetchone()
        db.connection_close()
        if item : 
            return ItemModel(name=item[0], price = item[1])
        else:
            return None
        

    @classmethod
    def remove(cls,data):
        db.execute_and_commit("DELETE FROM ITEMS WHERE NAME=?",data.name)
        db.connection_close()
    
    @classmethod
    def findAll(cls):
        res = db.execute_and_commit("SELECT * FROM ITEMS")
        result = list(map(lambda row: ItemModel(name=row[0],price=row[1]).json(),res))
        db.connection_close()
        return result

    def json(self):
        return {'name':self.name,'price':self.price}

