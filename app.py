import os

from flask import Flask, request, Response
from flask_restful import Resource, Api
from src.busca_dados_cadastrais import BuscaDadosCadastrais
from src.lib.cors import build_cors_response

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = b'CDgWUjqcCaNURJD9AkcRgKaTucApXBGH'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'

api = Api(app)

class PHAuth(Resource):

    @app.route("/api/v1/Query/CadastroCompleto", methods=["GET", "POST"])       
    def UserAuth(*self):        
        
        token: str = request.headers.get('Access-Token')
        worker: BuscaDadosCadastrais = BuscaDadosCadastrais()

        if request.method == "GET":            
            return worker.buscar_cadastro_complementar(token)
        elif request.method == "POST":            
            return worker.atualizar_cadastro_complementar(token, request.get_json())
        
    @app.after_request
    def AfterRequest(response: Response):
        return build_cors_response(response)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)