from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
      if check_password_hash(user.password, password):
        flash("Logged in successfully!")
        login_user(user, remember=True)
        return redirect(url_for('views.home'))
      else: 
        flash("Incorrect password", category="error")
    else:
      flash("Email doesn't exist", category="error")
  return render_template("login.html", user=None)


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    firstname = request.form.get("email")
    pass_1 = request.form.get("password1")
    pass_2 = request.form.get("password2")

    user = User.query.filter_by(email=email).first()

    if user:
      flash("Email already exist", category="error")
    elif len(email) < 4:
      flash("Invalid Email", category="error")
    elif len(firstname) < 2:
      flash("First Name must be greater than 1 character", category="error")
    elif pass_1 != pass_2:
      flash("Password don't match", category="error")
    elif len(pass_1) < 7:
      flash("Password must be at least 7 characters", category="error")
    else:
      new_user = User(email=email, password=generate_password_hash(pass_1, method="sha256"), first_name=firstname)
      db.session.add(new_user)
      db.session.commit()
      flash("Account created")
      login_user(new_user, remember=True)
      return redirect(url_for('views.home'))


  return render_template("sign-up.html", user=None)

