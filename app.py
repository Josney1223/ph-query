import os

from json import dumps
from requests import request as rq
from flask import Flask, request, Response
from flask_restful import Resource, Api

from src.lib.cors import build_cors_response
from src.validation.validate_json import validator, get_json_schema

from src.scripts.busca_dados_cadastrais import BuscaDadosCadastrais
from src.scripts.sistema_arquivos import SistemaArquivos
from src.scripts.analise import AnaliseCredito
from src.scripts.analise_cliente import AnaliseCliente
from src.scripts.analise_credito import AnaliseAssessor
from src.scripts.alterar_etapa import ControladorEtapas

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
            if not validator(body, schema): return Response(dumps(get_json_schema(schema)), 400)

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

    @app.route('/api/v1/Query/List/Assessor', methods=["GET"])
    def list_client(*self): 

        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')

        token: str = request.headers.get('Access-Token')
        worker: BuscaDadosCadastrais = BuscaDadosCadastrais()

        return worker.buscar_assessores(token)

    @app.route("/api/v1/Query/Analise", methods=["GET", "POST", "PUT"])
    def analise_credito(*self):
        
        # validar token
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')

        worker: AnaliseCredito = AnaliseCredito()

        if request.method == 'GET':
            body: dict = request.args     
            schema: str = "AnaliseGET"
            # validar json
            if not validator(body, schema): return Response(dumps(get_json_schema(schema)), 400, mimetype="application/json")

            return worker.busca_analise_credito(request)

        elif request.method == 'POST':            
            return worker.create_analise_credito(request)
        elif request.method == 'PUT':
            return worker.atualizar_analise_credito(request)                    

    @app.route("/api/v1/Query/AnalisePorCliente", methods=["GET"])       
    def analise_por_cliente(*self):
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')            
        token: str = request.headers.get('Access-Token')        
    
        worker: AnaliseCliente = AnaliseCliente()

        return worker.analise_cliente(token)

    @app.route("/api/v1/Query/AnalisePorAssessor", methods=["GET"])       
    def analise_por_assessor(*self):
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')       
        token: str = request.headers.get('Access-Token')
        worker: AnaliseAssessor = AnaliseAssessor()

        return worker.analise_assessor(token)

    @app.route("/api/v1/Query/Etapas", methods=["GET"])
    def alterar_etapas(*self):
        if 'Access-Token' not in request.headers.keys(): return Response("Token não informado", 400, mimetype='text/plain')       
        token: str = request.headers.get('Access-Token')
        worker: ControladorEtapas = ControladorEtapas()

        return worker.busca_etapas()

    @app.after_request
    def AfterRequest(response: Response):
        return build_cors_response(response)

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=2000)