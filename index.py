from flask import Flask, render_template
app = Flask(__name__)




@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hakkımda")
def hakkımda():
    return render_template("hakkımda.html")


@app.route("/yazi/<string:id>")
def yazi(id):
    return "ID " + id





if __name__ == "__main__":
    app.run(debug=True)