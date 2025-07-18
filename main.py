# Jogo de bingo


import streamlit as st
from textwrap import dedent
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import random
import base64

if 'jogo_iniciado' not in st.session_state:
    st.session_state['jogo_iniciado'] = False

def gerar_cartela():
    """Gera uma cartela de bingo 5x5."""
    cartela = []

    numeros = list(range(1, 76))
    random.shuffle(numeros)

    for i in range(5):
        coluna = [n for n in numeros if (n-1) // 15 == i][:5]
        if i == 2:
            coluna[2] = " "
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

def mostrar_pdf_embed(caminho_pdf, largura="100%", altura="800px"):
    with open(caminho_pdf, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    iframe = (
        f'<iframe src="data:application/pdf;base64,{b64}" '
        f'width="{largura}" height="{altura}" type="application/pdf"></iframe>'
    )
    st.markdown(iframe, unsafe_allow_html=True)

def gerar_tudo(n_jogadores):
    cartelas = [gerar_cartela() for _ in range(n_jogadores)]
    pdf_path = "cartelas.pdf"
    criar_pdf(cartelas, filename=pdf_path)
    return pdf_path


def iniciar_jogo():
    st.session_state['sorteio'] = random.sample(range(1, 76), 75)
    st.session_state['sorteados'] = []
    st.session_state['numero_atual'] = None
    st.session_state['jogo_iniciado'] = True


def sortear_numero():
    if st.session_state['sorteio']:
        numero = st.session_state['sorteio'].pop(0)
        st.session_state['numero_atual'] = numero
        st.session_state['sorteados'].append(numero)
    else:
        st.session_state['numero_atual'] = None


def exibir_cartao_numero():
    """Exibe o número sorteado num cartão estilizado."""
    numero = st.session_state.get('numero_atual')
    if numero is not None:
        st.markdown(f"""
        <div style="
            margin: 30px auto;
            padding: 40px;
            max-width: 160px;
            text-align: center;
            border: 4px solid #4CAF50;
            border-radius: 20px;
            background-color: #F9FFF9;
            color: #2E7D32;
            font-size: 72px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            {numero}
        </div>
        """, unsafe_allow_html=True)


def exibir_pool_bingo():
    sorteados = set(st.session_state.get('sorteados', []))

    html = "<table style='border-collapse: collapse; margin: auto;'>"
    for row in range(15):
        html += "<tr>"
        for col in range(5):
            num = row + 1 + col*15
            if num in sorteados:
                bg, fg = "#4CAF50", "white"
            else:
                bg, fg = "#ddd", "#777"

            bloco = f"""
                <td style="padding:5px;">
                  <div style="
                    width:32px; height:32px;
                    border-radius:50%;
                    background-color:{bg};
                    color:{fg};
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    font-weight:bold;
                  ">
                    {num}
                  </div>
                </td>
            """
            html += dedent(bloco)   # remove todos os espaços iniciais
        html += "</tr>"
    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

jogadores = st.sidebar.number_input(
    "Informe o número de jogadores:",
    min_value=1,
    value=1,
    step=1
)

if st.sidebar.button('Gerar Cartelas'):
    st.session_state['jogo_iniciado'] = False
    pdf_path = gerar_tudo(jogadores)
    with st.expander('📄 Visualizar/Esconder Cartelas', expanded=True):
        mostrar_pdf_embed(pdf_path)

st.sidebar.button('Iniciar Jogo', on_click=iniciar_jogo)


if st.session_state['jogo_iniciado'] and st.sidebar.button('Sortear Número'):
    sortear_numero()

col_esq, col_dir = st.columns([2, 1])
with col_esq:
    if st.session_state['jogo_iniciado']:
        st.title("Bingo do João")
        exibir_cartao_numero()
with col_dir:
    if st.session_state['jogo_iniciado']:
        st.subheader("Números Sorteados")
        exibir_pool_bingo()

sorteio = list(range(1, 76))
random.shuffle(sorteio)
