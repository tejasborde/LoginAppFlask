from flask import Flask, render_template, request, flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] =  "postgresql://postgres:12345678@127.0.0.1:5432/loginapp"
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SERVER_MODE"] = True
app.secret_key = 'secret string'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'loggedOut'
login_manager.login_message_category = "info"
login_manager.init_app(app)


class Customer(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    gender=db.Column(db.String(80), nullable=False)

    def __init__(self, name,password,email,gender):
        self.name = name
        self.password = password
        self.email = email
        self.gender=gender
    
    def get_id(self):
        return (self.id)

@login_manager.user_loader
def load_user(id):
    return Customer.query.get(int(id))
    

@app.route('/')
def loggedOut():
    if(current_user.is_authenticated):
        return redirect(url_for('welcome'))
    return render_template("login.html")

@app.route('/welcome')
@ login_required
def welcome():
    if(current_user.is_authenticated):
        return render_template('welcome.html', name=current_user.name,user=current_user)
    return redirect(url_for('loggedOut'))





@ app.route('/login', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):

        u = Customer.query.filter_by(email=request.form.get('email')).first()
        if(u == None):
            flash("LOGIN FAILED !! INCORRECT USERNAME OR PASSWORD", "danger")
            return redirect(url_for('loggedOut'))
        if(u.password == request.form.get('password')):
            login_user(u)
            flash("LOGIN SUCCESSFULL", "success")
            return redirect(url_for('welcome'))
        else:
            flash("LOGIN FAILED !! INCORRECT USERNAME OR PASSWORD", "danger")
            return redirect(url_for('loggedOut'))
    return redirect(url_for('loggedOut'))



@ app.route('/logout')
@ login_required
def logout():
    logout_user()
    flash("LOGOUT SUCCESSFULLY", "success")
    return redirect(url_for('loggedOut'))

def validate_password(password):
    Capi_alpha = 0
    small_alpha = 0
    num = 0
    Spe_char = ['@', '#', '%', '&', '?']
    Spe_count = 0
    valid = False
    for i in password:
        if(ord(i) >= 65 and ord(i) <= 90):
            Capi_alpha += 1
        elif(i in Spe_char):
            Spe_count += 1
        elif(ord(i) >= 48 and ord(i) <= 57):
            num += 1
        elif(ord(i) >= 97 and ord(i) <= 122):
            small_alpha += 1
        else:
            pass

    if(len(password) >= 8):
        if(Capi_alpha > 0):
            if(small_alpha > 0):
                if(Spe_count > 0):
                    if(num > 0):
                        valid = True

    return valid

@app.route("/register", methods=['POST'])
def register():
    name = request.form["name"]
    password = request.form["password"]
    email = request.form["email"]
    gender = request.form["gender"]

    u = Customer.query.filter_by(email=email).all()
    if(len(u) != 0):
        flash("EMAIL ID IS ALREADY TAKEN!!!", "danger")
        return redirect(url_for('loggedOut'))
    if(validate_password(password)):
        entry = Customer(name,password,email,gender)
        db.session.add(entry)
        db.session.commit()
        flash("Registered Successfully","success")
        return redirect(url_for('loggedOut'))
    else:
        flash("PASSWORD CRITERIA MUST BE SATISFIED!!!", "danger")
        return redirect(url_for('loggedOut'))
    return redirect(url_for('loggedOut'))


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)