from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash("Login successful!", category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.index')) 
        else:
            flash("Invalid username or password.", category='error')
    return render_template("login.html", user=current_user)    

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm_password = request.form.get('confirm_password')
        groqApi = request.form.get('groqApi')
        zapApi = request.form.get('zapApi')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category='error')
            return redirect(url_for('auth.register'))
        elif len(username) < 3:
            flash("Username must be at least 3 characters long.", category='error')
            return redirect(url_for('auth.register'))
        elif len(password) < 6:
            flash("Password must be at least 6 characters long.", category='error')
            return redirect(url_for('auth.register'))
        elif password != confirm_password:
            flash("Passwords do not match.", category='error')
            return redirect(url_for('auth.register')) 
        else:
            new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), email=email, groqApi=groqApi, zapApi=zapApi)

            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful. Please log in.", category='success')
            return redirect(url_for('auth.login'))
    return render_template("register.html", user=current_user)