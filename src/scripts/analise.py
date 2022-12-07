from json import dumps
from flask import Response, Request
import pandas as pd
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
            id_analise_df: pd.DataFrame = self._run_query(query, has_return=True)
            
        except Exception as ex:
            print(ex.args)
            return Response("Falha em processar o pedido.", 500)
        id_analise = str(id_analise_df.iloc[0,0])
        id_user = str(id_analise_df.iloc[0,1])
        response_json = '{{"id_analise":{},"id_user":{}}}'.format(id_analise,id_user )
        

        return Response(response_json, 200)    

    def atualizar_analise_credito(self, request: Request) -> Response:

        resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        json: dict = request.get_json()

        query: str = "CALL ProjetoHorizonte.AtualizarAnalise({}, {}, {}, {}, '{}', {});".format(id_user, 
                        json.get('id_analise'),
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