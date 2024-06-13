from flask import Flask, render_template,Blueprint,flash,request,redirect,url_for
from werkzeug.security import generate_password_hash
from . import db
from .models import User,Upload
from flask_login import login_required,current_user
import cloudinary.uploader
from sqlalchemy import or_

views = Blueprint('views',__name__)

@views.route("/")
@login_required
def index():
    return render_template("welcome.html")

@views.route('/messages')
@login_required
def messages():
    return render_template('messagelist.html')


@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        file = request.files['file']

        # Upload the file to Cloudinary
        if file:
            result = cloudinary.uploader.upload(file)
            file_url = result.get('secure_url')

            # Save the upload to the database
            new_upload = Upload(
                title=title,
                description=description,
                category=category,
                file_url=file_url,  # Store the file URL
                user_id=current_user.id
            )
            db.session.add(new_upload)
            db.session.commit()
            flash('Your item has been uploaded successfully!', 'success')
        else:
            flash('File upload failed. Please try again.', 'error')

        return redirect(url_for('views.upload'))

    return render_template('upload.html')

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



@views.route('/exchange', methods=['GET'])
@login_required
def exchange():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            or_(Upload.title.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%"))
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).all()

    return render_template('exchange.html', uploads=uploads, search_query=search_query)



@views.route('/books', methods=['GET'])
@login_required
def books():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information and filter by category
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%")
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "book"
        ).all()

    return render_template('books.html', uploads=uploads, search_query=search_query)

@views.route('/past-questions', methods=['GET'])
@login_required
def past_questions():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information and filter by category
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%")
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "past question"
        ).all()

    return render_template('past_questions.html', uploads=uploads, search_query=search_query)

@views.route('/news', methods=['GET'])
def news():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information and filter by category
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "news",
            or_(Upload.title.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%"))
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "news"
        ).all()

    return render_template('news.html', uploads=uploads, search_query=search_query)

