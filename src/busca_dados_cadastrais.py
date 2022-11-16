import pandas as pd

from json import dumps
from flask import Response
from src.classes.busca_dados import BuscaDados

class BuscaDadosCadastrais(BuscaDados):
    def __init__(self) -> None:
        super().__init__()

    def _buscar_cpf_cadastro(self, id: int) -> int:
        # Utilizado para buscar arquivos
        return self._run_query("CALL BuscaCPF({});".format(id)).values.tolist()[0][0]

    def buscar_cadastro_complementar(self, token: str) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(token)        
        if resp_token.status_code != 200: return resp_token            
        id_user: int = resp_token.json()["id_user"]

        # Busca dados complementares
        return_df: pd.DataFrame = self._run_query("CALL BuscaCadastroComplementar({});".format(id_user))

        if return_df.empty: return Response("", 204, mimetype="text/plain")

        return Response(dumps(return_df.to_dict("records")[0]), 200, mimetype="application/json")

    def atualizar_cadastro_complementar(self, token: str, request_json: dict) -> Response:
        # Busca id
        resp_token: Response = self._validar_token(token)
        if resp_token.status_code != 200: return resp_token
        id_user: int = resp_token.json()["id_user"]

        params: tuple = (id_user, request_json["segmentacao"], request_json["faturamento"], request_json["grupo_economico"])
        self._run_query("CALL ProjetoHorizonte.CadastrarAtualizarCadastroComplementar(%s, %s, %s, %s);", params=params, has_return=False)

        return Response("Updated", 202, mimetype="text/plain")
