# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 18:33:05 2020

@author: neres
"""


import nltk
import string
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import plotly.graph_objects as go



"""
necessario para funcionamento correto e atualizado da biblioteca nltk, 
#verificar no git da biblioteca como fazer pelo prompt e automatizar 
verificação de atualizações nltk.download()
"""
from Classes_Conselheiros import conselheiro

#-----------------------------------------------------------------------------
def salva_data_csv(df,endereco):
    df.to_csv(endereco + '.csv')

#-----------------------------------------------------------------------------
def salva_data_xlsx(df,endereco):
    df.to_excel(endereco + '.xlsx')
#-----------------------------------------------------------------------------
def verifica_falas_para_graph(df,endereco):
    return 0
#-----------------------------------------------------------------------------
def grafico_linha(conselheiros,endereco):
    """
    Optamos por considerar apenas os falantes para ser apresentados nos 
    graficos de linhas. Dentro dessa ideia, a chamada dessa função só faz 
    sentido considerando ao menos duas reuniões devos tentar implementar algo
    nesse sentido.
    """
    
    #TALVEZ TRABALHAR COM UMA MATRIZ CRIADA A PARTIR DOS DADOS JÁ NA CLASSE
    #VERIFICAR E IR PREENCHENDO, PROVALVEMENTE A FUNÇÃO QUE EXECUTADA ISSO DEVE
    #ESTAR DENTRO DE PROCESSAMENTO DE ENTRADA? NÃO SEI AO CERTO
    return 0
    
    


#-----------------------------------------------------------------------------
def grafico_barras_h(df,endereco):
    
    palavras = df[['Numero de Falas']].apply(pd.to_numeric)
    palavras['Nome'] = df['Nome']
    palavras = palavras.sort_values('Numero de Falas')
    
    
    plt.barh(palavras['Nome'],palavras['Numero de Falas'])
    
    plt.title("Falas por conselheiro da " + endereco[-10:] + " da CMI")

    #tentando fazer com que a figura seja salva com todas as infos
    plt.tight_layout()
    
    #limpando o pyplot, verificar qual metodo utilizar
    plt.savefig( endereco+'_barras_h', format='pdf')
    
    plt.cla()   
    plt.clf()
    plt.close()
    
    
#-----------------------------------------------------------------------------
def grafico_barras(df, endereco):
    
    palavras = df[['Numero de Falas']].apply(pd.to_numeric)
    palavras['Nome'] = df['Nome']
    palavras = palavras.sort_values('Numero de Falas')
    
    
    y_pos = range(len(palavras['Nome']))
    plt.bar(y_pos, palavras['Numero de Falas'])
    # Rotation of the bars names
    plt.xticks(y_pos, palavras['Nome'], rotation=90)
    
    plt.title("Falas por conselheiro da " + endereco[-10:] + " da CMI")
    
    #tentando fazer com que a figura seja salva com todas as infos
    plt.tight_layout()
    
    plt.savefig( endereco+'_barras', format='pdf')
    
    #limpando o pyplot, verificar qual metodo utilizar
    plt.cla()   
    plt.clf()
    plt.close()
    
def grafico_pizza(df, endereco):

    # Aqui criamos a área que plotamos o gráfico e definimos seu tamanho
    fig, ax = plt.subplots(figsize=(18, 18), subplot_kw=dict(aspect="equal"))


    palavras = df[['Numero de Falas']].apply(pd.to_numeric)
    palavras['Nome'] = df['Nome']
    palavras = palavras.sort_values('Numero de Falas')
    

    # Aqui serão colocados os kg e as porcentagens no gráfico
    def func(pct, allvals):
        # calc %
        absolute = int(pct/100.*np.sum(allvals))
        # fazendo legenda do gráfico com % e kg
        return "{:.1f}%".format(pct)

    # Criando o gráfico e colocando a função da legenda interna
    wedges, texts, autotexts = ax.pie( palavras['Numero de Falas'], 
                    autopct = lambda pct: func(pct, palavras['Numero de Falas']),
                                                textprops=dict(color="w"))

    # Definindo a caixa de legenda externa, título, localização e onde vai 'ancorar o box'
    ax.legend(wedges, palavras['Nome'],
          title="Conselheiros",
          loc="center left",
          prop={'size': 22},
          bbox_to_anchor=(1, 0, 0.5, 1))

    # Aqui definimos o tamanho do texto de dentro do gráfico, e o peso da fonte como bold
    plt.setp(autotexts, size=14, weight="bold")

    # Título do gráfico
    ax.set_title("Porcenagem de falas dos conselheiros em uma reunião", 
             fontsize=30,
             horizontalalignment = 'center')

    plt.tight_layout()

    #salvando o gráfico
    plt.savefig( endereco+'_pizza', format='pdf')
    
    #limpando o pyplot, verificar qual metodo utilizar
    plt.cla()   
    plt.clf()
    plt.close()
 #-----------------------------------------------------------------------------
#   Esta é uma gambiarra safada, Implementar isso de uma forma mais 
#   eficiente no futuro   
def falas_no_ano(conselheiros):
    
    reuniao_array = np.arange(41,55)
    
    for conselheiro in conselheiros:
        if(conselheiro.quantidade_falas() > 3):
        
            reuniao_falas = []
            for i, valor in enumerate(reuniao_array):
                reuniao_falas.append(0)
    
            for indice_c, reuniao in enumerate(conselheiro.reuniao_interviu()):
                for indice, posicao in enumerate(reuniao_array): 
                    #esse loop poderia ser subistituido por um while? 
                    if int(reuniao) == posicao:
                        reuniao_falas[indice] = conselheiro.intervencoes_feitas()[indice_c]
                        break
            
            #x = reuniao_array
            #y = reuniao_falas            
            grafico_linhas(conselheiro, reuniao_array, reuniao_falas)
            
            grafico_linhas_acumulado(conselheiro, reuniao_array, reuniao_falas)
            #reuniao_interviu
            """
            plt.plot(x, y, label = "linear")
        
            plt.savefig(conselheiro.nome_conselheiro()+" falas ao longo do ano")
        
            plt.cla()   
            plt.clf()
            plt.close()"""
            
#-----------------------------------------------------------------------------
def grafico_linhas(conselheiro, x, y):
    
    plt.plot(x, y, label = conselheiro.nome_conselheiro(), 
             marker = "8", markersize = 5, markeredgecolor = "red")

    plt.title("Evolução das falas ao longo do ano")
    plt.xlabel("reuniões do ano de 2019")
    plt.ylabel("Numero de falas ao longo do ano")
    plt.grid(True)
    
    endereco = "Dados_acumulados/Falas_ao_longo_do_ano/"
    plt.savefig(endereco + conselheiro.nome_conselheiro() + " falas ao longo do ano")
    
    plt.cla()   
    plt.clf()
    plt.close()
    
#-----------------------------------------------------------------------------    
def grafico_linhas_acumulado(conselheiro, x, y):
#   O ideal seria talvez utilizar o grafico de linhas pra n reescrever codigo
#   igual, mas aqui seriam necessarias pelo menos duas alterações
#   *A primeira referente aos salvamentos, seria necessario criar uma função 
#       isso salvando e fechado o plot
#   *A segunda referente ao envio de enderecos que deve "subir de nível"
    for posicao, valor in enumerate(y): 
        if posicao != 0:
            y[posicao] = y[posicao - 1] + y[posicao] 
    
    plt.plot(x, y, label = conselheiro.nome_conselheiro(), 
             marker = "8", markersize = 5, markeredgecolor = "red")
    
    plt.title("Evolução das falas ao longo do ano (Acumulado)")
    plt.xlabel("reuniões do ano de 2019")
    plt.ylabel("Numero de falas ao longo do ano")
    plt.grid(True)
    
    endereco = "Dados_acumulados/Falas_ao_longo_do_ano_acumuladas/"
    plt.savefig(endereco + conselheiro.nome_conselheiro() + " falas ao longo do ano")
    
    plt.cla()   
    plt.clf()
    plt.close()
    
#-----------------------------------------------------------------------------
def cria_data(conselheiros_nomeados):
    data = []
    for conselheiros in conselheiros_nomeados:
        lista = []
        lista.append(conselheiros.nome_conselheiro())
        lista.append(conselheiros.quantidade_falas())
        lista.append(conselheiros.quantidade_palavras())
        lista.append(conselheiros.caracter_falados())
    
        if(conselheiros.quantidade_falas() > 0):
            lista.append(conselheiros.caracter_falados()/
                         conselheiros.quantidade_falas())
    
            lista.append(conselheiros.quantidade_palavras()/
                         conselheiros.quantidade_falas())
        else:
            lista.append(0)
            lista.append(0)
    
    
        data.append(lista)
    
    
    datapy = np.array(data)
    
    df = pd.DataFrame(datapy, columns=['Nome', 'Numero de Falas', 
                                       'Numero de Palavras Faladas',
                                       'Numero de Caracteres Falados',
                                       'Media de Caracteres por Fala',
                                       'Media de Palavras por Fala'])
    
    return df


#Linhas se mantem até que eu efetivamente consiga selecionar o que vai ser
#printado ou transformado em graficos usando os dados dos dataframes gerados
#-----------------------------------------------------------------------------
def cria_data_falantes(conselheiros_nomeados):
    data = []
    for conselheiros in conselheiros_nomeados:
        if(conselheiros.quantidade_falas() > 1):
            lista = []
            lista.append(conselheiros.nome_conselheiro())
            lista.append(conselheiros.quantidade_falas())
            lista.append(conselheiros.quantidade_palavras())
            lista.append(conselheiros.caracter_falados())
            
            lista.append(conselheiros.caracter_falados()/
                 conselheiros.quantidade_falas())
    
            lista.append(conselheiros.quantidade_palavras()/
                 conselheiros.quantidade_falas())
           
            data.append(lista)
    
    
    datapy = np.array(data)
    
    df = pd.DataFrame(datapy, columns=['Nome', 'Numero de Falas', 
                                       'Numero de Palavras Faladas',
                                       'Numero de Caracteres Falados',
                                       'Media de Caracteres por Fala',
                                       'Media de Palavras por Fala'])
    
    return df

#-----------------------------------------------------------------------------
def gera_matriz_falantes(conselheiros_nomeados):
    data = []
    #transformar em dicionario e implementar depois 
    reunioes = ['41', '42', '43', '44', '45', '46', '47', '48', '49', '50', 
                '51', '52', '53', '54']
    for conselheiro in conselheiros_nomeados:
        if conselheiro.quantidade_falas() > 1:
            lista = []
            

#-----------------------------------------------------------------------------
def teste():
    x = np.arange(15)
    y = x**2
    
    plt.plot(x, y, label = "quadratica", marker = "8", markersize = 7, mec = "red", mfc = "red")
    plt.plot(x, x, label = "linear", marker = "8", markersize = 7, mec = "red", mfc = "red")
    plt.show()
    
#-----------------------------------------------------------------------------   
def teste_2(conselheiros):
    legenda = []
    
    reuniao_array = np.arange(41,55)
    
    #mudar nome do interavel
    for conselheiro in conselheiros:
        if(conselheiro.quantidade_falas() > 40):
        
            #inicializa o vetor reunião falas considerando q se presente o 
            #conselheiro pode n ter falado na reunião, por isso inserimos 0
            reuniao_falas = []
            for i, valor in enumerate(reuniao_array):
                reuniao_falas.append(0)
    
            
            #Aqui a verificação é feita em relação as reuniões em que o conse-
            #lheiro efetivamente falou/participou com relação a todas as
            #reuniões possiveis
            for indice_c, reuniao in enumerate(conselheiro.reuniao_interviu()):
                for indice, posicao in enumerate(reuniao_array): 
                    #esse loop poderia ser subistituido por um while? 
                    if int(reuniao) == posicao:
                        reuniao_falas[indice] = conselheiro.intervencoes_feitas()[indice_c]
                        break
            
            
            x = reuniao_array
            y = reuniao_falas 
            
            for posicao, valor in enumerate(y): 
                if posicao != 0:
                    y[posicao] = y[posicao - 1] + y[posicao] 
    
            plt.plot(x, y, label = conselheiro.nome_conselheiro(),
                     marker = "8", markersize = 3, 
                     mfc = "w")
            
    plt.legend()
    plt.title("Falas ao longo do ano (Acumulado)")
    plt.xlabel("reuniões do ano de 2019")
    plt.ylabel("Numero de falas ao longo do ano")
    plt.grid(True, c="gainsboro")
    plt.show()
                    
#-----------------------------------------------------------------------------    
def teste_3(conselheiros):
    legenda = []
    
    reuniao_array = np.arange(41,55)
    
    #mudar nome do interavel
    for conselheiro in conselheiros:
        if(conselheiro.quantidade_falas() > 40):
        
            #inicializa o vetor reunião falas considerando q se presente o 
            #conselheiro pode n ter falado na reunião, por isso inserimos 0
            reuniao_falas = []
            for i, valor in enumerate(reuniao_array):
                reuniao_falas.append(0)
    
            
            #Aqui a verificação é feita em relação as reuniões em que o conse-
            #lheiro efetivamente falou/participou com relação a todas as
            #reuniões possiveis
            for indice_c, reuniao in enumerate(conselheiro.reuniao_interviu()):
                for indice, posicao in enumerate(reuniao_array): 
                    #esse loop poderia ser subistituido por um while? 
                    if int(reuniao) == posicao:
                        reuniao_falas[indice] = conselheiro.intervencoes_feitas()[indice_c]
                        break
            
            
            x = reuniao_array
            y = reuniao_falas 
    
            plt.plot(x, y, label = conselheiro.nome_conselheiro(),
                     marker = "8", markersize = 3, 
                     mfc = "w")
            
    plt.legend()
    plt.title("Falas ao longo do ano (Acumulado)")
    plt.xlabel("reuniões do ano de 2019")
    plt.ylabel("Numero de falas ao longo do ano")
    plt.grid(True, c="gainsboro")
    plt.show()
#-----------------------------------------------------------------------------  
def salva_fecha_plot(endereco):
    plt.savefig(endereco)
    plt.cla()   
    plt.clf()
    plt.close()
                    
                    
                    
            
    