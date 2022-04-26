# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:10:27 2020

@author: neres
"""

import nltk
import string
import pandas as pd
import Processamento_de_entrada as processamento
import Processamento_de_dataframe as prodata
import numpy as np


from Casamento_KMP import KMP
from Classes_Conselheiros import conselheiro




"""
necessario para funcionamento correto e atualizado da biblioteca nltk, 
#verificar no git da biblioteca como fazer pelo prompt e automatizar verificação de atualizações
#nltk.download()
"""
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import stopwords


#Para teste antes de incerir no modulo correto 
from matplotlib.colors import ListedColormap
from wordcloud import WordCloud
import matplotlib.pyplot as plt



#ALTERAR: inserir endereço correto
"""Alterar o funcionamento do processamento de entra, ao inves de indicar um
endereço onde estão todas as atas, encaminhar um arquivo com os endereços
de pastas diferentes para cada Ata.

MOTIVO: Facilitar a identificação por reunião além de possibilitar uma 
produção de material especifico para cada reunião. (Nuvem de palavras, 
                                                    Graficos, tabelas
                                                    relações com o obejto 
                                                    reunião)"""



# "Endereco_atas.txt" contem o endereço de todas as atas
reunioes, enderecos = processamento.entrada('Endereco_atas.txt')


#Aqui a melhoria possivel é uma futura desse bloco dentro do modulo
# de processamento de entradas isso pode ocorrer na medida em que 
# os padrões de busca são expandidos.
padrao = processamento.carrega_padroes('Padroes')


teste, teste_total, df, endereco = processamento.processa_entrada(reunioes, enderecos, padrao)

# retirando os dados gerais provisoriamente aqui 
#Primeiro limpando as frases armazenadas para gerar uma nuvem de palavras
palavras_total = ""
for conselheiro in teste_total:
    
    palavras =[]
    if(conselheiro.quantidade_falas() > 0):
        frases = conselheiro.palavras_faladas()
        for frase in frases:
            for palavra in frase:
                if not(palavra[-1].isalpha()):
                    palavras_total += " " + palavra[:-1]
                elif not(palavra[0].isalpha()):
                    palavras_total += " " + palavra[1:]
                else:
                    palavras_total += " " + palavra
            


#encontrar meio de tornar essas StopWords Globais
stops = stopwords.words('portuguese')
stops.append("aqui")
stops.append("201f")
stops.append("gs")
stops.append("então")
stops.append("porque")
stops.append("vai")
stops.append("aí")
stops.append("u")


mapa_cores = ListedColormap(['orange', 'green', 'red', 'magenta'])


nuvem = WordCloud(stopwords=stops,
                      background_color='black', width=1600,                            
                      height=800).generate(palavras_total)


fig, ax = plt.subplots(figsize=(16,8))            
ax.imshow(nuvem, interpolation='bilinear')       
ax.set_axis_off()
plt.imshow(nuvem)                 
nuvem.to_file('rafael.png');
#-----------------------------------------------

df_total = prodata.cria_data_falantes(teste_total)
prodata.grafico_barras(df_total, "Todas_reuniões")
prodata.grafico_barras_h(df_total, "Todas_reuniões")
prodata.grafico_pizza(df_total, "Todas_reuniões")

prodata.falas_no_ano(teste_total)

"""

kmp = KMP()

#listaa auxiliares usada para receber os conselheiros localizados no texto
    #sera uma lista de objetos da conselheiro
    #uma responsavel por registrar apenas os conselheiros em cada reunião
    #outra registra todos os conselheiros nomeados que aparecem no ano 
conselheiros_nomeados = []
    
conselheiros_reuniao = []

intervencao =''


    #Aqui pegamos as linhas com os padrões de busca (nomes dos conselheiros). 
    #Utilizamos o algoritmo de busca localizamos a posição onde estão as falas 
    #de cada conselheiros, além de criar um novo objeto do tipo conselheiro, 
    #inserindo já o nome do conselhereiro. O proximo passo segue a partir da 
    #verificação de existencia de falas do conselheiro, havendo então é 
    #armazenado o conteudo da fala buscando pelos caracteres usados no texto 
    #da ata para se referir a uma fala '“' e '”'

for indice in range( len( reunioes)):
    
        #reiniciar a lista de conselheiros e inserir a nova ata
    todo_texto = reunioes[indice]
    conselheiros_reuniao = []
    conselheiros_total = []
        
    if len(conselheiros_nomeados) > 1:
        print("deu ruim")
        
        print(enderecos[indice])
        
        #todas_as_falas = kmp.search(todo_texto, '“')
    
    for nome in padrao:
        
        falas = kmp.search(todo_texto, nome)
            
        #conselheiros_reuniao.append(conselheiro())
        #conselheiros_reuniao[-1].set_nome(nome)
            
        #verificaçao boleana, indice na lista de conselheiros
        verificacao, indice_total = processamento.verifica_conselheiro(
                                                            conselheiros_total, 
                                                             nome)
            
        if verificacao:
            conselheiros_total.append(conselheiro())
            conselheiros_total[-1].set_nome(nome)
            #print("adicionnando conselheiro: ", nome)
            #print("de numero: ", len(conselheiros_total))

            
        if falas != []:
            
            conselheiros_reuniao.append(conselheiro())
            conselheiros_reuniao[-1].set_nome(nome)
       
            #print(nome, ": ", len(falas))
            for posicao in falas:
                j = posicao
                if(todo_texto[j+len(nome)+2] == '“'):
                        
                    intervencao =''
                    #reiniciar a variavel para n acumular texto 
                    #Pensar em solução mais eficiente depois
                    
                    while(todo_texto[j+len(nome)+3] != '”'):
                        intervencao += todo_texto[j+len(nome)+3] 
                        j+=1
            
                    conselheiros_reuniao[-1].add_fala(intervencao.lower())
                    conselheiros_total[indice_total].add_fala(intervencao.lower()
                                                                  ) 
                        #conseguir algum indice pra indicar qual posição adico
                        #adicionar, levando o nome em consideração 


    processamento.nuvem_por_conselheiros(conselheiros_reuniao, 
                                         enderecos[indice])
        
    df = prodata.cria_data_falantes(conselheiros_reuniao)
        
        #inserir chegagem de existência da pasta para criação de novos caminhos
        #os.mkdir('endereco')
        
    endereco =( "Dados_por_reuniao/" + enderecos[indice][9:] + "/" + 
                    "Tabela_da_" + enderecos[indice][9:] + "_reuniao")
        
    prodata.salva_data_csv(df,endereco)
    prodata.salva_data_xlsx(df,endereco)
        
    endereco =( "Dados_por_reuniao/" + enderecos[indice][9:] + "/" + 
                    "grafico_da_" + enderecos[indice][9:] + "_reuniao")
        
    #prodata.grafico_barras(df, endereco)
    #prodata.grafico_barras_h(df, endereco)
        






falas_totais = []
auxiliar_falas_totais = ''
testando = 0
for i in range(len(todo_texto)): 
    if todo_texto[i] == '“':
        testando += 1
        
        print("total de falas é: ", testando)
#        for j in range(todo_texto[j] != '”'):
#            auxiliar_falas_totais += todo_texto[j]
#            j += 1
#    
#    auxiliar_falas_totais += todo_texto[j] 
#    falas_totais.append(auxiliar_falas_totais)        
#    auxiliar_falas_totais = ''

#gera e armazena nuvem de palavras para cada conselheiro com mais de uma fala


#BLOCO que esta fazendo uma lista com as palavras mais comuns
#precisa ser aprimorado e em seguida movido para modulo correro
#Processamento de entrada 
stops = stopwords.words('portuguese')

todas_as_falas_split = todas_as_falas.split()

palavras_semstop = [p for p in todas_as_falas_split if p not in stops]
len(palavras_semstop)

palavras_sem_pontuacao = [p for p in palavras_semstop if p not in string.punctuation]
len(palavras_sem_pontuacao)

frequencia = nltk.FreqDist(palavras_sem_pontuacao)
mais_comuns = frequencia.most_common(100)







#plt.barh(df['Nome'],df['Numero de Falas'], color = 'red')

#y_pos = range(len(df['Nome']))
#plt.bar(y_pos, df['Numero de Falas'])
# Rotation of the bars names
#plt.xticks(y_pos, df['Nome'], rotation=90)



ATÉ AQUI
"""


