from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personagens.db'
db = SQLAlchemy(app)

class Personagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500))
    link_imagem = db.Column(db.String(200))
    programa = db.Column(db.String(100))
    animador = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "link_imagem": self.link_imagem,
            "programa": self.programa,
            "animador": self.animador
        }

db.create_all()

@app.route('/characters/', methods=['POST'])
def criar_personagem():
    data = request.json

    personagem = Personagem(nome=data['nome'], descricao=data['descricao'], link_imagem=data['link_imagem'],
                            programa=data['programa'], animador=data['animador'])
    db.session.add(personagem)
    db.session.commit()

    return jsonify({"mensagem": "Personagem criado com sucesso!"}), 201

@app.route('/characters/', methods=['GET'])
def listar_personagens():
    personagens = Personagem.query.all()
    return jsonify({"personagens": [p.to_dict() for p in personagens]})

@app.route('/characters/<int:personagem_id>/', methods=['GET'])
def visualizar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    return jsonify(personagem.to_dict())

@app.route('/characters/<int:personagem_id>/', methods=['PUT'])
def atualizar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    data = request.json

    personagem.nome = data['nome']
    personagem.descricao = data['descricao']
    personagem.link_imagem = data['link_imagem']
    personagem.programa = data['programa']
    personagem.animador = data['animador']

    db.session.commit()
    return jsonify({"mensagem": "Personagem atualizado com sucesso!"})

@app.route('/characters/<int:personagem_id>/', methods=['DELETE'])
def deletar_personagem(personagem_id):
    personagem = Personagem.query.get_or_404(personagem_id)
    db.session.delete(personagem)
    db.session.commit()
    return jsonify({"mensagem": "Personagem deletado com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True)

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Gerenciamento de Personagens"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

