# Dataset Iris
# Utilizado para demonstrar, passo a passo como um algoritmo de Machine Learning funciona.

# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt #Criar gráficos
from sklearn.datasets import load_iris #Importar o dataset Iris
from sklearn.tree import DecisionTreeClassifier #Importar o algoritmo de árvore de decisão
from sklearn.tree import plot_tree #Importar a função para plotar a árvore de decisão

#Métricas de avaliação do modelo
from sklearn.metrics import accuracy_score #Importar a métrica de acurácia
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay #Importar a função para plotar a matriz de confusão
from sklearn.metrics import classification_report #Importar a função para gerar o relatório de classificação

#2 carregando o dataset Iris
iris = load_iris() #Carregando o dataset Iris
print('\n')
print('='*70)
print('Dataset Iris')
print('='*70)
print("\n Dataset carregado com sucesso!")

#3 Conhecendo o dataset Iris
#Quantidade de registros
print('\n quantidade de registros')
print(len(iris.data))

# Nome das caracteristicas
print('\n Nome das caracteristicas')
for caracteristicas in iris.feature_names:
    print("-", caracteristicas)

# Nome das especies
print('\n Nome das especies')
for especies in iris.target_names:
    print("-", especies)

#visualizando uma flor
print('\n')
print('='*70)
print('Visualizando uma flor')
print('='*70)

print('\n Medidas da primeira flor do dataset')
print("Comprimento da sépala: ", iris.data[0][0], "cm")
print("Largura da sépala: ", iris.data[0][1], "cm")
print("Comprimento da pétala: ", iris.data[0][2], "cm")
print("Largura da pétala: ", iris.data[0][3], "cm")