from helpers.tabela_parsing import tabParsing
from helpers.producoes import producoes

class Sintatico:
    def __init__(self):
        self.arrayExpansoes = []
        self.arrayEntrada = []
        self.arrayLinhas = []
        self.arrayTokens = []
        self.elementoAnalisando = 0
        self.erro = False

    def montaArrayEntrada(self):
        arrayLexico = []
        
        with open("resp_lexico.txt", "r") as arquivo:
            linha = arquivo.readline()

            while (linha):
                tokensLinhas = linha.strip().split("#")
                self.arrayEntrada.append(int(tokensLinhas[0]))
                self.arrayLinhas.append(tokensLinhas[1])
                self.arrayTokens.append(tokensLinhas[2])
                linha = arquivo.readline()

        return arrayLexico

    def parseia(self):
        self.montaArrayEntrada()
        self.arrayEntrada.append('$')

        self.arrayExpansoes[0:0] = producoes[1]
        self.arrayExpansoes.append('$')

        topoArrayExpansoes = self.arrayExpansoes[0]
        topoArrayEntrada = self.arrayEntrada[0]

        while topoArrayExpansoes != '$':
            print("Elemento da entrada sendo analisado: " + str(self.arrayEntrada[0]) + " | Token: " + str(self.arrayTokens[self.elementoAnalisando]) + " | Linha: " + str(self.arrayLinhas[self.elementoAnalisando]))
            print("Pilha: " + str(self.arrayExpansoes))

            if topoArrayExpansoes == 16:
                self.arrayExpansoes.pop(0)
                topoArrayExpansoes = self.arrayExpansoes[0]
            else:   
                if topoArrayExpansoes <= 48 and topoArrayExpansoes >= 1:
                    if topoArrayExpansoes == topoArrayEntrada:
                        self.arrayExpansoes.pop(0)
                        self.arrayEntrada.pop(0);
                        self.elementoAnalisando = self.elementoAnalisando + 1
                        topoArrayExpansoes = self.arrayExpansoes[0]
                        topoArrayEntrada = self.arrayEntrada[0]
                        continue
                    else:
                        print("Erro sintatico (T) na linha " + self.arrayLinhas[self.elementoAnalisando])
                        print("Elemento da entrada do erro: " + str(self.arrayEntrada[0]))
                        print("Token do erro: " + str(self.arrayTokens[self.elementoAnalisando]))
                        self.erro = True
                        break
                elif topoArrayExpansoes <= 80 and topoArrayExpansoes >= 49:
                    if tabParsing[topoArrayExpansoes][topoArrayEntrada] != None:
                        self.arrayExpansoes.pop(0)
                        listaProducao = producoes[tabParsing[topoArrayExpansoes][topoArrayEntrada]]
                        self.arrayExpansoes[0:0] = listaProducao
                        topoArrayExpansoes = self.arrayExpansoes[0]
                    else:
                        print("Erro sintatico (NT) na linha " + self.arrayLinhas[self.elementoAnalisando])
                        print("Elemento da entrada do erro: " + str(self.arrayEntrada[0]))
                        print("Token do erro: " + str(self.arrayTokens[self.elementoAnalisando]))
                        self.erro = True
                        break

        if self.erro != True:
            print("Pilha: " + str(self.arrayExpansoes))
            print("Analise sintatica concluida com sucesso!")
                        
    
sintatico = Sintatico()
sintatico.parseia()