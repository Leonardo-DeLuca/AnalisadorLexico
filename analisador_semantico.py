import helpers.token_type_enum as tokenTypeEnum

class Semantico:
    def __init__(self, arrayTokens, arrayLexemas):
        self.tabela_simbolos = {
            "nome": [],
            "categoria": [],
            "tipo": [],
            "nivel": [],
        }
        self.arrayTokens = arrayTokens
        self.arrayLexemas = arrayLexemas

    def executaAcaoSemantica(self, token, linha, proximoToken, lexema, posicaoToken):
        if token == tokenTypeEnum.TokenType.NOMEVARIAVEL.value:
            if proximoToken == 39 or proximoToken == 41 or proximoToken == 44:
                self.insereTabelaSimbolos(lexema, 0, linha, posicaoToken)

        # Verificação de tipos em operações
        if self.isOperador(token):
            operando1 = self.arrayLexemas[posicaoToken - 1]
            operando2 = self.arrayLexemas[posicaoToken + 1]

            tipo1 = self.buscaTipoOperando(operando1)
            tipo2 = self.buscaTipoOperando(operando2)

            operandoNaoInicializado = None

            if tipo1 is None:
                operandoNaoInicializado = operando1
            elif tipo2 is None:
                operandoNaoInicializado = operando2

            if operandoNaoInicializado is not None:
                print(f"Erro semantico: Variavel nao inicializada: {operandoNaoInicializado} na linha {linha}")
                raise Exception("Erro semantico")

            self.verificaCompatibilidadeTipos(tipo1, tipo2, operando1, operando2, linha)

        if self.isCinCout(token):
            tokenCinCout = self.arrayLexemas[posicaoToken + 1]

            tipoToken = self.buscaTipoOperando(tokenCinCout)

            if tipoToken is None and tokenCinCout != "literal":
                print(f"Erro semantico: Variavel nao inicializada: {tokenCinCout} na linha {linha}")
                raise Exception("Erro semantico")

    def insereTabelaSimbolos(self, nome, nivel, linha, posicaoToken):
        self.verificaDuplicidadeVariaveis(nome, linha)

        categoria = self.buscaCategoriaNomeVariavel(posicaoToken)
        tipo = self.buscaTipoVariavel(posicaoToken, categoria)

        self.tabela_simbolos.get("nome").append(nome)
        self.tabela_simbolos.get("categoria").append(categoria)
        self.tabela_simbolos.get("tipo").append(tipo)
        self.tabela_simbolos.get("nivel").append(nivel)

    def isOperador(self, token):
        return token in ["+", "-", "*", "/", "=="]
    
    def isCinCout(self, token):
        return token in ["<<", ">>"]

    def buscaTipoVariavel(self, posicaoToken, categoria):
        tipo = None
        tipos = ["string", "integer", "float", "char"]

        if categoria == "variavel":
            ## For para pegar variáveis declaradas múltiplas vezes com ,
            for i in range(posicaoToken, len(self.arrayTokens) - 1):
                proximoToken = self.arrayTokens[i + 1]

                if self.arrayTokens[i] == ":" and proximoToken in tipos:
                    tipo = proximoToken
                    break

        elif categoria == "funcao":
            tokenAnterior = self.arrayTokens[posicaoToken - 1]

            if tokenAnterior in tipos:
                tipo = tokenAnterior

        return tipo

    def buscaCategoriaNomeVariavel(self, posicaoToken):
        categoria = None
        tipos = ["string", "integer", "float", "char"]

        ## Antes de entrar na ação semântica, já foi verificado que o programa está correto sintaticamente.
        ## Por isso, tomei a liberdade de acessar diretamente o token anterior
        tokenAnterior = self.arrayTokens[posicaoToken - 1]

        if tokenAnterior in tipos:
            categoria = "funcao"
        else:
            categoria = "variavel"
        return categoria

    def buscaTipoOperando(self, operando):
        if operando in self.tabela_simbolos.get("nome"):
            indice = self.tabela_simbolos.get("nome").index(operando)
            return self.tabela_simbolos.get("tipo")[indice]
        elif operando.isdigit():
            return "integer"
        elif operando.replace(".", "", 1).isdigit():
            return "float"
        else:
            if operando.startswith('"') and operando.endswith('"'):
                return "string"
            elif operando.startswith("'") and operando.endswith("'"):
                return "char"
            elif operando.startswith("`") and operando.endswith("`"):
                return "literal"
            else:
                return None

    def printaTabelaSimbolos(self):
        nomes = self.tabela_simbolos.get("nome")
        categorias = self.tabela_simbolos.get("categoria")
        tipos = self.tabela_simbolos.get("tipo")
        niveis = self.tabela_simbolos.get("nivel")
        
        print()
        print(f"{'Nome':<20}{'Categoria':<20}{'Tipo':<20}{'Nível':<20}")
        print("="*65)
        for nome, categoria, tipo, nivel in zip(nomes, categorias, tipos, niveis):
            print(f"{nome:<20}{categoria:<20}{tipo:<20}{nivel:<20}")

    ##### ERROS SEMANTICOS #####

    def verificaDuplicidadeVariaveis(self, nome, linha):
        if nome in self.tabela_simbolos.get("nome"):
            print(f"Erro semantico: Variavel ou funcao '{nome}' ja declarada na linha {linha}")
            raise Exception("Erro semantico")

    def verificaCompatibilidadeTipos(self, tipo1, tipo2, operando1, operando2, linha):
        tipos_compativeis = {
            "integer": ["integer", "float"],
            "float": ["integer", "float"],
            "string": ["string"],
            "char": ["char"],
        }

        if (
            tipo1 not in tipos_compativeis
            or tipo2 not in tipos_compativeis[tipo1]
        ):
            print(f"Erro semantico: Tipos incompatíveis entre: {operando1}({tipo1}) e {operando2}({tipo2}) na linha {linha}")
            raise Exception("Erro semantico")
