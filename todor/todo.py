from flask import Blueprint, render_template, request, redirect, url_for, g
from todor.auth import login_required
from .models import Todo, User
from todor import db

bp = Blueprint('todo', __name__, url_prefix='/todo')

@bp.route('/list')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 5  
    
    todos_paginated = Todo.query.filter_by(created_by=g.user.id).paginate(page=page, per_page=per_page)
    
    return render_template('todo/index.html', todos=todos_paginated)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(g.user.id, title, desc)
        
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')


def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    todo = get_todo(id)
    
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False
        
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))
