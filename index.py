from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import hashlib
from functools import wraps
#Kullanici Giriş Decorater
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Bu Sayfayı Görüntülemek için Lütfen Giriş Yapınız","danger")
            return redirect(url_for("login"))
    return decorated_function


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


@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article) 
    else:
        return redirect(url_for("index"))


#Kullanici Giriş Form
class LoginForm(Form):
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min=5,max=35)])
    password = PasswordField("Şifre",validators=[validators.DataRequired(message="Lütfen Parola Belirleyin.")])

@app.route("/login",methods=["GET","POST"])
def login():
    if 'logged_in' in session:
        return redirect(url_for("index"))
    else: 
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
                session["logged_in"] = True
                session["username"] = username
                flash("Giriş Başarıyla Yapıldı.","success")
                return redirect(url_for("index"))
            else:
                flash("Kullanıcı Bulunamadı.","danger")
                return redirect(url_for("login"))
            cursor.close()
        else: 
            return render_template("login.html",form = form) 
    

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

@app.route("/register",methods=["GET","POST"])
def register():
    if 'logged_in' in session:
        return redirect(url_for("index"))
    else: 
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
    

@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/admin")
@app.route("/admin/articles")
@login_required
def admin():
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where author = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0 :
        articles = cursor.fetchall()
        return render_template("admin.html",articles = articles)
    else:
        return render_template("admin.html")


#Makale Kayıt Form
class ArticleForm(Form):
    title = StringField("Yazı Başlığı",validators=[validators.Length(min=5,max=100,message="En az 5 En fazla 100 Karakter Girin.")])
    content = TextAreaField("Yazı İçeriği",validators=[validators.Length(min=15,message="Çok Kısa")])

@app.route("/admin/article/add",methods=["GET","POST"])
@login_required
def addarticle():
    if 'logged_in' in session:
        form = ArticleForm(request.form)
        if request.method == "POST" and form.validate():
            title = form.title.data
            content = form.content.data
            cursor = mysql.connection.cursor()
            sorgu = "Insert  into articles(title,content,author) values(%s,%s,%s)"
            cursor.execute(sorgu,(title,content,session["username"]))
            mysql.connection.commit()
            cursor.close()
            flash('Başarıyla Makale Eklediniz.',"success")
            return redirect(url_for("admin"))
        else: 
            return render_template("addarticle.html",form=form)
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)