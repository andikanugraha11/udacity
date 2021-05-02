from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Pass2021!@database:5432/udacity_fullstack_02'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    data = [
        {
        'description': 'Todo 1'
        },
        {
        'description': 'Todo 2'
        },
        {
        'description': 'Todo 3'
        },
        {
        'description': 'Todo 4'
        }
    ]
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")