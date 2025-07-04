# Jogo de bingo

import random
import streamlit as st
from textwrap import dedent


def gerar_cartela():
    """Gera uma cartela de bingo 5x5."""
    cartela = []

    numeros = list(range(1, 76))
    random.shuffle(numeros)

    for i in range(5):
        coluna = [n for n in numeros if (n-1) // 15 == i][:5]
        cartela.append(coluna)

    return cartela


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


st.sidebar.button('Iniciar Jogo', on_click=iniciar_jogo)

if st.sidebar.button('Sortear Número', on_click=sortear_numero):
    pass  # só dispara o callback

# cria duas colunas: à esquerda seu título/cartão; à direita o pool de bolinhas
col_esq, col_dir = st.columns([2, 1])

with col_esq:
    st.title("Bingo do João")
    exibir_cartao_numero()      # sua função de mostrar o número grande

with col_dir:
    st.subheader("Números Sorteados")
    exibir_pool_bingo()


# if 'jogo_iniciado' not in st.session_state:
#     st.session_state['jogo_iniciado'] = False

# if not st.session_state['jogo_iniciado']:
#     if st.sidebar.button('Novo Jogo'):
#         st.session_state['mostrar_entrada'] = True

#     if st.session_state.get('mostrar_entrada'):
#         if st.button('Confirmar'):
#             iniciar_jogo()
#             st.session_state['mostrar_entrada'] = False
# else:
#     if 'sorteio' not in st.session_state or not st.session_state['sorteio']:
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button('Sortear Novo Número'):
#                 sortear_numero()
#         with col2:
#             if st.sidebar.button('Sair do Jogo'):
#                 st.session_state.clear()
#                 st.experimental_rerun()
#         if st.session_state.get('numero_atual') is not None:
#             st.write(f'Número sorteado: {st.session_state["numero_atual"]}')
#         elif st.session_state['sorteio'] == []:
#             st.write('Todos os números foram sorteados.')
#             if st.button('Novo Jogo'):
#                 st.session_state.clear()
#                 st.experimental_rerun()
