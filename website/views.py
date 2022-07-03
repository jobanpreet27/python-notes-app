from flask import Blueprint, jsonify, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Notes
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/',methods =['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        if current_user.is_authenticated:
            data = request.form.get('note')
            new_note = Notes(data=data,user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Saved', category="success")

    return render_template("home.html", user=current_user)

@views.route('/delete-note',methods=['DELETE'])
@login_required
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Notes.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
