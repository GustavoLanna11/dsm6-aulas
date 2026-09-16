from collections import Counter
import string
import nltk

# Garantir downloads das dependências do NLTK
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Leitura do arquivo corpus.txt
with open("corpus.txt", "r", encoding="utf-8") as arquivo:
    linhas = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    texto = "\n".join(linhas[:10])

# Tokenização inicial
tokens_iniciais = nltk.word_tokenize(texto.lower())

# Contagem da Q2 (Quantidade total, únicos e o mais frequente geral)
total_tokens_iniciais = len(tokens_iniciais)
tokens_unicos = len(set(tokens_iniciais))
token_mais_frequente_geral = Counter(tokens_iniciais).most_common(1)[0]

print("Tokenização Inicial:")
print(f"Quantidade total de tokens: {total_tokens_iniciais}")
print(f"Exemplo dos 10 primeiros tokens: {tokens_iniciais[:10]}\n")

# Remoção de Stopwords e Filtro de Pontuação
stop_words = set(nltk.corpus.stopwords.words("portuguese"))

# Lista mantendo pontuação
vocab_com_pontuacao = [w for w in tokens_iniciais if w not in stop_words]

# Lista removendo pontuação 
pontuacao_extra = {"–", "—", "''", "``", "...", "•"}
simbolos = set(string.punctuation).union(pontuacao_extra)

vocab_sem_pontuacao = [
    w for w in tokens_iniciais if w not in stop_words and w not in simbolos
]

print("Remoção de Stopwords: ")
print(f"Tokens restantes (com pontuação): {len(vocab_com_pontuacao)}")
print(f"Tokens restantes (sem pontuação): {len(vocab_sem_pontuacao)}\n")

# palavras frquentes
top_10 = Counter(vocab_sem_pontuacao).most_common(10)

print("10 Palavras mais frequentes")
for palavra, freq in top_10:
    print(f"{palavra}: {freq}x")