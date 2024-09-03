from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///padaria.db'
db = SQLAlchemy()
db.init_app(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500))
    ingredientes = db.Column(db.String(500))
    origem = db.Column(db.String(100))
    imagem = db.Column(db.String(100))

    def __init__(self, nome: str, descricao: str, ingredientes: str, origem: str, imagem: str) -> None:
        self.nome = nome
        self.descricao = descricao
        self.ingredientes = ingredientes
        self.origen = origem
        self.imagem = imagem


@app.route('/')
def home():  # put application's code here
    return render_template('index.html')


@app.route('/listar_produtos', methods=['GET', 'POST'])
def listar_produtos():
    if request.method == 'POST':
        termo = request.form['pesquisa']
        resultado = db.session.execute(db.select(Product).filter(Product.nome.like(f'%{termo}%'))).scalars()
        return render_template('listar_produtos.html', produtos=resultado)

    else:
        produtos = db.session.execute(db.select(Product)).scalars()
    return render_template('listar_produtos.html', produtos=produtos)


@app.route('/cadastrar_produtos')
def cadastrar_produtos():  # put application's code here
    return render_template('cadastrar.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
