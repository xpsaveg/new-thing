import requests
from flask import Flask, render_template, request, url_for, session
from werkzeug.utils import redirect
from flask import Flask,render_template,request
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
# data base
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.app_context():
    class User(UserMixin, db.Model):
        __tablename__ = 'User'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        city = db.Column(db.String(1000))


    class weather(UserMixin, db.Model):
        __tablename__ = 'weather'
        id = db.Column(db.Integer, primary_key=True)
        city = db.Column(db.String(100), unique=True)
        temp = db.Column(db.Integer)

    db.session.commit()
    db.create_all()

class MyModelView(ModelView):
    def is_accessible(self):

            return True

admin = Admin(app)
admin.add_view(MyModelView(User, db.session))

@app.route("/")
def start():
    return render_template("index.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        user=User.query.all()
        for i in user:
            if i.name==name and i.password==password:

                return redirect(f"/weather?u={i.city}")
        return redirect("/register")
    return render_template("login.html")
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form.get("name")
        password = request.form.get("password")
        city = request.form.get("city")
        new=User(
            name=name,
            password=password,
            city=city,
        )
        db.session.add(new)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/weather")
def w():
    cities = ["Cairo","New York"]
    u= request.args.get("u")
    END_POINT = "https://api.openweathermap.org/data/2.5/weather"
    API = "868c5469fc5add3122d3e7e8313c8f3e"
    target=[]

    index = cities.index(u, 0, len(cities))
    new_list = [cities[index]] + cities[:index] + cities[index+1:]
    print(new_list)
    for c in new_list:

            params = {
                "q": c,
                "appid": API
            }

            response = requests.get(url=END_POINT, params=params)
            weather_data = response.json()
            t = int(weather_data["main"]["temp"]) - 273
            target.append(t)


    print(target)
    return render_template("weather.html",target=target)

# Handle the "Change City" form submission
def update_city_in_database(city):
    pass


@app.route('/new',methods=["GET","POST"])
def new():

    return render_template("new.html")

if __name__==("__main__"):

    app.run(debug=True)


































































