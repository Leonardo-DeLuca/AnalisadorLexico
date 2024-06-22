import helpers.token_type_enum as tokenTypeEnum

class Semantico:
    def __init__(self, arrayTokens):
        self.tabela_simbolos = {
            "nome": [],
            "categoria": [],
            "tipo": [],
            "nivel": [],
        }
        self.arrayTokens = arrayTokens

    ## Lexema é o nome para ser inserido na tabela de simbolos
    ## categoria se refere a variavel que pode ser o token ou o token anterior ao da variavel proximoToken
    ## tipo pode ser o poximo token em relação a proximoToken - (proximoToken + 1) ou (token + 2)
    ## nivel pode ser global ou interno a um escopo de COMANDO
    def executaAcaoSemantica(self, token, linha, proximoToken, lexema, posicaoToken):
        if token == tokenTypeEnum.TokenType.NOMEVARIAVEL.value:
            if proximoToken == 39 or proximoToken == 41 or proximoToken == 44:
                self.insereTabelaSimbolos(lexema, "variavel", 0, linha, posicaoToken)
            
    def insereTabelaSimbolos(self, nome, categoria, nivel, linha, posicaoToken):
        if nome in self.tabela_simbolos.get("nome"):
            print(f"Erro semantico: Variavel ou funcao '{nome}' ja declarada na linha {linha}")
            raise Exception("Erro semantico")
        
        categoria = self.buscaCategoriaNomeVariavel(posicaoToken)
        tipo = self.buscaTipoVariavel(posicaoToken, categoria)
        
        self.tabela_simbolos.get("nome").append(nome)
        self.tabela_simbolos.get("categoria").append(categoria)
        self.tabela_simbolos.get("tipo").append(tipo)
        self.tabela_simbolos.get("nivel").append(nivel)

    def buscaTipoVariavel(self, posicaoToken, categoria):
        tipo = None
        tipos = ['string', 'integer', 'float', 'char']

        if categoria == 'variavel':
            ## For para pegar variáveis declaradas múltiplas vezes com ,
            for i in range(posicaoToken, len(self.arrayTokens) - 1):
                proximoToken = self.arrayTokens[i + 1]

                if self.arrayTokens[i] == ":" and proximoToken in tipos:
                    tipo = proximoToken
                    break

        elif categoria == 'funcao':
            tokenAnterior = self.arrayTokens[posicaoToken - 1]
            
            if tokenAnterior in tipos:
                tipo = tokenAnterior

        return tipo
    
    def buscaCategoriaNomeVariavel(self, posicaoToken):
        categoria = None
        tipos = ['string', 'integer', 'float', 'char']

        ## Antes de entrar na ação semântica, já foi verificado que o programa está correto sintaticamente.
        ## Por isso, tomei a liberdade de acessar diretamente o token anterior
        tokenAnterior = self.arrayTokens[posicaoToken - 1]

        if tokenAnterior in tipos:
            categoria = "funcao"
        else:
            categoria = "variavel"

        return categoria
        
    def printaTabelaSimbolos(self):
        print(self.tabela_simbolos.get("nome"))
        print(self.tabela_simbolos.get("categoria"))
        print(self.tabela_simbolos.get("tipo"))
        print(self.tabela_simbolos.get("nivel"))