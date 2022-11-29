import mysql.connector
import pandas as pd

from mysql.connector.errors import IntegrityError, DatabaseError
from requests import get, Response
from sqlalchemy import create_engine, engine
from typing import Union


class BuscaDados:
    def __init__(self) -> None:

        self.website_auth: str = "https://projetohorizonte.materacapital.com.br/api/v1/Auth/ValidateToken"
        self.db_access: tuple[str] = ("10.147.17.25", "admin_projeto_horizonte", "PROJETO TI@TCC2022") 
        self.db_engine: engine.Engine = create_engine('mysql+pymysql://admin_projeto_horizonte:PROJETO%20TI%40TCC2022@10.147.17.25:3306/ProjetoHorizonte')

    def _validar_token(self, token: str) -> Response:
        return get(self.website_auth, headers={"Access-Token": token})    

    def _run_query(self, query: str, params: tuple = (), has_return: bool = True) -> Union[pd.DataFrame, None]:
        
        if has_return:
            try:   
                df = pd.read_sql(query, con=self.db_engine)         
                return df
            except Exception as e:
                raise Exception("Falha ao se conectar com o banco de dados.", e.args)        
        else:
            with mysql.connector.connect(host = self.db_access[0],                                                
                                        user = self.db_access[1],
                                        password = self.db_access[2]) as con:
                cursor = con.cursor()
                cursor.execute(query, params)
                con.commit()

        return None
