#entrada, geralmente vem de um arquivo texto
palavra = ''

#variavel para armazenar o lexema 
lexema = ''

dicionario = {
    "while": "1",
    "void": "2",
    "string": "3",
    "return": "4",
    "numerointeiro": "5",
    "numerofloat": "6",
    "nomevariavel": "7",
    "nomedochar": "8",
    "nomedavariavel": "9",
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
    "-": "48"
}
tokens = []
lexemas = []

file = open('palavras.txt', 'r')
 
while 1:
     
    char = file.read(1)   

    if char == '{': 
        if lexema != '':
            lexemas.append(lexema)
            lexema = ''

        lexema = char
        lexemas.append(lexema)
        lexema = ''
    
    elif char != ' ':  #se nao for espaço... aqui tem q colocar 
                       #outros caracters como pontuacao e parentização
            lexema = lexema + char
    else:
        if lexema != '':
            lexemas.append(lexema)
            lexema = ''

    if not char: 
        break

    

    if dicionario.get(lexema):
        tokens.append(dicionario.get(lexema))

print(lexemas)
print(tokens)
 

   




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


file.close()