from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect
import os

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


@app.route('/cadastrar_produtos', methods=['GET', 'POST'])
def cadastrar_produtos():  # put application's code here
    if request.method == 'POST':
        status={'type':'sucesso','mensagem':'Produto Cadastrado com Sucesso'}
        dados = request.form
        imagem = request.files['imagem']
        try:
            produto = Product(dados['nome'], dados['descricao'], dados['ingredientes'], dados['origem'],
                              imagem.filename)
            imagem.save(os.path.join('static/imagens', imagem.filename))
            db.session.add(produto)
            db.session.commit()
            return render_template('cadastrar.html', status=status)
        except:
            status = {'type': 'erro', 'mensagem': f'Houve um problema ao cadastrar o produto {dados["nome"]}!'}
            return render_template('cadastrar.html', status=status)
    else:
        return render_template('cadastrar.html')

@app.route("/editar_produto/<int:id>", methods=['GET', 'POST'])
def editar_produto(id):
    if request.method == 'POST':
        produto_editado = request.form
        imagem = request.files['imagem']
        produto = db.session.execute(db.select(Product).filter(Product.id == id)).scalar()

        produto.nome = produto_editado['nome']
        produto.descricao = produto_editado['descricao']
        produto.ingredientes = produto_editado['ingredientes']
        produto.origem = produto_editado['origem']
        if imagem.filename:
            produto.imagem = imagem.filename
        db.session.commit()
        return redirect("/listar_produtos")
    else:
        produto_editado = db.session.execute(db.select(Product).filter(Product.id == id)).scalar()
        return render_template('editar.html', produto = produto_editado)

@app.route("/deletar_produto/<int:id>")
def deletar_produto(id):
    produto_deletado = db.session.execute(db.select(Product).filter(Product.id == id)).scalar()
    db.session.delete(produto_deletado)
    db.session.commit()
    return redirect("/listar_produtos")





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)
