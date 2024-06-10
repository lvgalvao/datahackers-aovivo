import pandas as pd
import sqlite3
import os
from transforme import integrar_dados, processar_dados_movimentacao,tratar_dados_extraidos
from extract import buscar_todos_dados_commodities

def criar_dw(df_integrado):
    os.makedirs('data/dw', exist_ok=True)
    conn = sqlite3.connect('data/dw/commodities_dw.db')
    df_integrado.to_sql('commodities', conn, if_exists='replace', index=False)
    conn.close()
    print("Data Warehouse criado em data/dw/commodities_dw.db")

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities()
    dados_tratados = tratar_dados_extraidos(dados_concatenados)
    df_movimentacao = processar_dados_movimentacao('data/external/movimentacao_commodities.csv')
    df_integrado = integrar_dados(dados_tratados, df_movimentacao)
    criar_dw(df_integrado)
