import helpers.tabela_parsing as t_parsing
import analisador_lexico as lexico
import helpers.palavras_reservadas as p_reservadas

def palavra_por_codigo(codigo):
    return p_reservadas.palavras_reservadas.get(int(codigo))

def parse(tabParsing, tokens):
    simbolo_inicial = "S"  # Substitua "S" pelo símbolo inicial da sua gramática
    pilha = ["$", simbolo_inicial]  # Pilha com o símbolo inicial e o marcador de fim de pilha
    topo = pilha[-1]  # Topo da pilha
    i = 0  # Índice para percorrer os tokens de entrada
    while topo != "$" and i < len(tokens):
        token_atual = palavra_por_codigo(tokens[i]["codigo"])
        if topo == token_atual:  # Coincidência entre topo da pilha e token atual
            pilha.pop()
            i += 1
        else:
            regra = tabParsing[int(topo)][int(token_atual)]
            print(regra)
            if regra:
                pilha.pop()
                if regra != ["î"]:  # Não empilha se a produção é vazia
                    pilha.extend(reversed(regra))
            else:
                print(
                    f"Erro de parsing: regra não encontrada para {topo} e {token_atual} na linha {tokens[i]['linha']}"
                )
                return False
        topo = pilha[-1] if pilha else "$"  # Atualiza o topo
    return True if topo == "$" and i == len(tokens) else False

# Carrega o dicionário de palavras reservadas
dicionario = lexico.carregar_dicionario()
tokens, linhas = lexico.pegar_tokens("tests/palavras.txt", dicionario)

resultado = parse(t_parsing.tabParsing, tokens)
if resultado:
    print("Análise sintática concluída com sucesso!")
else:
    print("Erro durante a análise sintática.")
