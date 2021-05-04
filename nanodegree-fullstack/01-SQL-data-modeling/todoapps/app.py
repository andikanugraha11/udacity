from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate
import json
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pass2021!@database:5432/udacity_fullstack_02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}>'

# db.create_all()

@app.route('/')
def index():
    data = Todo.query.order_by('id').all()
    return render_template('index.html', data=data)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        print(sys.exc_info())
        error = True
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def todo_set_completed(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    success = False
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        success = True
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': success })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")