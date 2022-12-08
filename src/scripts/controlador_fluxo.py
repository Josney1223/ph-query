import pandas as pd
import json
import requests

from flask import Request, Response
from src.classes.busca_dados import BuscaDados

class ControladorEtapas(BuscaDados):
    def __init__(self) -> None:
        self.endpoint_email: str = "http://192.168.66.102:2002/api/v1/GerarEmail/EmailBasico"
        super().__init__() 

    def busca_etapas(self) -> Response:
        query: str = "SELECT * FROM ProjetoHorizonte.TipoEtapa;"

        return Response(self._run_query(query), 200, mimetype="application/json")

    def alterar_etapas(self, UserID: int, ProjectID: int, EtapaID: int) -> Response:        
        
        query: str = "CALL ProjetoHorizonte.AlterarEtapa({}, {}, {});".format(UserID, ProjectID, EtapaID)

        self._run_query(query, has_return=False)

        return Response("Alterado", 200)
    
    def finalizar_projeto(self, request: Request) -> Response:
        json_data: dict = request.get_json() 
        resultado: int = json_data.get("resultado")
        UserID: int = json_data.get("UserID")
        ProjectID: int = json_data.get("ProjectID")
        mensagem: int = json_data.get("mensagem")

        if resultado in (0, 1):
            query: str = "CALL ProjetoHorizonte.FinalizarAnalise({}, {}, {})".format(UserID, ProjectID, resultado)

            self._run_query(query, has_return=False)

            return Response("Finalizado", 200)
        elif resultado == 2:

            query: str = "CALL ProjetoHorizonte.BuscarEmail({})".format(UserID)   

            df: pd.DataFrame = self._run_query(query)

            dict_email: dict = {
                "Destinatario": [str(df.iloc[0,0])],
                "Cc": [str(df.iloc[0,1])],
                "Cco": [],
                "Assunto": "Revisão de Proposta",
                "Corpo": [
                    {
                        "Tipo": "texto",
                        "Conteudo": mensagem
                    }
                ]
            }

            requests.post(self.endpoint_email, files={'file': ('body.json', json.dumps(dict_email).encode('utf-8'))})

            return Response("Enviado mensagem para Cliente", 200)