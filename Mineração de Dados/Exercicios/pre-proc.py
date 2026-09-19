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

# Padronização e Normalização 
variaveis = ['idade_cliente', 'renda_mensal', 'valor_total']

# Mostra como idade, renda e valor de compra possuem escalas muito diferentes
print('\nEscala Original:')
print(limpo[variaveis].agg('min', 'max', 'mean').round(2))

#Min - Max transforma cada atributo para o intervalo de 0 e 1
limpo[['idade_minmax', 'renda_minmax', 'valor_minmax']] = (MinMaxScaler().fit_transform(limpo[variaveis]))
fit_transform(limpo[variaveis])

# Z-Score deixar a média próxima a 0 e o desvio-padrão próximo a 1
limpo[['idade_z', 'renda_z', 'valor_z']] = (StandardScaler().fit_transform(limpo[variaveis]))

# RobustScaler uma a mediana e quartis, sendo util quando existem outliers
limpo['renda_robusta']=(RobustScaler().fit_transform(limpo[['renda_mensal']]).ravel())

print('\nExemplo das trasnformações: ')
print(
    limpo[
        'idade_cliente',
        'idade_minmax',
        'idade_z',
        'renda_mensal',
        'renda_minmax',
        'renda_z',
        'renda_robusta',
    ].head(5).round(3).to_string(index=False)
)

# Discritização e Binarização
limpo['faixa_etaria'] = pd.cut(
    limpo['idade_cliente'], 
    bins=[17, 24, 34, 44, 54, 64, 120]
    labels=['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
)

# Qcut: divide os dados em quantis, útil para criar faixas de renda
limpo['faixa_renda'] = pd.qcut(
    limpo['renda_mensal'], 
    q=4, 
    labels=['Baixo', 'Médio', 'Alto', 'Muito Alto']
)

#Binarização: acima de mil recebe 1 caso contrário 0
limpo['alto_ticket']=(limpo['valor_total']>1000).astype(int)
print('\nFaixas Etárias:')
print(limpo['faixa_etaria'].value_counts(sort=False))

print('\nFaixas de Ticket:')
print(limpo['faixa_ticket'].value_counts(sort=False))

print('\nPedidos acima de mil:')
print(limpo['alto_ticket'].value_counts().sort_index())
print(f"Percentual de alto ticket: {limpo['alto_ticket'].mean()*100:.2f}%")

#Codificação de variáveis categóricas


dumies = [
    c for c in modelo.columns
    if c.startswith(('forma_pagamento_', 'canal_venda_', 'dispositivo_'))
]

print ('Colunas criadas pelo One-hot:', len(dumies))
print  (dumies)


#Labe/Ordinal Encoding: como fidelidade possui ordem natural, usamos números que representam Bronze < Prata < Ouro < Diamante

ordem = {'BRONZE': 0, 'PRATA': 1, 'OURO': 2, 'DIAMANTE': 3}
limpo['fidelidade_cod'] = limpo['nivel_fidelidade'].str.upper().map(ordem)

print('\nCodificação de fidelidade:')
print(
    limpo[['nivel_fidelidade', 'fidelidade_cod']]
    .drop_duplicates()
    .sort_values('fidelidade_cod')
    .to_string(index=False)
)

# Target Encoding precisa aprender SOMENTE com o treino, evitando que informações
treino, teste=train_test_split(
    limpo,
    test_size=0.25,
    random_state=42,
    stratify=limpo['recomprou_90d']
)

media_global= treino['recomprou_90d'].mean()
mapa_target = treino.groupby('id_parceiro')['recomprou_90d'].mean()
teste=teste.copy()
teste['parceiro_te']=(
    teste['id_parceiro'].map(mapa_target).fillna(media_global)
)

print('\nTreino:', len(treino), '|Teste:', len(teste))
print(f'Média global de recompra: {media_global:.3f}')

print('\nExemplo de Target Encoding:')
print(
    teste[['id_parceiro', 'recomprou_90d', 'parceiro_te']]
    .head(8)
    .round(3)
    .to_string(index=False)
)

#Resumo
print('\n === Resumo de Pré-Processamento ===')
print('Base Recebida: ', len(df), 'linhas')
print('Base Limpa:', len(limpo), 'linhas')
print('O dado passou por: limpeza -> transformação -> discritização -> codificação')