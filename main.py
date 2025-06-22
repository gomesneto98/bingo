# Jogo de bingo

import random
import time


def gerar_cartela():
    cartela = []
    numeros = list(range(1, 76))
    random.shuffle(numeros)
    print("Números embaralhados:", numeros)

    for i in range(5):
        coluna = []
        for n in numeros:
            if len(coluna) == 5:
                break
            if n // 15 == i:
                coluna.append(n)

        cartela.append(coluna)

    return cartela


def pega_numero(sorteio):
    if sorteio:
        return sorteio.pop(0)
    else:
        return None


cartela = gerar_cartela()

sorteio = list(range(1, 76))
random.shuffle(sorteio)

while True:
    numero = pega_numero(sorteio)
    if numero is None:
        print("Todos os números foram sorteados.")
        break

    print(f"Número sorteado: {numero}")

    opcao = input(
        "Digite 'c' para continuar ou 's' para sair: ").strip().lower()
    if opcao == 's':
        print("Saindo do jogo.")
        break
