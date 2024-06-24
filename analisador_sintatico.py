from helpers.tabela_parsing import tabParsing
from helpers.producoes import producoes
import analisador_semantico as analisadorSemantico

class Sintatico:
    def __init__(self):
        self.arrayExpansoes = []
        self.arrayEntrada = []
        self.arrayLinhas = []
        self.arrayTokens = []
        self.arrayLexemas = []
        self.elementoAnalisando = 0
        self.erro = False

    def montaArrayEntrada(self):
        with open("resp_lexico.txt", "r") as arquivo:
            for linha in arquivo:
                tokensLinhas = linha.strip().split("#")
                self.arrayEntrada.append(int(tokensLinhas[0]))
                self.arrayLinhas.append(tokensLinhas[1])
                self.arrayTokens.append(tokensLinhas[2])
                self.arrayLexemas.append(tokensLinhas[3])

    def parseia(self):
        print("Comecando analise sintatica...\n")

        self.analise_semantica = analisadorSemantico.Semantico(self.arrayTokens, self.arrayLexemas)

        self.montaArrayEntrada()
        self.arrayEntrada.append('$')

        self.arrayExpansoes[0:0] = producoes[1]
        self.arrayExpansoes.append('$')

        topoArrayExpansoes = self.arrayExpansoes[0]
        topoArrayEntrada = self.arrayEntrada[0]

        while topoArrayExpansoes != '$':
            print(
                "Elemento da entrada sendo analisado: " + str(self.arrayEntrada[0]) 
                + " | Token: " + str(self.arrayTokens[self.elementoAnalisando]) 
                + " | Linha: " + str(self.arrayLinhas[self.elementoAnalisando])
                )
            print("Pilha: " + str(self.arrayExpansoes))
            if topoArrayExpansoes == 16:
                self.arrayExpansoes.pop(0)
                topoArrayExpansoes = self.arrayExpansoes[0]
            else:   
                if topoArrayExpansoes <= 48 and topoArrayExpansoes >= 1:
                    if topoArrayExpansoes == topoArrayEntrada:
                        self.arrayExpansoes.pop(0)
                        self.arrayEntrada.pop(0)

                        token = self.arrayTokens[self.elementoAnalisando]
                        linha = self.arrayLinhas[self.elementoAnalisando]
                        proximoToken = self.arrayEntrada[0]
                        lexema = self.arrayLexemas[self.elementoAnalisando]

                        self.analise_semantica.executaAcaoSemantica(token, linha, proximoToken, lexema, self.elementoAnalisando)

                        self.elementoAnalisando += 1
                        topoArrayExpansoes = self.arrayExpansoes[0]
                        topoArrayEntrada = self.arrayEntrada[0]
                        continue
                    else:
                        print("Erro sintatico (T) na linha " + self.arrayLinhas[self.elementoAnalisando])
                        print("Elemento da entrada do erro: " + str(self.arrayEntrada[0]))
                        print("Token do erro: " + str(self.arrayTokens[self.elementoAnalisando]))
                        self.erro = True
                        break
                elif 49 <= topoArrayExpansoes <= 80:
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

        if not self.erro:
            print("Pilha: " + str(self.arrayExpansoes))
            print("Analise sintatica concluida com sucesso!")