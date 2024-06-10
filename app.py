from flask import Flask,request,jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource,Api
from flask_jwt_extended import JWTManager,jwt_required
 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"]="secret_key"
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(50),nullable=False)

@app.route("/register",methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    username = data["username"]
    password = data["password"]

    # Checks if the username or password is missing in the request data and returns an error message if true.
    if not username or not password:
        return jsonify({"Message": "Missing Username or Password "})

    # Checks if the provided username already exists in the database and returns an error message if true.
    if User.query.filter_by(username=username).first():
        return jsonify({"Message": "Username already exist"})

    # If both upper condition is false then add the new user in database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"Message": "User has been created successfully"})

@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first() #Retrieves the user from the database based on the provided username.

    print(user)
    if user and user.password==password: # If user enter same password as register password then give him JWT access token
        access_token = create_access_token(identity=user.id)
        return {"accesss_token":access_token}
    return {"Message":"Invalid Login Credentials"}


@app.route("/protected",methods=["GET"])
@jwt_required
def secure():
    current_user_id = get_jwt_identity() # get_jwt_identity() is a function provided by Flask-JWT-Extended that extracts the identity information from the JWT token.

    return {"Message":f'Hello user {current_user_id} you can now access the secured resources.'}

if __name__=="__main__":
    app.run(debug=True,port=6000)