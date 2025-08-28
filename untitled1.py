# Importando bibliotecas necessárias
import pandas as pd
import numpy as np

# Carregando os dados da planilha
url = '/content/Quadro_3_Parametros_Ocupacao finalizada.csv'
data = pd.read_csv(url, sep=';')

# Limpeza e preparação dos dados
data['C.A. Maximo'] = data['C.A. Maximo'].astype(str).str.replace(r'[^0-9.,]+', '', regex=True)
data['C.A. Maximo'] = data['C.A. Maximo'].str.replace(',', '.')
data['C.A. Maximo'] = pd.to_numeric(data['C.A. Maximo'], errors='coerce')

data['T.O. até 500m²'] = data['T.O. até 500m²'].astype(str).str.replace(r'[^0-9.,]+', '', regex=True)
data['T.O. até 500m²'] = data['T.O. até 500m²'].str.replace(',', '.')
data['T.O. até 500m²'] = pd.to_numeric(data['T.O. até 500m²'], errors='coerce')

data['Recuo Frente'] = data['Recuo Frente'].astype(str).str.replace(r'[^0-9.,]+', '', regex=True)
data['Recuo Frente'] = data['Recuo Frente'].str.replace(',', '.')
data['Recuo Frente'] = pd.to_numeric(data['Recuo Frente'], errors='coerce')

data['Recuo ≤10m'] = data['Recuo ≤10m'].astype(str).str.replace(r'[^0-9.,]+', '', regex=True)
data['Recuo ≤10m'] = data['Recuo ≤10m'].str.replace(',', '.')
data['Recuo ≤10m'] = pd.to_numeric(data['Recuo ≤10m'], errors='coerce')

data['Recuo >10m'] = data['Recuo >10m'].astype(str).str.replace(r'[^0-9.,]+', '', regex=True)
data['Recuo >10m'] = data['Recuo >10m'].str.replace(',', '.')
data['Recuo >10m'] = pd.to_numeric(data['Recuo >10m'], errors='coerce')

def validar_entradas(zona, area, medidas):
    # Verificar se a zona existe
    if zona not in data['Zona'].values:
        print(" Erro: Zona não encontrada na planilha.")
        return False

    # Verificar área válida
    if area <= 0:
        print(" Erro: Área deve ser maior que zero.")
        return False

    # Verificar medidas válidas
    if any(m <= 0 for m in medidas.values()):
        print(" Erro: Medidas não podem ser zero ou negativas.")
        return False

    return True

def calcular_largura_util(ns_medida, recuo_lateral):
    return ns_medida - (2 * recuo_lateral)

def calcular_profundidade_util(lo_medida, recuo_frontal, recuo_fundo):
    return lo_medida - recuo_frontal - recuo_fundo

def mostrar_resultados(zona, area, medidas):
    try:
        # Filtrar dados da zona
        dados_zona = data[data['Zona'] == zona].iloc[0]

        # Configurações da zona
        recuo_frontal = dados_zona['RecuoFrontal']
        recuo_fundo = dados_zona['RecuoFundo']
        recuo_lateral = dados_zona['RecuoLateral']
        taxa_ocupacao = dados_zona['TaxaOcupacao']
        ca_maximo = dados_zona['C.A. Maximo']
        gabarito = dados_zona['Gabarito']
        cota_max = dados_zona['Cota Max. Terreno p/ unidade']

        # Cálculos principais
        area_ocupada = area * taxa_ocupacao
        area_maxima = area * ca_maximo
        largura_util = calcular_largura_util(medidas['ns'], recuo_lateral)
        profundidade_util = calcular_profundidade_util(medidas['lo'], recuo_frontal, recuo_fundo)
        qtd_unidades = area / cota_max

        # Resultados
        print(f"\n RESULTADOS PARA ZONA {zona}")
        print("======================================")
        print(f" DIMENSÕES ÚTEIS")
        print(f"• Largura útil: {largura_util:.2f}m")
        print(f"• Profundidade útil: {profundidade_util:.2f}m")

        print("\n PARÂMETROS CONSTRUTIVOS")
        print(f"• Taxa de ocupação: {taxa_ocupacao*100:.2f}%")
        print(f"• C.A. Máximo: {ca_maximo:.2f}")
        print(f"• Gabarito (altura máxima): {gabarito:.2f}m")

        print("\n ÁREAS")
        print(f"• Área ocupada permitida: {area_ocupada:.2f}m²")
        print(f"• Área máxima construída: {area_maxima:.2f}m²")
        print(f"• Unidades possíveis: {qtd_unidades:.1f}")

        print("\n RECUOS OBRIGATÓRIOS")
        print(f"• Recuo frontal: {recuo_frontal}m")
        print(f"• Recuo de fundo: {recuo_fundo}m")
        print(f"• Recuo lateral: {recuo_lateral}m")
        display(data[['Zona', 'Recuo Frente', 'Recuo ≤10m', 'Recuo >10m']])

        print("\n ESTIMATIVA DE INVESTIMENTO")
        investimento = area_maxima * 2500  # R$/m²
        print(f"• Valor estimado: R$ {investimento:,.2f}")

    except Exception as e:
        print(f"Erro durante os cálculos: {str(e)}")

# Entrada de dados
print(" ANÁLISE URBANÍSTICA - SIMULADOR")
print("----------------------------------")
zona = input("Informe a zona: ")
try:
    area = float(input("Área total do terreno (m²): "))
    print("\nInforme as medidas reais do terreno:")
    norte_sul = float(input("Medida Norte-Sul (m): "))
    leste_oeste = float(input("Medida Leste-Oeste (m): "))

    # Validar entradas
    medidas = {'ns': norte_sul, 'lo': leste_oeste}
    if validar_entradas(zona, area, medidas):
        mostrar_resultados(zona, area, medidas)
    else:
        print("Execução interrompida devido a dados inválidos.")

except ValueError:
    print("Erro: Insira valores numéricos válidos.")
