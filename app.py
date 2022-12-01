import os

from requests import request as rq
from flask import Flask, request, Response
from flask_restful import Resource, Api
from src.busca_dados_cadastrais import BuscaDadosCadastrais
from src.sistema_arquivos import SistemaArquivos
from src.lib.cors import build_cors_response
from src.validation.validate_json import validator, get_json_schema

UPLOAD_FOLDER = os.getcwd()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

api = Api(app)

class PHAuth(Resource):

    @app.route("/api/v1/Query/CadastroCompleto", methods=["GET", "POST"])       
    def cadastro_completo(*self):        
                
        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')        

        token: str = request.headers.get('Access-Token')
        worker: BuscaDadosCadastrais = BuscaDadosCadastrais()

        if request.method == "GET":            
            return worker.buscar_cadastro_complementar(token)

        elif request.method == "POST":  
            body: dict = request.get_json()     
            schema: str = "CadastroCompletoPOST"

            # validar json
            if not validator(body, schema): return Response(get_json_schema(schema), 400)

            return worker.atualizar_cadastro_complementar(token, body)
    
    @app.route("/api/v1/Query/FileSystem", methods=["GET", "POST", "PUT", "DELETE"])
    def file_system(*self):
        
        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')

        worker: SistemaArquivos = SistemaArquivos()

        return worker.fazer_request(request)

    @app.route("/api/v1/Query/FileSystem/ListFiles", methods=["GET"])
    def list_system(*self):
        
        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')

        worker: SistemaArquivos = SistemaArquivos()

        return worker.listar_arquivos(request)

    @app.route('/api/v1/Query/ListAAI', methods=["GET"])
    def list_aai(*self): 

        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')

        token: str = request.headers.get('Access-Token')
        worker: BuscaDadosCadastrais = BuscaDadosCadastrais()

        return worker.buscar_assessores(token)

    @app.after_request
    def AfterRequest(response: Response):
        return build_cors_response(response)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)