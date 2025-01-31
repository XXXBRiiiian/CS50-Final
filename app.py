import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template,request,session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms.validators import DataRequired,Regexp,DataRequired, Length, EqualTo, NumberRange
from wtforms.fields import (StringField, PasswordField, DateField, BooleanField,DateTimeField,TimeField,
                            SelectField, SelectMultipleField, TextAreaField,FloatField,HiddenField,
                            RadioField, IntegerField, DecimalField, SubmitField,
                            IntegerRangeField)


app = Flask(__name__)
db = SQL("sqlite:///logbook.db")
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Session(app)
CSRFProtect(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show profiles of pilot"""

    user_data = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    return render_template("index.html", user_data=user_data)



@app.route("/register1", methods=["GET", "POST"])
def register():
    """Register user"""
    print("Form submitted")
    form = Userform()
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            print(form.username.data, form.password.data, form.hours.data, form.minutes.data, form.position.data)
            hash = generate_password_hash(password, method='scrypt', salt_length=16)
            try:
                db.execute(
                "INSERT INTO users (username, hash , hours ,minutes ,position) VALUES(?, ?, ?, ?, ?)", form.username.data, hash, form.hours.data, form.minutes.data,form.position.data
                )
            except (KeyError, ValueError) as e:
                print(f"Data parsing error: {e}")
                return apology("Duplicated User", 400)

            flash("Registered!")
            return redirect("/")
        else:
            print(form.errors)
    return render_template("register1.html",form=form)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    form = LoginForm()
    if form.validate_on_submit():
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", form.username.data
        )
        if len(rows) != 1:
             flash("Register first!")
             return redirect("/login")
        elif not check_password_hash(
            rows[0]["hash"], form.password.data):
            flash("Invalid password")
            return redirect("/login")
        session["user_id"] = rows[0]["id"]
        flash("Logged in!")
        return redirect("/")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    flash("Logged out!")
    # Redirect user to login form
    return redirect("/")


class RegisterForm(FlaskForm):


    date = DateField('Flight Date', format='%Y-%m-%d')

    model = SelectField('Model', choices=[
        ('319', 'A-319'),
        ('320', 'A-320'),
        ('321', 'A-321')
    ])

    ident = StringField('A/C Ident', validators=[Length(min=5, max=8)])
    ap_from = StringField('From', validators=[Length(min=3, max=4)])
    ap_to = StringField('To', validators=[Length(min=3, max=4)])

    hours = IntegerField('Total Hours', validators=[NumberRange(min=0, max=20)])
    minutes = IntegerField('Total Minutes', validators=[NumberRange(min=0, max=59)])
    night = RadioField('Night Flight', choices=[('d', 'Day'), ('n', 'Night')],
                                  validators=[DataRequired()])
    land = IntegerField('Lands', validators=[NumberRange(min=0, max=8)])                           

    
    submit = SubmitField('Add')

class Userform(FlaskForm):


    username = StringField(label=u"Username", validators=[DataRequired(), Length(min=3, max=18)])

    password = PasswordField(label=u"Passwords", validators=[DataRequired(), Length(min=3, max=18)])
    repeat_password = PasswordField(label=u"Confirm Passwords", validators=[DataRequired(),EqualTo("password", u"Didn't mach")])
    position = RadioField('Captain', choices=[('Captain', 'Captain'), ('First Officer', 'Copilot')],
                                  validators=[DataRequired()])
    hours = IntegerField('Current Hours', validators=[NumberRange(min=0, max=99999)])
    minutes = IntegerField('Current Minutes', validators=[NumberRange(min=0, max=59)])

    submit = SubmitField('Submit')                         


@app.route('/add1', methods=('GET', 'POST'))
def add1():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.night == "n":
            night_hours = form.hours
            night_minutes = form.minutes
        else:
            night_hours = 0
            night_minutes = 0

        db.execute(
        "INSERT INTO history (user_id, date, model, ident, ap_from,ap_to,hours,minutes,night_hours,night_minutes,land) VALUES(?, ?, ?, ?,?,?,?,?,?,?,?)", 
        session["user_id"], form.date.data, form.model.data, form.ident.data, form.ap_from.data, form.ap_to.data, form.hours.data, form.minutes.data, night_hours, night_minutes, form.land.data)
        current_hours = db.execute("SELECT hours FROM users WHERE id = ?",
                        session["user_id"])[0]['hours']
        current_minutes = db.execute("SELECT minutes FROM users WHERE id = ?",
                        session["user_id"])[0]['minutes']
        add_hours = int(form.hours.data)
        add_minutes= int(form.minutes.data)

        current_hours += add_hours
        current_minutes += add_minutes
        if current_minutes >= 60:
            current_minutes -= 60
            current_hours += 1
        db.execute(
                    "UPDATE users SET hours = ?,minutes = ? WHERE id = ?", current_hours,current_minutes, session["user_id"])
        flash('Add successfully！')

        return render_template('add1.html', form=form)
        
    return render_template('add1.html', form=form)

@app.route("/history")
@login_required
def history():
    """Show history of flights"""
    data = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total = len(data)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_data = data[start:end]
    return render_template("history.html", data=paginated_data, page=page, total=total, per_page=per_page)
    