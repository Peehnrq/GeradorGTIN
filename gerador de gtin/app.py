import streamlit as st

# 1. Primeiro definimos a função lógica
def calcular_digito_gtin(sequencia):
    # Inverte a sequência para facilitar a lógica da direita para a esquerda
    numeros = [int(d) for d in str(sequencia)][::-1]
    
    soma = 0
    for i, num in enumerate(numeros):
        # Pesos: posições pares (índice 0, 2...) peso 3, ímpares peso 1
        peso = 3 if i % 2 == 0 else 1
        soma += num * peso
    
    proximo_multiplo_10 = (soma + 9) // 10 * 10
    return proximo_multiplo_10 - soma

# 2. Depois configuramos a interface do Streamlit
st.set_page_config(page_title="Verificador GTIN", page_icon="🔢")

st.title("Gerador de GTIN")
st.write("Insira os números do GTIN (sem o último dígito!!!)")

entrada = st.text_input("Digite a sequência (ex: 202603050801):", max_chars=13)

if entrada:
    if entrada.isdigit():
        # Agora o Python saberá o que é 'calcular_digito_gtin'
        digito = calcular_digito_gtin(entrada)
        st.success(f"O dígito verificador é: **{digito}**")
        st.info(f"Código completo: **{entrada}{digito}**")
    else:
        st.error("Por favor, digite apenas números.")
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
    }
    </style>
    <div class="footer">
        Criado e pensado por Pedro Parra.
    </div>
    """,
    unsafe_allow_html=True
)