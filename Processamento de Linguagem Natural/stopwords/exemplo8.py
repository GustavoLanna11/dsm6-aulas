import nltk

texto= "No meio do caminho tinha uma pedra tinha uma pedra no meio do caminho tinha uma pedra no meio do caminho tinha uma pedra. Nunca me esquecerei desse acontecimento na vida de minhas retinas tão fatigadas. Nunca me esquecerei que no meio do caminho tinha uma pedra tinha uma pedra no meio do caminho no meio do caminho tinha uma pedra."

vocabulario = []

palavras = nltk.word_tokenize(texto.lower())

stop_words = nltk.corpus.stopwords.words("portuguese")

for palavra in palavras:
    if not(palavra in stop_words):
        vocabulario.append(palavra)

#print(stop_words)

print(vocabulario)

