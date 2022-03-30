from flask import Flask, render_template, request, flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost/loginapp'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'secret string'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"
login_manager.init_app(app)

class People(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name,password):
        self.name = name
        self.password = password
    
    def get_id(self):
        return (self.id)

@login_manager.user_loader
def load_user(user_id):
    return People.query.get(int(user_id))
    
@app.route('/')
def loggedOut():
    return render_template('index.html')

@app.route('/welcome')
@ login_required
def welcome():
    if(current_user.is_authenticated):
        return render_template('welcome.html', name=current_user.name)
    return redirect(url_for('login_page'))



@ app.route('/login_page')
def login_page():
    if(current_user.is_authenticated):
        return redirect(url_for('welcome'))
    return render_template("login.html")

@ app.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):

        u = People.query.filter_by(name=request.form.get('name')).first()
        print(u)
        if(u == None):
            return redirect(url_for('login_page'),error="Invalid username or password")
        if(u.password == request.form.get('password')):
            login_user(u)
            flash("LOGIN SUCCESSFULL", "success")
            return redirect(url_for('welcome'))
        else:
            flash("LOGIN FAILED !! INCORRECT USERNAME OR PASSWORD", "danger")
            return redirect(url_for('login_page'))
    return redirect(url_for('login_page'))



@ app.route('/logout')
@ login_required
def logout():
    logout_user()
    flash("LOGOUT SUCCESSFULLY", "success")
    return redirect(url_for('loggedOut'))

@app.route("/addperson")
def addperson():
    return render_template("register.html")


@app.route("/personadd", methods=['POST'])
def personadd():
    name = request.form["name"]
    password = request.form["password"]
    entry = People(name,password)
    db.session.add(entry)
    db.session.commit()

    return redirect(url_for('login_page'))


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)