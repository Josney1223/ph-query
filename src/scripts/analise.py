from json import dumps
from flask import Response, Request
from src.classes.busca_dados import BuscaDados

class AnaliseCredito(BuscaDados):
    def __init__(self):
        super().__init__()

    def busca_analise_credito(self, request: Request) -> list[list]:
        
        json: dict = request.args        

        if json.get('UserID') == None:
            resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
            if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
            id_user: int = resp_token.json()["id_user"]
        else:
            id_user: int = json.get('UserID')
        
        query: str = "CALL ProjetoHorizonte.BuscaAnalise({}, {});".format(id_user, json.get('ProjectID'))

        try:
            return_df = self._run_query(query)
        except Exception as ex:
            print(ex.args)
            return Response("Falha em processar o pedido.", 500)

        return Response(dumps(return_df.to_dict("records")[0], default=str), 202, mimetype="application/json") 

    def create_analise_credito(self, request: Request) -> Response:

        resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        json: dict = request.get_json()

        query: str = "CALL ProjetoHorizonte.NovaAnalise({}, {}, {}, '{}', {});".format(id_user, 
                        json.get('valor_credito'),
                        json.get('periodo_divida'),
                        json.get('produto'),
                        json.get('juros'))
        
        try:
            self._run_query(query, has_return=False)
        except Exception as ex:
            print(ex.args)
            return Response("Falha em processar o pedido.", 500)

        return Response("Sucesso", 202)    