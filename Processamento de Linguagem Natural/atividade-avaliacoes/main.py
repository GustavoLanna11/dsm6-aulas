import nltk

texto= "O mouse Ajazz AJ179 V2 é uma excelente opção para quem busca desempenho e conforto em um só produto. Com design ergonômico, leve e moderno, ele oferece uma pegada firme que garante precisão nos movimentos, ideal tanto para jogos quanto para uso no dia a dia. Seus switches responsivos e a qualidade de construção transmitem durabilidade, enquanto o sensor de alta performance entrega rapidez e confiabilidade em cada clique. Um periférico que une estilo, eficiência e ótimo custo-benefício."
vocabulario = []

palavras = nltk.word_tokenize(texto.lower())

stop_words = nltk.corpus.stopwords.words("portuguese")

for palavra in palavras:
    if not(palavra in stop_words):
        vocabulario.append(palavra)

#print(stop_words)

print(vocabulario)

