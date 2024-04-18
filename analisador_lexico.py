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

def isDelimitador(char):
    delimitadores = ["{", "}", ";", "(", ")", ":", ","]

    if char in delimitadores:
        return True

    return False

def isOperador(char):
    operadores = [">", ">>", "<", "<<", "<=", ">=", "=", "==", "+", "-", "++", "--", "/", "*", "!="]

    if char in operadores:
        return True
    
    return False

def isNumero(char):
    numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    if char in numeros:
        return True
    
    return False

def analisar_arquivo(nome_arquivo, dicionario):    
    tokens = []
    lexemas = []
    linhas = []

    with open(nome_arquivo, "r") as file:
        numeroLinha = 1

        linha = file.readline()

        while (linha):
            tamanhoLinha = len(linha)
            lexema = ""
            contadorCharAtual = 0

            while contadorCharAtual < tamanhoLinha:
                char = linha[contadorCharAtual]
                proximoChar = None

                if contadorCharAtual != len(linha) - 1:
                    proximoChar = linha[contadorCharAtual + 1]
    
                if isDelimitador(char):
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, numeroLinha)
                        lexema = ""

                    processaLexema(dicionario, lexemas, tokens, char, linhas, numeroLinha)
                    lexema = ""
                ## Valida os comentários de linha pulando para a próxima
                elif char == '#' and proximoChar == '#':
                    contadorCharAtual = tamanhoLinha
                ## Valida os comentários de bloco loopando entre os chars até achar o *#.
                ## Se não achar, é erro léxico. Ignora o resto dos tokens.
                elif char == '#' and proximoChar == '*':
                    ## Para saber a linha caso erro
                    linhaComecoBloco = numeroLinha

                    while not (char == '*' and proximoChar == '#'):
                        ## Verifica se o char atual e próximo vão existir
                        if ((contadorCharAtual + 2) < tamanhoLinha):
                            contadorCharAtual += 1
                            char = linha[contadorCharAtual]
                            proximoChar = linha[contadorCharAtual+1]                   
                        else:
                            linha = file.readline()
                            tamanhoLinha = len(linha)
                            numeroLinha += 1
                            contadorCharAtual = -1
                            ## O comentário não foi fechado pois acabaram as linhas do arquivo
                            ## sem ocorrência de *#.
                            if (not linha):
                                print("Erro: Comentario nao fechado na linha %d" %linhaComecoBloco)
                                break

                    contadorCharAtual += 1
                elif char == "'" or char == '"':
                    delimitador = char;
                    contadorCharAtual += 1

                    ## Tenta buscar mais uma ocorrência do delimitador na linha. Se não achar, retorna -1 e
                    ## indica o erro de char ou string não fechada
                    if linha[contadorCharAtual:].find(delimitador) == -1:
                        msg = "String nao fechada" if delimitador == '"' else "Char nao fechado"
                        print("Erro: " + msg + " na linha %d" %numeroLinha)
                        ## Passa para a próxima linha
                        contadorCharAtual = tamanhoLinha
                    else:
                        indiceFinalDaStringOuChar = contadorCharAtual+linha[contadorCharAtual:].find(delimitador)
                        lexema = linha[contadorCharAtual:indiceFinalDaStringOuChar]
                        contadorCharAtual = indiceFinalDaStringOuChar

                        if (delimitador == "'"):
                            if (len(lexema) > 1):
                                print("Erro: Char com mais de um caracter na linha %d" %numeroLinha)
                            else:
                                processaLexema(dicionario, lexemas, tokens, "nomedochar", linhas, numeroLinha)
                        else:
                            processaLexema(dicionario, lexemas, tokens, "nomedastring", linhas, numeroLinha)

                        lexema = ""
                elif char == "`":
                    contadorCharAtual += 1

                    if linha[contadorCharAtual:].find('`') == -1:
                        print("Erro: Literal nao fechado na linha %d" %numeroLinha)
                        contadorCharAtual = tamanhoLinha
                    else:
                        indiceFinalDoLiteral = contadorCharAtual+linha[contadorCharAtual:].find('`')
                        lexema = linha[contadorCharAtual:indiceFinalDoLiteral]
                        contadorCharAtual = indiceFinalDoLiteral

                        processaLexema(dicionario, lexemas, tokens, "literal", linhas, numeroLinha)

                    lexema = ""
                ## Operadores como ++ e >>
                elif proximoChar != None and isOperador(char + proximoChar):
                    ## Se tem algo colado no operador. Por exemplo cout>>
                    ## Ele adicionará o cout antes, para ficar na ordem correta
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, numeroLinha)
                        lexema = ""

                    processaLexema(dicionario, lexemas, tokens, char + proximoChar, linhas, numeroLinha)
                    contadorCharAtual += 1
                elif isOperador(char):
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, numeroLinha)

                    processaLexema(dicionario, lexemas, tokens, char, linhas, numeroLinha)
                elif char != " ":
                    if char != '\n':
                        lexema += char
                        
                else:
                    if lexema:
                        processaLexema(dicionario, lexemas, tokens, lexema, linhas, numeroLinha)
                        lexema = ""
                
                contadorCharAtual+=1

            if lexema:
                processaLexema(dicionario, lexemas, tokens, lexema, linhas, numeroLinha)
                lexema = ""

            linha = file.readline()
            numeroLinha += 1

    return tokens, lexemas, linhas

def adicionaLexemasETokens(dicionario, lexemas, tokens, nomeDoToken):
    lexemas.append(nomeDoToken)
    tokens.append(dicionario.get(nomeDoToken))

def processaLexema(dicionario, lexemas, tokens, lexema, linhas, linha_atual):
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
            "\nToken: " + tokens[i] + " | Lexema: " + lexemas[i] + " | Linha: " + str(linhas[i])
        )

if __name__ == "__main__":
    main()