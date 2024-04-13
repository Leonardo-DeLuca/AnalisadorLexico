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
    tokens = []
    lexemas = []

    with open(nome_arquivo, "r") as file:
        lexema = ""
        while True:
            char = file.read(1)

            if char in {"{", ";", "}"}:
                if lexema:
                    lexemas.append(lexema)
                    tokens.append(dicionario.get(lexema))
                    lexema = ""

                lexema = char
                lexemas.append(lexema)
                tokens.append(dicionario.get(lexema))
                lexema = ""
            elif char != " ":  # se nao for espaço... aqui tem q colocar
                # outros caracters como pontuacao e parentização
                lexema += char
            else:
                if lexema:
                    if lexema in dicionario:
                        lexemas.append(lexema)
                        tokens.append(dicionario.get(lexema))
                    elif re.search("^[_a-zA-Z0-9][_a-zA-Z0-9]*$", lexema):
                        lexemas.append("nomevariavel")
                        tokens.append(dicionario.get("nomevariavel"))
                    lexema = ""

            if not char:
                if lexema:
                    lexemas.append(lexema)
                    tokens.append(dicionario.get(lexema))
                    lexema = ""
                break

    return tokens, lexemas


def main():
    dicionario = carregar_dicionario()
    tokens, lexemas = analisar_arquivo("palavras.txt", dicionario)
    print(lexemas)
    print(tokens)


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
