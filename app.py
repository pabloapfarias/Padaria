from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_templater

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///padaria.db'
db = SQLAlchemy()
db.init_app(app)



class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome =db.Column(db.String(100), nullable=False)
    descricao =db.Column(db.String(500))
    ingredientes =db.Column(db.String(500))
    origen = db.Column(db.String(100))
    imagem =db.Column(db.String(100))

    def __init__(self, nome: str, descricao: str,ingredientes: str,  origen: str, imagem: str) -> None:
        self.nome = nome
        self.descricao = descricao
        self.ingredientes = ingredientes
        self.origen = origen
        self.imagem = imagem


@app.route('/')
def hello_world():  # put application's code here
    return render_templater('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
