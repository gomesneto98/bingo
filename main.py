# Jogo de bingo

import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import random


JOGADORES = 4

def gerar_cartela():
    numeros = list(range(1, 76))
    random.shuffle(numeros)
    cartela = []
    for i in range(5):
            coluna = []
            for n in numeros:
                if len(coluna) == 5:
                    break
                if n // 15 == i:
                    coluna.append(n)
            if i == 2:
                coluna[2] = "X"

            cartela.append(coluna)

    return cartela

def draw_cartela(c, x, y, cell_size, cartela):
    tamanho_fonte = int(cell_size * 0.5)
    c.setFont("Helvetica-Bold", tamanho_fonte)

    # desenha 5x5 células
    for i in range(6):  # linhas horizontais
        c.line(x, y - i*cell_size, x + 5*cell_size, y - i*cell_size)
    for j in range(6):  # linhas verticais
        c.line(x + j*cell_size, y, x + j*cell_size, y - 5*cell_size)
    # preenche números
    for row in range(5):
        for col in range(5):
            num = cartela[row][col]
            tx = x + row*cell_size + cell_size/2
            ty = y - col*cell_size - cell_size/2
            c.drawCentredString(tx, ty - 4, str(num))

def criar_pdf(cartelas, filename="cartelas.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    page_w, page_h = A4

    # margens e espaçamento
    margin_x = 15 * mm
    margin_y = 15 * mm
    gutter_x = 10 * mm
    gutter_y = 10 * mm

    # calcula espaço disponível e tamanho da célula
    avail_w = (page_w - 2*margin_x - gutter_x) / 2
    avail_h = (page_h - 2*margin_y - 2*gutter_y) / 3
    cell_size = min(avail_w/5, avail_h/5)

    for idx, cartela in enumerate(cartelas):
        # quando ultrapassar 6 por página, começa nova
        if idx > 0 and idx % 6 == 0:
            c.showPage()

        pos = idx % 6
        col = pos % 2
        row = pos // 2

        x = margin_x + col * (5*cell_size + gutter_x)
        y = page_h - margin_y - row * (5*cell_size + gutter_y)

        draw_cartela(c, x, y, cell_size, cartela)

    c.save()
    print(f"{filename} gerado com sucesso.")

if __name__ == "__main__":
    # Exemplo: gerar 12 cartelas (2 páginas de 6 cada)
    cartelas = [gerar_cartela() for _ in range(JOGADORES)]
    criar_pdf(cartelas)

def pega_numero(sorteio):
    if sorteio:
        return sorteio.pop(0)
    else:
        return None

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
