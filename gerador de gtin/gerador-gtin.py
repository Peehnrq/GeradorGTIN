def calcular_digito_gtin(sequencia):
    # Inverte a sequência para facilitar a lógica da direita para a esquerda
    numeros = [int(d) for d in str(sequencia)][::-1]
    
    soma = 0
    for i, num in enumerate(numeros):
        # Pesos: posições pares (0, 2, 4...) peso 3, ímpares peso 1
        peso = 3 if i % 2 == 0 else 1
        soma += num * peso
    
    proximo_multiplo_10 = (soma + 9) // 10 * 10
    return proximo_multiplo_10 - soma

# Exemplo de uso:
# print(calcular_digito_gtin("202603050801")) -> Saída: 7