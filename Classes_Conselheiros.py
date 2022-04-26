# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 14:12:55 2020

@author: neres

Tentativa um de criar uma Bilioteca com classes utilizadas para gerenciar as
falas ditas durantes as reuniões do COPAM, a pricipio, analizando as reuniões 
da CMI 

"""


##import nltk
"""
necessario para funcionamento correto e atualizado da biblioteca nltk, 
verificar no git da biblioteca como fazer pelo prompt e automatizar verificação de atualizações
nltk.download()
"""

#Bibliotecas inseridas para facilitar o trabalho de limpesa de stopwords e 
#pontuação, bem como possivelmente utilizar outras funções e da biblioteca 
#string
from nltk.corpus import stopwords
import string

#inseirda como variavel "universal" pq não era localizada como atributo dentro
#da classe falas como um atributo
stops = stopwords.words('portuguese')

class falas(object):
    

    """ tem como objetivo armazenar as falas ditas tanto por conselheiros
    (individualmente) como as gerais proferidas pela plateia. Armazena também
    algumas metricas, numero de palavras e caracteres falados 
    
    Deve ser encaminhada uma lista com ao menos uma fala proferida na reunião 
    ou por um dos conselheiros se esta for uma fala atribuida a ela"""
    
    def __init__(self, intervencoes=""):
        """Não necessecita de parametros iniciais"""
        self.intervencoes = []
        self.caracteres = 0
        self.palavras = []
        self.numero_de_palavras = 0
    
    
#--------------------------------------------------------------------------
#Bloco de operações basicas da Classe fala usados para encapsular os atributos
#internos da classe 
    def caracter_falados(self):
        return self.caracteres
    
    def quantidade_palavras(self):
        return self.numero_de_palavras
    
    def quantidade_falas(self):
        return len( self.intervencoes)

    def palavras_faladas(self):
        return self.palavras   
    
    def todas_falas(self):
        return self.intervencoes
    
    
     
#--------------------------------------------------------------------------
#Bloco de operações
    #NECESSARIO CHECAR A NECESSIDADE DE SE VERIFICAR CASOS DE LISTAS VAZIAS
    def add_fala(self, nova_intervencao):
        """adinciona a nova fala e atualiza os valores dos demais atributos
        deve ser encaminhada uma strig para ser adicionada a lista de falas"""
        self.intervencoes.append(nova_intervencao)
        self.caracteres += len(nova_intervencao)
      
        #intervalo responsavel por "limpar" a fala adicionando apenas palavras
        #dentro da lista removendo pontuações e palavras sem valor semántico 
        palavras_dividida = nova_intervencao.split()
        palavras_semstop = [p for p in palavras_dividida if p not in stops]
        self.palavras.append( [p for p in palavras_semstop if p not in string.punctuation] )
        
        for i in self.palavras:
            self.numero_de_palavras += len(i)
    
    
    #def __str__(self):
    #   return "Title:%s , author:%s, pages:%s " %(self.title, self.author, self.pages)

    #def __len__(self):
    #   return self.pages

    #def __del__(self):
#==============================================================================
       
class conselheiro(falas):
    """ tem como objetivo armazenar as informações referentes a ações tomadas
    pelos conselheiros. suas falas, seus votos e solicitações de vistas.
    
    a principio para sua criação deve ser encaminhada o nome do coselheiro, as
    demais caracteristicas serão inseridas a medida em que o documento é lido"""
    
    def __init__(self, nome=""):
        """Não necessecita de parametros iniciais"""
        self.nome = ""
        self.entidade = ""
        self.votos = []
        self.fala_por_reuniao = []
        super().__init__()
        """" 
        UMA MELHORIA NA ESTRUTURA DA CLASSE PODE SER FEITA AO INSERIR TODAS AS
        FALAS DOS COSNSELHEIROS DENTRO DE FALAS POR REUNIÃO DE FORMA QUE SEJA
        MAIS FACIL COLETAR INFORMAÇÕES INDIVIDUAIS.
        """
#--------------------------------------------------------------------------
#Bloco de operações basicas da Classe conselheiro usados para encapsular os 
#atributos internos da classe 
    def nome_conselheiro(self):
        return self.nome
    
    def entidade_conselheiro(self):
        return self.entidade
    
    def votos_conselheiro(self):
        return self.votos

#--------------------------------------------------------------------------
#Bloco de operações
    #NECESSARIO CHECAR OS TIPOS DE DADOS INSERIDOS COMO PRECAUSSÃO
    #INSERIR DEPOIS
    def set_nome(self, nome):
        self.nome = nome
        
    def set_entidade(self, entidade):
        self.entidade = entidade
    
    def add_voto(self, voto):
        self.votos.append(voto)
    
    def add_fala_conselheiro(self, endereco, nova_intervencao):
        """
        endereco enviado corresponde ao nome da ata, usaremos de refêrencia 
        para saber a quantidade de falas feitas por reunião 
        
        nova_intervencao é a nova fala a ser adicionada.
        
        essa função executa a chamada da função responsavel por adioconar
        efetivamente a nova fala, além de contabilizar as variaveis relativas
        especificamente a classe conselheiro
        """
        if self.fala_por_reuniao == []: #or fala_por_reunião[-1][0] != endereco[-2]:
            self.fala_por_reuniao.append([endereco[-2:], 1])
            self.add_fala(nova_intervencao)
        elif endereco[-2:] == self.fala_por_reuniao[-1][0]:
            self.fala_por_reuniao[-1][1] += 1
            self.add_fala(nova_intervencao)
        else:
            self.fala_por_reuniao.append([endereco[-2:], 1])
            self.add_fala(nova_intervencao)
    
    def intervencoes_feitas(self):
        resultado = []
        for i in self.fala_por_reuniao:
            resultado.append(i[1])
        
        return resultado
    
    def reuniao_interviu(self):
        resultado = []
        for i in self.fala_por_reuniao:
            resultado.append(i[0])
        
        return resultado
            
#==============================================================================
class reuniao(falas):
    def __init__(self, numero= ""):
        self.numero = ""
        self.conselheiros_presentes = []
        self.processos_em_pauta = []
            #melhorar futuramente a descrição do processo, nome e caracteristicas
        self.processos_votados = []
            #inserir futuramente uma atributo para verificar PUs favoraveis
        super().__init__()

#--------------------------------------------------------------------------
#Bloco de operações basicas da Classe Reunião usados para encapsular os 
#atributos internos da classe 
        
        def reuniao_numero():
            return self.numero
        
        def listar_conselheiros():
            return self.conselheiros_presentes
        
        def listar_processos():
            return self.processos_em_pauta
        
        def listar_resultados():
            return self.processos_votados
        
        def total_falas():
            armazena_n_falas = 0
            for p in range(len(self.conselheiros_presentes)):
                armazena_n_falas += self.conselhereiros_presentes[p].quantidade_falas()
            
            return len(self.intervencoes) + armazena_n_falas 
#total de falas é quantidade_falas + conselheiros_presentes[i].quantidade_falas
#[p for p in palavras_dividida if p not in stops]   
#melhorar esse aspecto no futuro sera possivel ao armazenar a quantidade total 
#de falas sem a necessidade de acessar os valores atraves dos conselheiros
     
#--------------------------------------------------------------------------
#Bloco de operações
        def set_numero(self, numero):
            self.numero = numero
            
        def add_conselheiro(self, conselheiro):
            self.conselheiros_presentes.append(conselheiro)
            
        def add_processo(self, processo):
            self.processos_em_pauta.append(processo)
        
        def processos_votados(self, procresso):
            self.processos_votados.append(processo)


        
        
        
        
        
        
        
        