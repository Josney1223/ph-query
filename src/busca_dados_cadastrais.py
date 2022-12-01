import pandas as pd

from json import dumps
from flask import Response
from src.classes.busca_dados import BuscaDados

class BuscaDadosCadastrais(BuscaDados):
    def __init__(self) -> None:
        super().__init__()    

    def buscar_cadastro_complementar(self, token: str) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(token)        
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        # Busca dados complementares
        return_df: pd.DataFrame = self._run_query("CALL BuscaCadastroComplementar({});".format(id_user))

        if return_df.empty: return Response("", 204, mimetype="text/plain")

        return Response(dumps(return_df.to_dict("records")[0]), 200, mimetype="application/json")

    def atualizar_cadastro_complementar(self, token: str, request_json: dict) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(token)
        if resp_token.status_code != 200: return Response(resp_token.content, resp_token.status_code)
        id_user: int = resp_token.json()["id_user"]

        params: tuple = (id_user, request_json["segmentacao"], request_json["faturamento"], request_json["grupo_economico"], request_json["assessor"])
        self._run_query("CALL ProjetoHorizonte.CadastrarAtualizarCadastroComplementar(%s, %s, %s, %s, %s);", params=params, has_return=False)

        return Response("Updated", 202, mimetype="text/plain")
