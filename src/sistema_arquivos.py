import requests

from flask import Request, Response
from src.classes.busca_dados import BuscaDados

class SistemaArquivos(BuscaDados):
    def __init__(self) -> None:
        self.url: str = "http://192.168.0.33:40000/api/v1/FileSystem"
        BuscaDados.__init__(self)

    def _buscar_cpf_cadastro(self, id: int) -> int:
        # Utilizado para buscar arquivos
        return self._run_query("CALL BuscaCPF({});".format(id)).values.tolist()[0][0]
    
    def fazer_request(self, request: Request) -> Response:                
        # Busca id
        resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        cpf: str = self._buscar_cpf_cadastro(id_user)

        args: dict = {
            "CPF": cpf,
            "FileName": request.args.get("FileName")
        }

        resp: requests.Response = requests.request(request.method, self.url, params=args, data=request.data)

        return Response(resp.content, resp.status_code)

    def listar_arquivos(self, request: Request) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        cpf: str = self._buscar_cpf_cadastro(id_user)

        args: dict = {
            "CPF": cpf            
        }

        resp: requests.Response = requests.request(request.method, "{}/ListFiles".format(self.url), params=args)

        return Response(resp.content, resp.status_code)