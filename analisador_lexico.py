import re

def carregar_dicionario():
    return {
        "while": "1",
        "void": "2",
        "string": "3",
        "return": "4",
        "numerointeiro": "5",
        "numerofloat": "6",
        "nomevariavel": "7",
        "nomedochar": "8",
        "nomedastring": "10",
        "main": "11",
        "literal": "12",
        "integer": "13",
        "inicio": "14",
        "if": "15",
        "î": "16",
        "for": "17",
        "float": "18",
        "fim": "19",
        "else": "20",
        "do": "21",
        "cout": "22",
        "cin": "23",
        "char": "24",
        "callfuncao": "25",
        ">>": "26",
        ">=": "27",
        ">": "28",
        "==": "29",
        "=": "30",
        "<=": "31",
        "<<": "32",
        "<": "33",
        "++": "34",
        "+": "35",
        "}": "36",
        "{": "37",
        ";": "38",
        ":": "39",
        "/": "40",
        ",": "41",
        "*": "42",
        ")": "43",
        "(": "44",
        "$": "45",
        "!=": "46",
        "--": "47",
        "-": "48",
    }


def analisar_arquivo(nome_arquivo, dicionario):
    simbolos = {"{", ";", "}", "(", ")", ":"}
    
    tokens = []
    lexemas = []
    linhas = []

    with open(nome_arquivo, "r") as file:
        linhas_do_arquivo = file.read().splitlines()

        comentarioBloco = False

        for linha_atual, linha in enumerate(linhas_do_arquivo, start=1):
            lexema = ""
            dentroString = False
            dentroLiteral = False
            comentarioLinha = False

            for index, char in enumerate(linha):
                if index != len(linha) - 1:
                    proximoChar = linha[index + 1]
                    
                charAnterior = linha[index - 1]

                if comentarioLinha == True and char != '\n':
                    continue

                if comentarioBloco == True:
                    if char == '#' and charAnterior == '*':
                        comentarioBloco = False
                    continue

                elif dentroString or dentroLiteral:
                    lexema += char
                    if char == "'":
                        dentroString = False
                        ## Maior que 3 porque o char fica no formato 'x' sempre. Três caracteres.
                        adicionaLexemasETokens(dicionario, lexemas, tokens, "nomedastring" if len(lexema) > 3 else "nomedochar")
                        linhas.append(linha_atual)
                        lexema = ""

                    if char == '"':
                        dentroLiteral = False
                        adicionaLexemasETokens(dicionario, lexemas, tokens, "literal")
                        linhas.append(linha_atual)
                        lexema = ""
                        
                elif char in {"{", ";", "}", "(", ")", ":"}:
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, linha_atual)
                        lexema = ""

                    lexema = char
                    adicionaLexemasETokens(dicionario, lexemas, tokens, lexema)
                    linhas.append(linha_atual)
                    lexema = ""
                elif char != " ":
                    if char != '\n':
                        lexema += char

                    if char == "'":
                        dentroString = True

                    if char == '"':
                        dentroLiteral = True

                    if char == '#' and proximoChar == '#':
                        comentarioLinha = True
                    elif char == '#' and proximoChar == '*':
                        comentarioBloco = True
                        
                else:
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, linha_atual)
                        lexema = ""

            if lexema:
                processaLexema(dicionario, lexemas, tokens, lexema, linhas, linha_atual)
                lexema = ""

    return tokens, lexemas, linhas

def adicionaLexemasETokens(dicionario, lexemas, tokens, nomeDoToken):
    lexemas.append(nomeDoToken)
    tokens.append(dicionario.get(nomeDoToken))

def processaLexema(dicionario, lexemas, tokens, lexema, linhas, linha_atual):
    if (lexema == 'bol'):
        print('a')

    if lexema in dicionario:
        adicionaLexemasETokens(dicionario, lexemas, tokens, lexema)
        linhas.append(linha_atual)
    elif re.search("^\d+$", lexema):
        adicionaLexemasETokens(dicionario, lexemas, tokens, "numerointeiro")
        linhas.append(linha_atual)
    elif re.search("^\d+\.\d+$", lexema):
        adicionaLexemasETokens(dicionario, lexemas, tokens, "numerofloat")
        linhas.append(linha_atual)
    elif re.search("^[_a-zA-Z][_a-zA-Z0-9]*$", lexema):
        adicionaLexemasETokens(dicionario, lexemas, tokens, "nomevariavel")
        linhas.append(linha_atual)

def main():
    dicionario = carregar_dicionario()
    tokens, lexemas, linhas = analisar_arquivo("palavras.txt", dicionario)

    for i in range(len(tokens)):
        print(
            # "\033[1;32mToken: \033[0m"
            # + tokens[i]
            # + " \033[1;34m- Lexema: \033[0m"
            # + lexemas[i]
            # + " \033[1;33m- Linha: \033[0m"
            # + str(linhas[i])
            "\nToken: " + tokens[i] + " Lexema: " + lexemas[i] + " Linha: " + str(linhas[i])
        )

if __name__ == "__main__":
    main()

#     elif lexema == 'inicio':
#         tokens.append(15)
#         lexemas.append(lexema)
#     elif lexema == 'fim':
#         tokens.append(20)
#         lexemas.append(lexema)
#     elif lexema == ';':
#         tokens.append(40)
#         lexemas.append(lexema)

# #Entrega do lexico - token - lexema - linha
# for i in range(0,len(tokens)):
#     print('Token: '+str(tokens[i]) + ' - Lexema: '+str(lexemas[i]) + ' - Linha: 1' )

# #print(tokens) # [2, 11, 39, 15, 40, 20, 38]

# #salvar do lexico para entregar para o sintático
# tokens = np.array(tokens) #converte lista do python para numpy array
