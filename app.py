import streamlit as st
import pandas as pd
import random
import string

# 1. Função lógica original GTIN
def calcular_digito_gtin(sequencia):
    numeros = [int(d) for d in str(sequencia)][::-1]
    soma = 0
    for i, num in enumerate(numeros):
        # Pesos: posições pares peso 3, ímpares peso 1
        peso = 3 if i % 2 == 0 else 1
        soma += num * peso
    proximo_multiplo_10 = (soma + 9) // 10 * 10
    return proximo_multiplo_10 - soma

# 2. Função lógica SKU (LNLNLNLNL)
def gerar_sku_aleatorio():
    letras = string.ascii_uppercase
    numeros = string.digits
    sku = ""
    for i in range(9):
        if i % 2 == 0: # Letra
            sku += random.choice(letras)
        else:          # Número
            sku += random.choice(numeros)
    return sku

# 3. Configuração da Página
st.set_page_config(page_title="Gerador GTIN-13 Pro", page_icon="🔢")
st.title("🔢 Gerador de Códigos Customizado")

# Adicionado a terceira aba "Gerar SKU"
tab1, tab2, tab3 = st.tabs(["Gerar Único", "Gerar em Massa (GTIN)", "Gerar SKU"])

# --- ABA 1: GERAR ÚNICO ---
with tab1:
    st.write("Digite os **12 primeiros dígitos** manualmente.")
    entrada = st.text_input("Sequência de 12 dígitos:", max_chars=12, key="unico")
    if entrada and len(entrada) == 12 and entrada.isdigit():
        digito = calcular_digito_gtin(entrada)
        gtin_completo = f"{entrada}{digito}"
        st.success(f"Dígito Verificador: {digito}")
        st.code(gtin_completo)

# --- ABA 2: GERAR EM MASSA (GTIN) ---
with tab2:
    st.subheader("Configuração da Estrutura GTIN")
    col_data1, col_data2, col_data3 = st.columns(3)
    
    with col_data1:
        ano_input = st.number_input("Ano", min_value=2024, max_value=2030, value=2026)
    with col_data2:
        dia_input = st.number_input("Dia", min_value=1, max_value=31, value=17)
    with col_data3:
        mes_input = st.number_input("Mês", min_value=1, max_value=12, value=3)

    ano_str = str(ano_input)
    dia_str = str(dia_input).zfill(2)
    mes_str = str(mes_input).zfill(2)
    prefixo_custom = f"{ano_str}{dia_str}{mes_str}"

    col_seq1, col_seq2 = st.columns(2)
    with col_seq1:
        inicio_seq = st.number_input("Iniciar sequência em:", min_value=0, max_value=9999, value=800)
    with col_seq2:
        quantidade = st.number_input("Quantidade GTIN (Máx 100):", min_value=1, max_value=100, value=10)

    if st.button("Gerar Lote GTIN"):
        lista_gtins = []
        for i in range(quantidade):
            sequencial = str(inicio_seq + i).zfill(4)
            base_12 = f"{prefixo_custom}{sequencial}"
            digito = calcular_digito_gtin(base_12)
            lista_gtins.append(f"{base_12}{digito}")
        
        df_gtin = pd.DataFrame(lista_gtins, columns=["GTIN-13 Gerado"])
        st.dataframe(df_gtin, use_container_width=True)

# --- ABA 3: GERAR SKU (NOVA) ---
with tab3:
    st.subheader("Gerador de SKU")
    st.write("Gera códigos de 9 caracteres seguindo o padrão: **Letra-Número-Letra...**")
    
    qtd_sku = st.slider("Quantidade de SKUs para gerar:", min_value=1, max_value=100, value=50)
    
    if st.button("Gerar SKUs"):
        lista_skus = [gerar_sku_aleatorio() for _ in range(qtd_sku)]
        
        # Exibe em uma caixa de texto para fácil cópia
        st.text_area("SKUs Gerados:", value="\n".join(lista_skus), height=300)
        
        # Opção de baixar como CSV
        df_sku = pd.DataFrame(lista_skus, columns=["SKU Gerado"])
        csv_sku = df_sku.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar SKUs em CSV",
            data=csv_sku,
            file_name="skus_gerados.csv",
            mime="text/csv"
        )

# 4. Rodapé
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 10px;
        width: 100%;
        text-align: center;
        color: gray;
        font-size: 13px;
    }
    </style>
    <div class="footer">
        &copy; 2026 - Criado e pensado por <a href="https://www.instagram.com/peehnrq" target="_blank">Pedro Parra</a>.
    </div>
    """,
    unsafe_allow_html=True
)
