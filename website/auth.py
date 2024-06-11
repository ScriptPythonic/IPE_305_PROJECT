from flask import Flask, render_template, redirect, Blueprint, request, url_for, flash
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .email import send_welcome_email

auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        # Get form data
        matric_no = request.form["matric_no"]
        full_name = request.form["full_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        password = request.form["password"]

        # Validate form data
        if not matric_no or not full_name or not phone_number or not email or not password:
            flash('Please fill in all the fields.', 'error')
            return redirect(url_for('auth.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='scrypt')

        # Create new user
        new_user = User(matric_no=matric_no, full_name=full_name, phone_number=phone_number, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Send email notification
        send_welcome_email(full_name, email)

        flash('Account created successfully!', 'success')
        return redirect(url_for("auth.login"))

    return render_template('register.html')

@auth.route("/login", methods=['GET', "POST"])
def login():
    if request.method == 'POST':
        matric_no = request.form["matric_no"]
        password = request.form["password"]

        # Query user
        user = User.query.filter_by(matric_no=matric_no).first()

        if user and check_password_hash(user.password, password):
            flash('Login successful!', 'success')
            return render_template("welcome.html", name=user.full_name)
        else:
            flash('Invalid credentials. Please try again.', 'error')
            return redirect(url_for("auth.login"))

    return render_template('login.html')
