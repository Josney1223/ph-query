from flask import Response, Request
from src.classes.busca_dados import BuscaDados

class AnaliseCredito(BuscaDados):
    def __init__(self):
        super().__init__()

    def busca_analise_credito(self, id_user: int, id_analise_credito: int) -> list[list]:
        pass

    def create_analise_credito(self, request: Request) -> Response:

        resp_token: Response = self._validar_token(request.headers.get('Access-Token'))        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        query: str = "CALL ProjetoHorizonte.NovaAnalise(%s, %s, %s, '%s');"

        json: dict = request.get_json()

        params: tuple = (id_user,
                        json.get('valor_credito'),
                        json.get('periodo_divida'),
                        json.get('produto'))
                                
        try:
            self._run_query(query, params=params, has_return=False)
        except Exception as ex:
            return Response("Falha em processar o pedido.", 500)

        return Response("Sucesso", 202)    