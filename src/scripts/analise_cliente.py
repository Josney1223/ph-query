import pandas as pd

from json import dumps
from flask import Response
from src.classes.busca_dados import BuscaDados

class AnaliseCliente(BuscaDados):
    def analise_cliente(self, token: str) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(token)        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]
    
        # Query
        return_df: pd.DataFrame = self._run_query("CALL AnaliseCreditoPorCliente({});".format(id_user))

        if return_df.empty: return Response("", 204, mimetype="text/plain")

        return Response(dumps(return_df.to_dict("records"), default=str), 200, mimetype="application/json")