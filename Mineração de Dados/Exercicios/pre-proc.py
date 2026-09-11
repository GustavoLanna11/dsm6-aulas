import pandas as pd 
import re #trabalha com expressões regulares, limpa caracteres especiais
import unicodedata #trabalha com acentuação, normaliza os caracteres especiais
from pathlib import Path #permite localizar arquivos e diretórios de forma mais simples
from sklearn.preprocessing import MinMaxScaler #normaliza os dados
from sklearn.preprocessing import StandardScaler #padroniza os dados
from sklearn.preprocessing import RobustScaler #padroniza os dados, mas é mais robusto a outliers
from sklearn.model_selection import train_test_split #divide os dados em treino e teste

#configuração

# Localiza o arquivo de dados
arquivo = Path(__file__).resolve().parent / "base_ecommerce_brasil_2026_suja.csv" #localiza o arquivo de dados

#carregar a base
df=pd.read_csv(arquivo, sep=";", encoding="utf-8") 

#função auxiliar: remove acentuação e caracteres especiais, caracter maisculo para minusculo, remove espaços em branco no início e no final da string
def padronizar(valor):
    if pd.isna(valor):
        return valor
    
    valor = str(valor).strip().upper()
    valor = ''.join(
        letra for letra in unicodedata.normalize('NFKD', valor)
        if not unicodedata.combining(letra)
    )
    valor = re.sub(r'[^A-Z0-9]', '', valor)
    return re.sub(r'\s+', ' ', valor)  # Remove espaços extras

#conhecer a base sem alterar nada
print('Linhas recebidas: ', len(df))
print('Duplicados Exatos: ', df.duplicated().sum())
print('Ids de pedido repetidos: ', df.duplicated(('id_pedido')).sum())
print('Pedidos únicos: ', df['id_pedido'].nunique())

#Remover apenas as linhas totalmente iguais
limpo = df.drop_duplicates().copy()

limpo['nome_cliente'] = limpo['nome_cliente'].str.strip().str.title()
limpo['email'] = limpo['email'].str.strip().str.lower()
limpo['telefone'] = limpo['telefone'].str.replace(r'\D', '', regex=True)  # Remove caracteres não numéricos
limpo['data_pedido'] = pd.to_datetime(limpo['data_pedido'], errors='coerce', dayfirst=True, format='mixed').dt.strftime('%Y-%m-%d')

#Estados escritos por extenso serão convertidos
mapa_uf = {
    'ACRE': 'AC',
    'ALAGOAS': 'AL',
    'AMAZONAS': 'AM',
    'AMAPA': 'AP',
    'BAHIA': 'BA',
    'CEARA': 'CE',
    'DISTRITO FEDERAL': 'DF',
    'ESPIRITO SANTO': 'ES',
    'GOIAS': 'GO',
    'MARANHAO': 'MA',
    'MINAS GERAIS': 'MG',
    'MATO GROSSO DO SUL': 'MS',
    'MATO GROSSO': 'MT',
    'PARA': 'PA',
    'PARAIBA': 'PB',
    'PERNAMBUCO': 'PE',
    'PIAUI': 'PI',
    'PARANA': 'PR',
    'RIO DE JANEIRO': 'RJ',
    'RIO GRANDE DO NORTE': 'RN',
    'RONDONIA': 'RO',
    'RORAIMA': 'RR',
    'RIO GRANDE DO SUL': 'RS',
    'SANTA CATARINA': 'SC',
    'SERGIPE': 'SE',
    'SAO PAULO':  "SP",
}

limpo['estado'] = limpo['estado'].map(padronizar).replace(mapa_uf)

#categorias diferentes que significam o mesmo recebem o mesmo padrão
limpo['forma_pagamento']=(limpo['forma_pagamento'].map(padronizar).replace({
    'PAGAMENTO INSTANTANEO': 'PIX',
    'CARTAOCREDITO': 'CARTAO_CREDITO',
    'CARTAO CREDITO': 'CARTAO_CREDITO',
    'CARTAODEBITO': 'CARTAO_DEBITO',
    'CARTAO DEBITO': 'CARTAO_DEBITO',
    'DEBITO':'CARTAO_DEBITO',
    'BOLETO BANCARIO': 'BOLETO',
    'CARTEIRADIGITAL': 'CARTEIRA_DIGITAL',
    'CARTEIRA DIGITAL': 'CARTEIRA_DIGITAL',
    'WALLET': 'CARTEIRA_DIGITAL',
}))

limpo['dispositivo']=limpo['dispositivo'].map(padronizar)
limpo['categoria_produto']=limpo['categoria_produto'].map(padronizar)


#Após padronizar, registros antes "diferentes" podem se tornar iguais, então vamos remover duplicados novamente
limpo = limpo.drop_duplicates().copy()
print('Linhas após limpeza: ', len(limpo))
print('Estados após padronização: ', limpo['estado'].nunique())
print('Formas de pagamento após padronização: ', limpo['forma_pagamento'].nunique())
print('Canais de Vendas: ', limpo['canal_venda'].nunique())