from flask import Flask, render_template,Blueprint,flash,request,redirect,url_for
from werkzeug.security import generate_password_hash
from . import db
from .models import User
from flask_login import login_required

views = Blueprint('views',__name__)

@views.route("/")
@login_required
def index():
    return render_template("welcome.html")

@views.route('/forgot',methods=['POST','GET'])
def forgot_password():
    if request.method == 'POST':
        matric_no = request.form.get("matric_no")
        phone_number = request.form.get("phone_number")
        new_password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if matric_no exists in the database
        user = User.query.filter_by(matric_no=matric_no).first()
        if not user:
            flash('Matric number not found. Please enter a valid matric number.', 'error')
            return redirect(url_for('views.forgot_password'))

        # Verify that the phone number matches the user's phone number
        if user.phone_number != phone_number:
            flash('Phone number does not match the registered Matric Number.', 'error')
            return redirect(url_for('views.forgot_password'))

        # Check if the new password matches the confirm password
        if new_password != confirm_password:
            flash('Passwords do not match. Please enter the same password in both fields.', 'error')
            return redirect(url_for('views.forgot_password'))

        # Update the user's password with the new password
        user.password = generate_password_hash(new_password)
        db.session.commit()

        flash('Password reset successfully. You can now log in with your new password.', 'success')
        return redirect(url_for("auth.login"))

    
    return render_template('forgotpass.html')