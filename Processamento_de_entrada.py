# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 14:46:50 2020

@author: -
"""

import os
import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt

import Processamento_de_dataframe as prodata
"""
necessario, para funcionamento correto, a atualização da biblioteca nltk, 
verificar no git da biblioteca como fazer pelo prompt e automatizar 
verificação de atualizações ---> nltk.download()
"""

from Classes_Conselheiros import conselheiro
from Casamento_KMP import KMP

from nltk.corpus import PlaintextCorpusReader
from matplotlib.colors import ListedColormap
from wordcloud import WordCloud
from nltk.corpus import stopwords


#-----------------------------------------------------------------------------
#Essa função recebe como entrada um caminho de diretorio para um arquivo TXT, 
#esperasse uma string, o arquivo deve conter os caminhos de todas as atas que 
#Serão analisadas. 
#As atas devem estar no padrão utilizado pelo COPAM SISEMA MG(2020). 
#para então abrir esses
#arquivos e executar a primeira operação de tratamento retirando as numerações
#de linhas
#
#Inserir verificação de tipo de entrada 
def entrada(diretorio):
    
    arquivo = open(diretorio, 'r')

    linhas = arquivo.read()

    linhas = linhas.splitlines()

    reunioes = []

    for endereco in linhas:
        corpus = PlaintextCorpusReader(endereco, '.*')

        #cria uma variavel com o nome de todos os arquivos dentro do corpus
        #arquivos = corpus.fileids()


        #Cria um bloco de texto contendo todas as atas para facilitar a analise e 
        #não perder informações. Executamos também 
        #algumas operações para formatar os dados
    
        #Recebe o texto de todos os PDF's
        todo_texto = corpus.raw()
    
        #Divide em linhas para retirar a numeração das linhas
        todo_texto_linhas = todo_texto.splitlines() 

        #Prepara a lista que recebe as linhas formatadas
        todo_texto_sem_numeros = ''

        #Remove a numeração das linhas para facilitar as analises futuras
        #Melhorar o codigo ao tirar apenas os numeros marcando a pagina,
        #considerar retirar somente as primeiras ocorrências de numero até
        #localizar um espaço " ".
        for linha in todo_texto_linhas:
            for indice in range(len(linha)):
                if(not (linha[indice].isnumeric())):
                    todo_texto_sem_numeros += linha[indice:]
                    break
    
        reunioes.append(todo_texto_sem_numeros)
    
    return reunioes, linhas

#    for linha in todo_texto_linhas:
#        for indice in range(len(linha)):
#            if(not (linha[indice].isnumeric())
#               and not (linha[indice].isspace())):
#                todo_texto_sem_numeros.append(linha[indice:])
#                break
    #ESTA REMOVENDO MAIS ESPAÇOS DO QUE DEVERIA
    #esse proceso infelismente retira também a numerão da reunião, mas considera-
    #mos esta uma perda menor mais facilmente contornavel
#Conferir se casos onde os nomes estão divididos pela numeração são perdidos
#-----------------------------------------------------------------------------
def carrega_padroes(diretorio):
    
    corpus = PlaintextCorpusReader(diretorio, '.*')
    padrao = corpus.raw()
    padrao = padrao.splitlines()
    
    return padrao


#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def processa_entrada(reunioes, enderecos, padrao):
    
    
    #carrega o algoritmo KMP, verificar se o python tem um metodo imbutido que 
    #pode ser utilizado, pode ser interessante caso mais buscas por padrões 
    #sejam realizadas
    kmp = KMP()

    #listaa auxiliares usada para receber os conselheiros localizados no texto
    #sera uma lista de objetos da conselheiro
    #uma responsavel por registrar apenas os conselheiros em cada reunião
    #outra registra todos os conselheiros nomeados que aparecem no ano     
    conselheiros_reuniao = []

    intervencao =''

    conselheiros_total = []

    #Aqui pegamos as linhas com os padrões de busca (nomes dos conselheiros). 
    #Utilizamos o algoritmo de busca localizamos a posição onde estão as falas 
    #de cada conselheiros, além de criar um novo objeto do tipo conselheiro, 
    #inserindo já o nome do conselhereiro. O proximo passo segue a partir da 
    #verificação de existencia de falas do conselheiro, havendo então é 
    #armazenado o conteudo da fala buscando pelos caracteres usados no texto 
    #da ata para se referir a uma fala '“' e '”'
    
    #ISSO PRECISA SER MODULARIZADO
#-----------------------------------------------------------------------------
    for indice, todo_texto in enumerate(reunioes):
        #reiniciar a lista de conselheiros e inserir a nova ata
        #ACHO QUE É VIAVEL FAZER USANDO UM INTERAVEL COMO NOME conteudo ao -
        #invês de usar um indice
        #todo_texto = reunioes[indice]
        conselheiros_reuniao = []
        
        print(enderecos[indice])
        
        todas_as_falas = kmp.search(todo_texto, '“')
        #procuarar por ": ", para localizar falas, indo até '”'
    
#O TRECHO A BAIXO É/DEVE SER MODULARIZADO
#-----------------------------------------------------------------------------  
        for nome in padrao:
        
            falas = kmp.search(todo_texto, nome)
            
            #verificaçao boleana, indice na lista de conselheiros
            #determina se deve ser inserido ou não um novo conselheiro na lista
            verificacao, indice_total = verifica_conselheiro(conselheiros_total, 
                                                             nome)
            if verificacao:
                conselheiros_total.append(conselheiro())
                conselheiros_total[-1].set_nome(nome)
  
            #modularizar
            if falas != []:
                
                conselheiros_reuniao.append(conselheiro())
                conselheiros_reuniao[-1].set_nome(nome)
       
                #print(nome, ": ", len(falas))
                for posicao in falas:
                    
                    j = posicao
                    
                    
                    #o padrão de disposição dos nomes na 42ª reunião é diferente
                    #dos demais, por isso vamos inserir essa regra, 
                    #para adequala
                    if (enderecos[indice] == 'Atas_Txt/42' and 
                    nome != 'Yuri Rafael de Oliveira Trovão'):
                        contagem = 0
                        while todo_texto[j+len(nome)+2] != '“':
                            j+=1
                            contagem += 1
                            if contagem >15:
                                break
                        
                
                    if(todo_texto[j+len(nome)+2] == '“'):
                        
                        #Variavel que serve de flag para o caso de citações
                        #internas
                        cita_interno = 0
                        
                        intervencao =''
                        #reiniciar a variavel para n acumular texto 
                        #Pensar em solução mais eficiente depois
                    
                        while(todo_texto[j+len(nome)+3] != '”' and 
                              cita_interno == 0 ):
                            intervencao += todo_texto[j+len(nome)+3] 
                            
                            if todo_texto[j+len(nome)+3] == '“':
                                cita_interno += 1
                                
                            if todo_texto[j+len(nome)+3] == '”':
                                cita_interno -= 1   
          
                            j+=1
                              
                            
                        conselheiros_reuniao[-1].add_fala_conselheiro(enderecos[indice], 
                                                                      intervencao.lower())
                        conselheiros_total[indice_total].add_fala_conselheiro(enderecos[indice],
                                                                              intervencao.lower())
    
                        #conseguir algum indice pra indicar qual posição adico
                        #adicionar, levando o nome em consideração 
            
            #aqui vamos juntar os dados para criar o grafico de falas ao longo
            #do tempo, frases ditas por conselheiros
        
#-----------------------------------------------------------------------------
        #migrar para processa data frame
        """
        nuvem_por_conselheiros(conselheiros_reuniao, 
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
        
        prodata.grafico_barras(df, endereco)
        prodata.grafico_barras_h(df, endereco)
        prodata.grafico_pizza(df, endereco)
        
    return conselheiros_reuniao, conselheiros_total, df, endereco"""
    return conselheiros_total
    
    
#MELHORIA:  Nesse trecho o ideal é conseguir dividir o procesamento de uma 
#           forma a conseguir recolher as falas de individuos que não os 
#           conselheiros, procurar por '“' e buscar retroativamente o padrao
#           pode ser uma solução.
#-----------------------------------------------------------------------------
#voltar pra otimizar busca
def verifica_conselheiro(conselheiros, nome):
    """escrever comentario
    #Regra inserida para verificar quando se deve inserir um novo conselheiro 
    #Retorna um boleano para que seja possivel criar um novo conselheiro se 
    #ja não foi criado um conselheiro anteriormente, caso tenha sido criado
    #retorna o valor do indice na lista para que possa ser manipulado
    #é utilizado apenas para a lista total
    #É essa regra se faz necessaria pela escolha de ordem de leitura"""
    lista_conselheiros = []
    
    if not conselheiros == []:
        for i in range(len(conselheiros)):
            if (conselheiros[i].nome_conselheiro() == nome):
                lista_conselheiros.append(True)
                conselheiro_localizado = i
            else:
                lista_conselheiros.append(False)
    else:
        return True, 0
    
    if sum(lista_conselheiros):
        return False, conselheiro_localizado
    else:
        return True, len(conselheiros)
#-----------------------------------------------------------------------------
def gera_nuvem(texto,nome,diretorio):
    """
    Função generica para criar uma nuvem de palavras 
    idealmente devemos alrerara para receber apenas um endereço ja processado
    e
    o texto com o qual deve trabalhar para gerar a nuvem.
    
    hoje recebe o endereço "picado"
    """
    stops = stopwords.words('portuguese')
    nuvem = WordCloud(background_color = 'black',
                  stopwords = stops,
                  max_words = 100, 
                  width=1600, height=800)
    nuvem.generate(texto)
    plt.imshow(nuvem)
    endereco = "Dados_por_reuniao/" + diretorio[9:] + "/" + nome + "-Nuvem de Palavras.png"
    plt.savefig( endereco, format='png')
    plt.close()
    
#-----------------------------------------------------------------------------
def nuvem_por_conselheiros(lista_conselheiros,diretorio):
    """
    Recebe uma lista com elementos da classe conselheiros para determinar se 
    devem ser geradas nuvens de palavras para esses conselheiros. 
    
    idealmente a comporação no primeiro loop deve ser alterada por um parametro
    enviada a função para q possamos ter mais usabilidades. certamente há o 
    interesse de se 
    """
    
    
    todas_palavras_faladas = ""
    for informacoes_conselheiro in lista_conselheiros:
        if informacoes_conselheiro.quantidade_falas() > 0:
            for palavras in informacoes_conselheiro.palavras_faladas():
                for palavra in palavras:
                    todas_palavras_faladas += " " + palavra
            
            gera_nuvem(todas_palavras_faladas,
                       informacoes_conselheiro.nome_conselheiro(),
                       diretorio)



    """
    https://www.youtube.com/watch?v=hSPmj7mK6ng
    https://www.youtube.com/watch?v=USTqY4gH_VM
    https://www.youtube.com/watch?v=Y5-Rmdcd6MQ
    https://www.youtube.com/c/PlotLy/videos
    https://www.youtube.com/c/CanalFlai/videos    
    """
    