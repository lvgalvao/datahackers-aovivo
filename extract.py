import yfinance as yf
import pandas as pd

# Lista de commodities
commodities = ['CL=F', 'GC=F', 'SI=F']  # Petróleo bruto, Ouro, Prata

def buscar_dados_commodities(simbolo, periodo='5d', intervalo='1d'):
    ticker = yf.Ticker(simbolo)
    dados = ticker.history(period=periodo, interval=intervalo)[['Close']]
    dados['simbolo'] = simbolo  # Adiciona a coluna do símbolo
    return dados

def buscar_todos_dados_commodities():
    todos_dados = []
    for simbolo in commodities:
        dados = buscar_dados_commodities(simbolo)
        todos_dados.append(dados)
    return pd.concat(todos_dados)  # Concatena todos os dados em um único DataFrame

if __name__ == "__main__":
    dados_concatenados = buscar_todos_dados_commodities()
    print("Dados concatenados:")
    print(dados_concatenados.head())
