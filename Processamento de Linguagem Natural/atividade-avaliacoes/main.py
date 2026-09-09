#Importando a biblioteca NLTK
import nltk

#Avaliação usada para exemplo
texto= "O mouse Ajazz AJ179 V2 é uma excelente opção para quem busca desempenho e conforto em um só produto. Com design ergonômico, leve e moderno, ele oferece uma pegada firme que garante precisão nos movimentos, ideal tanto para jogos quanto para uso no dia a dia. Seus switches responsivos e a qualidade de construção transmitem durabilidade, enquanto o sensor de alta performance entrega rapidez e confiabilidade em cada clique. Um periférico que une estilo, eficiência e ótimo custo-benefício."
vocabulario = []

#Tokenizando o texto
palavras = nltk.word_tokenize(texto.lower())

#Removendo as stopwords do texto
stop_words = nltk.corpus.stopwords.words("portuguese")

#separando as palavras que não são stopwords e adicionando ao vocabulário
for palavra in palavras:
    if not(palavra in stop_words):
        vocabulario.append(palavra)

#Mostrando as stopwords e o vocabulário resultante
#print(stop_words)

#Mostrando o vocabulário final
print(vocabulario)

