import sqlite3
from flask_restful import Resource,reqparse

class User:
    def __init__(self,_id, username, password):
        self.id = _id
        self.username=username
        self.password=password
    
    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor =connection.cursor()
        query = "select * from users where username=?"
        result = cursor.execute(query,(username,))
        row = result.fetchone()
        if row : 
            user=cls(*row)
        else:
            user=None
        connection.close()
        return user
    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor =connection.cursor()
        query = "select * from users where id=?"
        result = cursor.execute(query,(_id,))
        row = result.fetchone()
        if row : 
            user=cls(*row)
        else:
            user=None
        connection.close()
        return user

    @classmethod
    def create_user(cls, data):
        if cls.find_by_username(data['username']):
            return False
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        create_user_query = "INSERT INTO USERS VALUES(NULL,?,?)"
        cursor.execute(create_user_query,(data['username'], data['password'],))
        connection.commit()
        connection.close()
        return True



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",type=str,required=True,help='username should not be blank')
    parser.add_argument("password",type=str,required=True,help='password should not be blank')
    def post(self):
        data= UserRegister.parser.parse_args()
        if User.create_user(data):
            return {"message":"User is created"},201
        return {"message":"User[{}] is already exist.".format(data['username'])}

    
    
