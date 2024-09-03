from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///padaria.db'
db = SQLAlchemy()
db.init_app(app)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
