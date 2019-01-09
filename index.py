from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import hashlib
#Kullanici Kayıt Form
class RegisterForm(Form):
    name = StringField("İsim Soyisim",validators=[validators.Length(min=4,max=25)])
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=35)])
    email = StringField("Email Adresiniz",validators=[validators.Email(message="Email Adresi Hatalı")])
    password = PasswordField("Şifre",validators=[
        validators.DataRequired(message="Lütfen Parola Belirleyin."),
        validators.EqualTo(fieldname="confirm",message="Şifreler Eşleşmiyor")    
    ])
    confirm = PasswordField("Şifre Tekrar")

class LoginForm(Form):
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=35)])
    password = PasswordField("Şifre",validators=[validators.DataRequired(message="Lütfen Parola Belirleyin.")])

app = Flask(__name__)
app.secret_key = 'flask_blog'
app.config["MYSQL_HOST"]        =   "localhost"
app.config["MYSQL_USER"]        =   "root"
app.config["MYSQL_PASSWORD"]    =   ""
app.config["MYSQL_DB"]          =   "flask"
app.config["MYSQL_CURSORCLASS"] =   "DictCursor"
mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hakkımda")
def hakkımda():
    return render_template("hakkımda.html")


@app.route("/yazi/<string:id>")
def yazi(id):
    #return "ID " + id
    password = '1234'
    h = hashlib.md5(password.encode())
    return h.hexdigest()

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        #password_entered = sha256_crypt.encrypt(form.password.data)
        password = hashlib.md5(form.password.data.encode()).hexdigest() 
        cursor = mysql.connection.cursor()
        sorgu = "select * from users where username = %s and password = %s"
        result = cursor.execute(sorgu,(username,password))
        if result > 0:
            data = cursor.fetchone()
            flash("Giriş Başarıyla Yapıldı.","success")
            return redirect(url_for("index"))
        else:
            flash("Kullanıcı Bulunamadı.","danger")
            return redirect(url_for("login"))
        cursor.close()
    else: 
        return render_template("login.html",form = form) 


@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = hashlib.md5(form.password.data.encode()).hexdigest() 
        #password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        sorgu = "Insert  into users(name,username,email,password) values(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,username,email,password))
        mysql.connection.commit()
        cursor.close()
        flash('Başarıyla Kayıt Oldunuz.',"success")
        return redirect(url_for("login"))
    else: 
        return render_template("register.html",form = form)
    


if __name__ == "__main__":
    app.run(debug=True)