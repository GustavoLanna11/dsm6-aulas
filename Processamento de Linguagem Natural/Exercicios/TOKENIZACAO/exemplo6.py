import nltk

avaliacao =["O produto é excelente. Eu compraria de novo","Chegou rápido o produto!"]
vocabulario = []

for texto in avaliacao:
    frases = nltk.sent_tokenize(texto)
    print(frases)
    for frase in frases:
        vocabulario.append(frase)

print(vocabulario)