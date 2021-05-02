from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import json
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pass2021!@database:5432/udacity_fullstack_02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo ID: {self.id}, description: {self.description}>'

db.create_all()

@app.route('/')
def index():
    # data = [
    #     {
    #     'description': 'Todo 1'
    #     },
    #     {
    #     'description': 'Todo 2'
    #     },
    #     {
    #     'description': 'Todo 3'
    #     },
    #     {
    #     'description': 'Todo 4'
    #     }
    # ]

    data = Todo.query.all()
    return render_template('index.html', data=data)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # description = request.form.get('description', '')
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")