import requests

from flask import Request, Response
from src.classes.busca_dados import BuscaDados

class SistemaArquivos(BuscaDados):
    def __init__(self) -> None:
        self.url: str = "http://192.168.66.102:40003/api/v1/FileSystem"
        super().__init__() 

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
            "FileName": request.args.get("FileName"),
            "ProjectID": request.args.get("ProjectID")
        }

        resp: requests.Response = requests.request(request.method, self.url, params=args, data=request.data)

        return Response(resp.content, resp.status_code, headers={"Contenta-Type": "application/octet-stream"})

    def listar_arquivos(self, request: Request, aai: bool = False) -> Response:
        
        if "UserID" not in request.args.keys():
            # Busca id
            resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
            if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
            id_user: int = resp_token.json()["id_user"]            
        else:        
            id_user: int = request.args.get("UserID")

        cpf: str = self._buscar_cpf_cadastro(id_user)

        args: dict = {
            "CPF": cpf ,
            "ProjectID": request.args.get("ProjectID")           
        }

        resp: requests.Response = requests.request(request.method, "{}/ListFiles".format(self.url), params=args)

        return Response(resp.content, resp.status_code)