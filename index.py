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
@app.route("/articles")
@app.route("/article")
def index():
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles order by created_at desc"
    result = cursor.execute(sorgu)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("index.html",articles = articles)
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/article/<string:url>")
def article(url):
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles where url = %s"
    result = cursor.execute(sorgu,(url,))
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
                #data = cursor.fetchone()
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
@app.route("/admin/article")
@login_required
def admin():
    cursor = mysql.connection.cursor()
    sorgu = "select * from articles order by created_at desc"
    result = cursor.execute(sorgu)
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
            sorgu = "Insert  into articles(title,content,author,url) values(%s,%s,%s,%s)"
            cursor.execute(sorgu,(title,content,session["username"],self_url(title)))
            mysql.connection.commit()
            cursor.close()
            flash('Başarıyla Makale Eklediniz.',"success")
            return redirect(url_for("admin"))
        else: 
            return render_template("addarticle.html",form=form)
    else:
        return redirect(url_for("index"))


@app.route("/admin/article/<string:id>/edit",methods=["GET","POST"])
@login_required
def edit_article(id):
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        sorgu = "update articles set title=%s, content=%s, author=%s, url=%s where id = %s"
        cursor.execute(sorgu,(title,content,session["username"],self_url(title),id))
        mysql.connection.commit()
        cursor.close()
        flash('Başarıyla Makale Güncellendi.',"success")
        return redirect(url_for("admin"))
    else:  
        cursor = mysql.connection.cursor()
        sorgu = "select * from articles where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result > 0:
            article = cursor.fetchone()
            form = ArticleForm()
            form.title.data = article["title"]
            form.content.data = article["content"]
            return render_template("editarticle.html",form=form) 
        else:
            return redirect(url_for("index"))


@app.route("/admin/article/<string:id>/delete",methods=["GET","POST"])
@login_required
def delete_article(id):
    form = ArticleForm(request.form)
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        sorgu = "delete from articles where id = %s"
        cursor.execute(sorgu,(id,))
        mysql.connection.commit()
        cursor.close()
        flash('Başarıyla Makale Silindi.',"success")
        return redirect(url_for("admin"))
    else:  
        return render_template("deletearticle.html",form=form) 


def self_url(string):
    string = string.lower()
    string = string.replace(' ', '_')
    string = string.replace('?', '_')
    string = string.replace('%', '_')
    string = string.replace('&', '_')
    string = string.replace('.', '_')
    string = string.replace(',', '_')
    string = string.replace('!', '_')
    string = string.replace('ı', 'i')
    string = string.replace('ğ', 'g')
    string = string.replace('Ğ', 'g')
    string = string.replace('ş', 's')
    string = string.replace('Ş', 's')
    string = string.replace('Ö', 'o')
    string = string.replace('ö', 'o')
    string = string.replace('Ç', 'c')
    string = string.replace('ç', 'c')
    string = string.replace('Ü', 'u')
    string = string.replace('ü', 'u')
    return string

if __name__ == "__main__":
    app.run(debug=True)