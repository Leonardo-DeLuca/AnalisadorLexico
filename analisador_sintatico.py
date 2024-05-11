from helpers.tabela_parsing import tabParsing
from helpers.producoes import producoes

class Sintatico:
    def __init__(self):
        self.arrayExpansoes = []
        self.arrayEntrada = []

    def parseia(self):
        self.arrayEntrada = [2, 11, 37, 14, 38, 19, 36]
        self.arrayEntrada.append('$')

        self.arrayExpansoes[0:0] = producoes[1]
        self.arrayExpansoes.append('$')

        topoArrayExpansoes = self.arrayExpansoes[0]
        topoArrayEntrada = self.arrayEntrada[0]

        while topoArrayExpansoes != '$':
            topoArrayExpansoes = self.arrayExpansoes[0]
            topoArrayEntrada = self.arrayEntrada[0]

            if topoArrayExpansoes == 16:
                self.arrayExpansoes.pop(0)
                topoArrayExpansoes = self.arrayExpansoes[0]
            else:
                if topoArrayExpansoes <= 48 and topoArrayExpansoes >= 1:
                    if topoArrayExpansoes == topoArrayEntrada:
                        self.arrayExpansoes.pop(0)
                        self.arrayEntrada.pop(0);
                        continue
                    else:
                        print("ERRO")
                        break
                elif topoArrayExpansoes <= 80 and topoArrayExpansoes >= 49:
                    if tabParsing[topoArrayExpansoes][topoArrayEntrada] != None:
                        self.arrayExpansoes.pop(0)
                        listaProducao = producoes[tabParsing[topoArrayExpansoes][topoArrayEntrada]]
                        self.arrayExpansoes[0:0] = listaProducao
                        topoArrayExpansoes = self.arrayExpansoes[0]
                    else:
                        print("ERRO 2")
                        break

            print("ANALISE CONCLUIDA")
                        
    
sintatico = Sintatico()
sintatico.parseia()