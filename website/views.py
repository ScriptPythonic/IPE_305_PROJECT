from flask import Flask, render_template,Blueprint,flash,request,redirect,url_for,jsonify
from werkzeug.security import generate_password_hash
from . import db
from .models import User,Upload
from flask_login import login_required,current_user
import cloudinary.uploader
from sqlalchemy import or_,func
from datetime import datetime

views = Blueprint('views',__name__)

@views.route("/")
@login_required
def index():
    return render_template("welcome.html")

# @views.route('/messages', methods=['GET'])
# @login_required
# def messages():
#     # Subquery to get the most recent timestamp for each user
#     subquery = db.session.query(
#         Message.sender_id,
#         func.max(Message.timestamp).label('max_timestamp')
#     ).filter(Message.receiver_id == current_user.id).group_by(Message.sender_id).subquery()

#     # Fetch users with their most recent message timestamp, ordered by descending timestamp
#     users = User.query.join(
#         subquery, User.id == subquery.c.sender_id
#     ).order_by(subquery.c.max_timestamp.desc())

#     return render_template('messagelist.html', users=users)

@views.route('/my-listings', methods=['GET', 'POST'])
@login_required
def my_listings():
    if request.method == 'POST':
        # Handle the delete item action
        item_id = request.form.get('item_id')
        item_to_delete = Upload.query.get(item_id)

        if item_to_delete and item_to_delete.user_id == current_user.id:
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('Item removed successfully!', 'success')
        else:
            flash('Item could not be found or you do not have permission to delete it.', 'error')

        return redirect(url_for('views.my_listings'))

    # Fetch the current user's listings
    user_uploads = Upload.query.filter_by(user_id=current_user.id).all()
    return render_template('my_listings.html', uploads=user_uploads)



@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# @views.route('/message/<int:user_id>', methods=['GET', 'POST'])
# @login_required
# def message_user(user_id):
#     other_user = User.query.get_or_404(user_id)

#     if other_user == current_user:
#         flash("You cannot message yourself.", "error")
#         return redirect(url_for('views.index'))  # Redirect to books listing or appropriate page

#     if request.method == 'POST':
#         message_content = request.form.get('message_content')

#         if message_content:
#             message = Message(
#                 sender_id=current_user.id,
#                 receiver_id=user_id,
#                 content=message_content
#             )
#             db.session.add(message)
#             db.session.commit()
#             flash('Message sent successfully!', 'success')
#             return redirect(url_for('message.message_user', user_id=user_id))
#         else:
#             flash('Message content cannot be empty.', 'error')

#     messages = Message.query.filter(
#         ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
#         ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
#     ).order_by(Message.timestamp.asc()).all()

#     return render_template('message.html', messages=messages, other_user=other_user)


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
        matric_no = request.form.get("matric-no").lower()
        phone_number = request.form.get("phone-number")
        new_password = request.form.get("new-password")
        confirm_password = request.form.get("confirm-password")
        print(matric_no)

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
        try:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while resetting the password. Please try again.', 'error')
            print(f"Error: {e}")  # Log the error for debugging purposes
            return redirect(url_for('views.forgot_password'))

    return render_template('forgotpass.html')
 
@views.route('/exchange', methods=['GET'])
@login_required
def exchange():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information and filter by category
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%")
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "exchange"
        ).all()

    return render_template('exchange.html', uploads=uploads, search_query=search_query)

########## THIS IS A ROUTE FOR THE BOOKS ############
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

########## THIS IS A ROUTE FOR THE PAST QUESTION ############
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

########## THIS IS A ROUTE FOR THE NEWS ############
@views.route('/news', methods=['GET'])
@login_required
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

@views.route('/buy', methods=['GET'])
@login_required
def buy():
    search_query = request.args.get('q', '')

    # Query uploads with associated user information and filter by category
    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "sell",
            or_(Upload.title.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%"))
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "sell"
        ).all()

    return render_template('buy.html', uploads=uploads, search_query=search_query)

@views.route('/services', methods=['GET'])
@login_required
def services():
    search_query = request.args.get('q', '')

    if search_query:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "services",
            or_(Upload.title.ilike(f"%{search_query}%"), User.username.ilike(f"%{search_query}%"))
        ).all()
    else:
        uploads = db.session.query(Upload, User).join(User).filter(
            Upload.category == "services"
        ).all()

    return render_template('services.html', uploads=uploads)

@views.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        user.full_name = request.form['full_name']
        user.phone_number = request.form['phone_number']
        user.address = request.form['address']
        user.reg_officer_no = request.form['reg_officer_no']
        user.department = request.form['department']
        user.level = request.form['level']
        user.bio = request.form['bio']
        
        if 'picture' in request.files:
            picture = request.files['picture']
            if picture:
                upload_result = cloudinary.uploader.upload(picture)
                user.picture = upload_result['secure_url']
        
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('views.profile'))

    return render_template('settings.html', user=user)
