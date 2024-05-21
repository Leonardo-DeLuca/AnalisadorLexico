import analisador_lexico as analisadorLexico
import analisador_sintatico as analisadorSintatico

class Index:
    def __init__(self):
        pass
    
    def analisa(self):
        ## Trocar pelo arquivo desejado:
        arquivo = 'tests/palavras.txt'

        analisadorLexico.parseia(arquivo)
        
        sintatico = analisadorSintatico.Sintatico()
        ## Sintatico sempre analisa o arquivo resp_lexico.txt
        sintatico.parseia()

index = Index()
index.analisa()