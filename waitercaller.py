from bitlyhelper import shorten_url
from flask import Flask 
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import LoginManager 
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from sqlalchemy.exc import IntegrityError
from config import DevConfig
from mockdbhelper import MockDBHelper as DBHelper 
from user import User 
from passwordhelper import PasswordHelper


DB = DBHelper()
PH = PasswordHelper()

base_url = "http://127.0.0.1:5000/"
app = Flask(__name__) 
app.config.from_object(DevConfig)
login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ModelUser(db.Model):
    __tablename__ = "user_table"
    email = db.Column(db.Text(), primary_key=True)
    salt = db.Column(db.Text(), nullable=False)
    hashedPassword = db.Column(db.Text(), nullable=False)

    def __init__(self, email, salt, hashedPassword):
        self.email = email
        self.salt  = salt 
        self.hashedPassword = hashedPassword

    def __repr__(self):
        return "\n<User email: {}\nsalt: {}\nhashedPassword: {}\n".format(self.email, self.salt, self.hashedPassword);

class Table(db.Model):
    __tablename__ = "tablemodel"
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Text(), nullable=False, unique=True)
    email = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text())

    def __init__(self, number, email, url):
        self.number = number 
        self.email = email 
        self.url = url

    def __repr__(self):
        return "\n<Table number: {}\n email: {}\n url: {}\n>".format(number, email, url)


@app.route("/")
def home():
    db.create_all()
    return render_template("home.html")

# @app.route("/account")
# @login_required 
# def account():
#     return "You are logged in"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    #user_password = DB.get_user(email)
    #stored_user = DB.get_user(email)
    stored_user = ModelUser.query.filter_by(email=email).first()
    if stored_user and PH.validate_password(password, stored_user.salt, stored_user.hashedPassword):
    #if user_password and user_password == password:
        user = User(email)
        login_user(user)
        return redirect(url_for("account"))
    return home()

@app.route("/logout")
def logout():
    logout_user() 
    return redirect(url_for("home"))

@login_manager.user_loader
def load_user(user_id):
    #user_password = DB.get_user(user_id)
    user_password = ModelUser.query.filter_by(email=user_id).first()
    if user_password:
        return User(user_id)

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    pw1 = request.form.get("password")
    pw2 = request.form.get("password2")
    if not pw1 == pw2:
        return redirect(url_for("home"))
    if ModelUser.query.filter_by(email=email).first():
        return redirect(url_for("home"))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1+salt)
    #DB.add_user(email, salt, hashed)
    user = ModelUser(email, salt, hashed)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/dashboard")
@login_required 
def dashboard():
    return render_template("dashboard.html")

@app.route("/account")
@login_required 
def account():
    tables = Table.query.filter_by(email=current_user.get_id()).all()
    return render_template("account.html", tables=tables)

@app.route("/account/createtable", methods=["POST"])
@login_required 
def account_createtable():
    tablenumber = request.form.get("tablenumber")
    #add table to database
    table = Table(tablenumber, current_user.get_id(), "")
    db.session.add(table)
    try:
        db.session.commit()
    except IntegrityError as ex:
        print("\n\nwe had an Exception here\n\n", ex)
    else:
        new_url = base_url + "newrequest/" + str(table.id)
        new_url = shorten_url(new_url)
        table = Table.query.filter_by(number=tablenumber)
        table.update({'url':new_url})
        db.session.commit();
    #update table in database
    return redirect(url_for('account'))

@app.route("/account/deletetable")
@login_required 
def account_deletable():
    tableid = request.args.get("tableid")
    table = Table.query.filter_by(id=tableid).first()
    db.session.delete(table)
    db.session.commit()
    return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def new_request(tid):
    #add request id and datetime.datetime.now() to db
    return "your request has been logged and a waiter will be with you shortly"

if __name__ == "__main__":
    app.run()
