import requests
import json

from flask import Request, Response
from src.classes.busca_dados import BuscaDados

class ControladorEtapas(BuscaDados):
    def __init__(self) -> None:
        super().__init__() 

    def busca_etapas(self) -> Response:
        query: str = "SELECT * FROM ProjetoHorizonte.TipoEtapa;"

        return Response(self._run_query(query), 200, mimetype="application/json")

    def alterar_etapas(self, UserID: int, ProjectID: int, EtapaID: int) -> Response:        
        
        query: str = "CALL ProjetoHorizonte.AlterarEtapa({}, {}, {});".format(UserID, ProjectID, EtapaID)

        self._run_query(query)

        return Response("Alterado", 200)
        