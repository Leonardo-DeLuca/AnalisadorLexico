import helpers.token_type_enum as tokenTypeEnum

class Semantico:
    def __init__(self):
        self.tabela_simbolos = {
            "nome": [],
            "categoria": [],
            "tipo": [],
            "nivel": [],
        }  # Tabela para armazenar tipos de variáveis

    def executaAcaoSemantica(self, token, linha, proximoToken, lexema):
    ## Lexema é o nome para ser inserido na tabela de simbolos
    ## categoria se refere a variavel que pode ser o token ou o token anterior ao da variavel proximoToken
    ## tipo pode ser o poximo token em relação a proximoToken - (proximoToken + 1) ou (token + 2)
    ## nivel pode ser global ou interno a um escopo de COMANDO


        if token == tokenTypeEnum.TokenType.NOMEVARIAVEL.value:
            self.verificaDeclaracaoVariavel(proximoToken, linha, lexema)

    def verificaDeclaracaoVariavel(self, proximoToken, linha, lexema):
        if lexema in self.tabela_simbolos.get("nome"):
            print(f"Erro semântico: Variável '{lexema}' já declarada na linha {linha}")
            raise Exception("Erro semântico")
        else:
            # Verifica se o próximo token é ':'
            if proximoToken != 39:
                print(f"Erro semântico: Falta ':' na declaração de variável {lexema} na linha {linha}")
                raise Exception("Erro semântico")

# E5 - Quinta Etapa: Analisador Semântico
# Consiste na implementação do Analisador Semântico com sua respectiva Tabela de Símbolos.

# Tarefas:
# 1) Definir ações semânticas a serem implementadas.
# 2) Modificar a gramática da linguagem inserindo as ações semânticas definidas.
# 3) Montar um relatório explicando o que faz cada ação semântica.
# 4) Implementar as ações semânticas definidas.

# O software além de mostrar ao usuário tudo o que foi solicitado na segunda e terceira etapa deverá mostrar
# também a tabela de símbolos a cada momento em que ela for modificada.
# Quando for encontrado um erro semântico, no programa fonte, este deverá ser reportado ao usuário, informando
# o erro e a linha em que ele se encontra.

# • Um relatório contendo as ações semânticas definidas (mínimo 5), explicando o funcionamento de cada uma
# delas, a gramática com as ações semânticas incluídas. Além disso, deverá constar no relatório a estrutura da
# tabela de símbolos, que foi implementada, explicando como se insere e se retira elementos da mesma. No
# relatório deverá constar também a listagem dos erros semânticos acusados pelo compilador. Pelo menos 3 dessas
# regras devem ser implementadas junto ao analisador sintático.

# • O programa fonte, o programa executável e arquivos de exemplo (pelo menos 3).

# • Se houver mudança significativa na implementação, em relação à terceira etapa, deverá ser entregue um
# relatório explicando as mudanças que foram efetuadas justificando o porquê dessas mudanças.

# Critérios de avaliação:
# Entrega no prazo; Regras semânticas; Completude; Qualidade do código; Tratamento erros semânticos e Entrega
# dos 3 exemplos.
