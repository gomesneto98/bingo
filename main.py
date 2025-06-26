# Jogo de bingo

import random
import time
from reportlab.pdfgen import canvas

c = canvas.Canvas("cartelas.pdf")
c.save()

N_JOGADORES = 1

def gerar_cartela(n_cartelas):
    cartelas = []
    cartela = []
    for j in range(n_cartelas):
        numeros = list(range(1, 76))
        random.shuffle(numeros)

        for i in range(5):
            coluna = []
            for n in numeros:
                if len(coluna) == 5:
                    break
                if n // 15 == i:
                    coluna.append(n)
            if i == 2:
                coluna[2] = "espaço livre"

            cartela.append(coluna)
        cartelas.append(cartela)

    return cartelas


def pega_numero(sorteio):
    if sorteio:
        return sorteio.pop(0)
    else:
        return None

cartelas = gerar_cartela(N_JOGADORES)
print (cartelas)

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
