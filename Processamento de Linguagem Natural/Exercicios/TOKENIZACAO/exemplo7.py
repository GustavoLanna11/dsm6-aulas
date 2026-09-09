import nltk

avaliacao =["O produto é excelente. Eu compraria de novo","Chegou rápido o produto!"]
vocabulario = []
vocabulario_sem_repetidos = []

for texto in avaliacao:
    palavras = nltk.word_tokenize(texto.lower())
    print(palavras)
    for palavra in palavras:
        vocabulario.append(palavra)

print(vocabulario)
print(len(vocabulario))

vocabulario_sem_repetidos = set(vocabulario)
print(vocabulario_sem_repetidos)
print(len(vocabulario_sem_repetidos))

reducao = (len(vocabulario_sem_repetidos)/len(vocabulario))
print(reducao)