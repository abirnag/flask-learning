from db import db



class ItemModel(db.Model):
    __tablename__='ITEMS'
    name = db.Column(db.String(80), primary_key=True)
    price= db.Column(db.Float(precision=2))
    store_id=db.Column(db.Integer,db.ForeignKey('stores.id'))
    store =db.relationship('StoreModel')
    def __init__(self,**args):
        self.name=args['name']
        self.price =args['price']
        self.store_id=args['store_id']
    @classmethod
    def saveItem(cls,data):
        db.session.add(data)
        db.session.commit()
        return True
    @classmethod
    def findItemByName(cls,name):
        return cls.query.filter_by(name=name).first()
    @classmethod
    def update(cls, data):
        item = cls.findItemByName(data.name)
        if item:
            item.price=data.price
        else:
            item= ItemModel(name=data.name, price=data.price)
        db.session.add(item)
        db.session.commit()


        

    @classmethod
    def remove(cls,data):
        item = cls.findItemByName(data.name)
        if item:
            db.session.delete(item)
            db.session.commit()
    
    @classmethod
    def findAll(cls):
        return list(map(lambda  x :x.json(), cls.query.all()))

    def json(self):
        return {'name':self.name,'price':self.price}

