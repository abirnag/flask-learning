from db import db

class UserModel(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    def __init__(self,_id, username, password):
        self.id = _id
        self.username=username
        self.password=password
    
    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
        

    @classmethod
    def create_user(cls, data):
        user  =cls.query.filter_by(username=data['username']).first()
        if user:
            return False
        db.session.add(cls(None,data['username'], data['password']))
        db.session.commit()
        return True
