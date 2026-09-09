import nltk

text = "Paulo Freire disse que quando a educação não é libertadora, o sonho do oprimido é ser o opressor. Em tempos de minorias fazendo campanha para candidato que despreza seus direitos e necessidades, fica claro que nunca tivemos uma educação de fato libertadora. ;( #DiaDosProfessores #EducacaoLibertadora @PauloFreireOficial"

tokenizador = nltk.TweetTokenizer()

tweet = tokenizador.tokenize(text)

print(text)