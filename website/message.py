# message.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User,Message
from . import db
from sqlalchemy import func


message = Blueprint('message', __name__)

@message.route('/message/<int:user_id>', methods=['GET', 'POST'])
@login_required
def message_user(user_id):
    other_user = User.query.get_or_404(user_id)

    if other_user == current_user:
        flash("You cannot message yourself.", "error")
        return redirect(url_for('views.index'))  # Redirect to books listing or appropriate page

    if request.method == 'POST':
        message_content = request.form.get('message_content')

        if message_content:
            message = Message(
                sender_id=current_user.id,
                receiver_id=user_id,
                content=message_content
            )
            db.session.add(message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
            return redirect(url_for('message.message_user', user_id=user_id))
        else:
            flash('Message content cannot be empty.', 'error')

    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp.asc()).all()

    return render_template('message.html', messages=messages, other_user=other_user)




@message.route('/messages', methods=['GET'])
@login_required
def messages():
    # Subquery to get the most recent timestamp for each user
    subquery = db.session.query(
        Message.sender_id,
        func.max(Message.timestamp).label('max_timestamp')
    ).filter(Message.receiver_id == current_user.id).group_by(Message.sender_id).subquery()

    # Fetch users with their most recent message timestamp, ordered by descending timestamp
    users = User.query.join(
        subquery, User.id == subquery.c.sender_id
    ).order_by(subquery.c.max_timestamp.desc())

    return render_template('messagelist.html', users=users)