import bcrypt as bcrypt
from flask import Flask, render_template, request, session, url_for
from werkzeug.security import check_password_hash
import flask_pymongo
from werkzeug.utils import redirect

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://hicham2:kunto@kuntosports.kzgbv.mongodb.net/test'
mongo = flask_pymongo(app)


@app.route('/', methods=["get", "post"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        name = request.form["name"]
        mail = request.form["mail"]
        city = request.form["city"]
        password = request.form["password"]
        print("username: ", username, "name: ", name, "mail: ", mail, "city", city, "password", password)

        admin_password = 'pbkdf2:sha256' \
                         ':150000$R1iudXL3$d2132c4b9f4e00ec4f5cb424790a3d3f9869d5337edc752a896cf12811458698 '

        user = mongo.db.Users
        user.insert_one([
            {"ID": int(name), "Password": password, "Email": mail, "Name": name, "User_name": username,
             "City": city}])

        if username == "admin" and check_password_hash(admin_password, password):

            return "Acces Autorisé"
        else:
            return "Acces Refusée"
    else:
        return render_template("index.html")


@app.route('/post-login', methods=["get", "post"])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user[
            'password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return 'Invalid username or password'

    return render_template("logIn.html")


@app.route('/profile', methods=["get", "post"])
def profile():
    twitter = mongo.db.Twitter
    tweet_text = request.form['Comment']
    tweet = twitter.find_one({'ID': request.form['ID']})
    twitter.insert_one([
            {"ID": request.form['ID'], "User_id": int(request.form["name"]), "Author": request.form["username"],"Text": tweet_text,"Media":"Nothing","Like":0,"Hashtag":"#creed"}
       ])
    return render_template("profile.html")

# if __name__ == '__main__':
#    app.run(debug=True)
