

class Registration(Resource):
    def post(self):
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        newuser = User(username=username,password=password)
        db.session.add(newuser)
        db.session.commit()
        return jsonify({"New User: Added Successfully"})
        if not username or not password:
            return jsonify({"Message":"Missing username and password"})
        if User.query.filter_by(username=username).first():
            return jsonify({"Message":"User already registered"})
       

api.add_resource(Registration, "/register")