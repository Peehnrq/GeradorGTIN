import streamlit as st
import pandas as pd

# 1. Sua função lógica original [cite: 1]
def calcular_digito_gtin(sequencia):
    numeros = [int(d) for d in str(sequencia)][::-1]
    soma = 0
    for i, num in enumerate(numeros):
        # Pesos: posições pares peso 3, ímpares peso 1 [cite: 1]
        peso = 3 if i % 2 == 0 else 1
        soma += num * peso
    proximo_multiplo_10 = (soma + 9) // 10 * 10
    return proximo_multiplo_10 - soma

# 2. Configuração da Página [cite: 1]
st.set_page_config(page_title="Gerador GTIN-13 Pro", page_icon="🔢")
st.title("🔢 Gerador de GTIN Customizado")

tab1, tab2 = st.tabs(["Gerar Único", "Gerar em Massa (Data Manual)"])

with tab1:
    st.write("Digite os **12 primeiros dígitos** manualmente.")
    entrada = st.text_input("Sequência de 12 dígitos:", max_chars=12, key="unico")
    if entrada and len(entrada) == 12 and entrada.isdigit():
        digito = calcular_digito_gtin(entrada)
        st.success(f"Dígito Verificador: {digito}")
        st.code(f"{entrada}{digito}")

with tab2:
    st.subheader("Configuração da Estrutura")
    st.write("Monte a data e a sequência para o lote:")

    # Seleção Manual de Data
    col_data1, col_data2, col_data3 = st.columns(3)
    
    with col_data1:
        ano_input = st.number_input("Ano", min_value=2024, max_value=2030, value=2026)
    with col_data2:
        dia_input = st.number_input("Dia", min_value=1, max_value=31, value=17)
    with col_data3:
        mes_input = st.number_input("Mês", min_value=1, max_value=12, value=3)

    # Formatação das strings com zeros à esquerda (zfill)
    ano_str = str(ano_input)
    dia_str = str(dia_input).zfill(2)
    mes_str = str(mes_input).zfill(2)
    
    prefixo_custom = f"{ano_str}{dia_str}{mes_str}"
    st.info(f"O prefixo será: **{prefixo_custom}** (8 dígitos)")

    # Configuração do Sequencial e Quantidade
    col_seq1, col_seq2 = st.columns(2)
    with col_seq1:
        inicio_seq = st.number_input("Iniciar sequência em:", min_value=0, max_value=9999, value=800)
    with col_seq2:
        quantidade = st.number_input("Quantidade (Máx 100):", min_value=1, max_value=100, value=10)

    if st.button("Gerar Lote Customizado"):
        lista_gtins = []
        
        for i in range(quantidade):
            # Sequencial sempre com 4 dígitos para fechar os 12 totais
            sequencial = str(inicio_seq + i).zfill(4)
            base_12 = f"{prefixo_custom}{sequencial}"
            
            # Cálculo do dígito [cite: 1]
            digito = calcular_digito_gtin(base_12)
            lista_gtins.append(f"{base_12}{digito}")
        
        df = pd.DataFrame(lista_gtins, columns=["GTIN-13 Gerado"])
        
        st.write("### Resultados:")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Planilha CSV",
            data=csv,
            file_name=f"gtins_{prefixo_custom}.csv",
            mime="text/csv"
        )

# 3. Rodapé [cite: 1]
st.markdown("""<style>.footer {position: fixed; left: 0; bottom: 10px; width: 100%; text-align: center; color: gray; font-size: 13px;}</style><div class="footer">Criado e pensado por Pedro Parra.</div>""", unsafe_allow_html=True)
