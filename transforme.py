import pandas as pd
from extract import buscar_todos_dados_commodities

# Trata os dados extraídos das commodities
def tratar_dados_extraidos(dados):
    dados = dados.rename(columns={'Date': 'data'})  # Renomeia a coluna 'Date' para 'data'
    dados = dados.rename(columns={'Close': 'fechamento'})  # Renomeia a coluna 'Close' para 'fechamento'
    dados['data'] = pd.to_datetime(dados.index, utc=True).date  # Converte o índice (que são as datas) para datetime e extrai apenas a data
    return dados.reset_index(drop=True)  # Reseta o índice

# Processa os dados de movimentação
def processar_dados_movimentacao(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)  # Lê o CSV
    df['date'] = pd.to_datetime(df['date']).dt.date  # Converte a coluna 'date' para datetime e extrai a data
    df = df.rename(columns={'date': 'data','symbol': 'simbolo'}) # Renomeia a coluna 'date' para 'data'
    return df

# Integra os dados das commodities com os dados de movimentação
def integrar_dados(dados_commodities, df_movimentacao):
    df_integrado = dados_commodities.merge(df_movimentacao, on=['data', 'simbolo'], how='inner')  # Junta os dados com base nas colunas 'data' e 'simbolo'
    df_integrado['valor'] = df_integrado['quantity'] * df_integrado['fechamento']  # Calcula o valor da transação
    df_integrado['ganho'] = df_integrado.apply(
        lambda row: row['valor'] if row['action'] == 'sell' else -row['valor'], axis=1
    )
    return df_integrado

if __name__ == "__main__":
    # Busca e concatena os dados de todas as commodities
    dados_concatenados = buscar_todos_dados_commodities()
    dados_tratados = tratar_dados_extraidos(dados_concatenados)

    # Processa os dados de movimentação
    df_movimentacao = processar_dados_movimentacao('data/external/movimentacao_commodities.csv')
    print("Colunas de df_movimentacao:\n", df_movimentacao.columns)
    # Integra os dados e calcula o saldo
    df_integrado = integrar_dados(dados_tratados, df_movimentacao)
    print("Dados integrados:")
    print(df_integrado.head())
    # Você pode salvar ou continuar o processamento a partir daqui
    # df_integrado.to_csv('data/processed/commodities_data.csv', index=False)
    # print("Dados integrados salvos em data/processed/commodities_data.csv")
