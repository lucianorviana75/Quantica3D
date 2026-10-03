from flask import Flask, render_template, request, jsonify
import math
import os

app = Flask(__name__)

# ==========================================
# 1. BANCO DE DADOS: TABELA PERIÓDICA (118)
# ==========================================
TABELA_PERIODICA = {
    "H":  {"nome": "Hidrogénio", "massa_molar": 1.008},
    "He": {"nome": "Hélio", "massa_molar": 4.0026},
    "Li": {"nome": "Lítio", "massa_molar": 6.94},
    "Be": {"nome": "Berílio", "massa_molar": 9.0122},
    "B":  {"nome": "Boro", "massa_molar": 10.81},
    "C":  {"nome": "Carbono", "massa_molar": 12.011},
    "N":  {"nome": "Azoto / Nitrogénio", "massa_molar": 14.007},
    "O":  {"nome": "Oxigénio", "massa_molar": 15.999},
    "F":  {"nome": "Flúor", "massa_molar": 18.998},
    "Ne": {"nome": "Néon", "massa_molar": 20.180},
    "Na": {"nome": "Sódio", "massa_molar": 22.990},
    "Mg": {"nome": "Magnésio", "massa_molar": 24.305},
    "Al": {"nome": "Alumínio", "massa_molar": 26.982},
    "Si": {"nome": "Silício", "massa_molar": 28.085},
    "P":  {"nome": "Fósforo", "massa_molar": 30.974},
    "S":  {"nome": "Enxofre", "massa_molar": 32.06},
    "Cl": {"nome": "Cloro", "massa_molar": 35.45},
    "Ar": {"nome": "Árgon", "massa_molar": 39.948},
    "K":  {"nome": "Potássio", "massa_molar": 39.098},
    "Ca": {"nome": "Cálcio", "massa_molar": 40.078},
    # Compostos comuns para testes práticos de simulação
    "CO2": {"nome": "Dióxido de Carbono", "massa_molar": 44.01},
    "H2O": {"nome": "Água (Vapor)", "massa_molar": 18.015}
}

# ==========================================
# 2. BANCO DE DADOS: MATERIAIS DOS VASOS
# ==========================================
MATERIAIS = {
    "vidro":    {"nome": "Vidro Comum", "resistencia_mpa": 50.0},
    "acrilico": {"nome": "Acrílico (PMMA)", "resistencia_mpa": 70.0},
    "aluminio": {"nome": "Alumínio (6061-T6)", "resistencia_mpa": 276.0},
    "aco":      {"nome": "Aço Inoxidável (316L)", "resistencia_mpa": 485.0},
    "borracha": {"nome": "Borracha", "resistencia_mpa": 25.0}
}

CONSTANTE_R = 8.314  # Constante universal dos gases [J / (mol * K)]

@app.route('/')
def home():
    """Renderiza a página principal do Quantica3D."""
    return render_template('index.html')

@app.route('/api/elementos', methods=['GET'])
def obter_elementos():
    """Retorna o banco de dados de elementos e materiais para a UI."""
    return jsonify({"elementos": TABELA_PERIODICA, "materiais": MATERIAIS})

@app.route('/api/calcular', methods=['POST'])
def calcular_fisica_quimica():
    """
    Recebe os parâmetros do front-end, executa o cálculo de pressão/tensão
    e determina reações/efeitos visuais (explosão, congelamento, corrosão).
    """
    dados = request.get_json()

    # Leitura dos inputs do utilizador
    geometria = dados.get('geometria', 'cubo')          # 'cubo', 'esfera', 'cilindro'
    dimensao = float(dados.get('dimensao', 0.5))        # Lado ou Raio em metros
    espessura = float(dados.get('espessura', 0.005))    # Espessura da parede em metros
    material_id = dados.get('material', 'vidro')
    elemento_id = dados.get('elemento', 'CO2')
    massa_g = float(dados.get('massa', 100.0))          # Massa em gramas
    temp_c = float(dados.get('temperatura', 25.0))      # Temperatura em Celsius

    # 1. Cálculo do Volume (m³)
    if geometria == 'esfera':
        volume = (4.0 / 3.0) * math.pi * (dimensao ** 3)
    elif geometria == 'cubo':
        volume = dimensao ** 3
    elif geometria == 'cilindro':
        # Assumindo altura = 2 * raio
        volume = math.pi * (dimensao ** 2) * (2 * dimensao)
    else:
        volume = 1.0

    # 2. Conversão de Temperatura (K) e Mols (n)
    temp_k = temp_c + 273.15
    massa_molar = TABELA_PERIODICA.get(elemento_id, {}).get('massa_molar', 44.01)
    mols = massa_g / massa_molar

    # 3. Equação dos Gases Ideais: P = (n * R * T) / V (em Pascal)
    pressao_pa = (mols * CONSTANTE_R * temp_k) / volume
    pressao_atm = pressao_pa / 101325.0

    # 4. Tensão Mecânica na Parede (Paredes Finas: sigma = (P * r) / (2 * t))
    tensao_pa = (pressao_pa * dimensao) / (2.0 * espessura)
    tensao_mpa = tensao_pa / 1e6

    # 5. Estresse e Verificação de Ruptura
    resistencia_mat = MATERIAIS.get(material_id, {}).get('resistencia_mpa', 50.0)
    estresse_percentual = (tensao_mpa / resistencia_mat) * 100.0
    ruptura = estresse_percentual >= 100.0

    # ==========================================
    # 6. DETERMINAÇÃO DA REAÇÃO / ESTADO VISUAL
    # ==========================================
    estado_efeito = "estavel"  # Opções: 'estavel', 'explosao', 'congelado', 'corrosao'
    mensagem_status = "SISTEMA ESTÁVEL"

    if ruptura:
        estado_efeito = "explosao"
        mensagem_status = "CRÍTICO: EXPLOSÃO POR SOBREPRESSÃO!"
    elif temp_c <= -10.0:
        estado_efeito = "congelado"
        mensagem_status = "ALERTA: CRISTALIZAÇÃO / CONGELAMENTO"
    elif elemento_id in ["F", "Cl"] and material_id in ["aluminio", "aco"]:
        # Exemplo de incompatibilidade química: Halogénios corroem metais
        estado_efeito = "corrosao"
        mensagem_status = "ALERTA: REAÇÃO DE CORROSÃO ACERBADA!"
    elif estresse_percentual > 70.0:
        mensagem_status = "ATENÇÃO: ALTA TENSÃO MECÂNICA"

    # Resposta em JSON devolvida para a interface 3D
    return jsonify({
        "status": "ok",
        "resultados": {
            "volume_m3": round(volume, 4),
            "mols": round(mols, 2),
            "pressao_atm": round(pressao_atm, 2),
            "pressao_pa": round(pressao_pa, 0),
            "tensao_mpa": round(tensao_mpa, 2),
            "estresse_percentual": round(estresse_percentual, 1),
            "ruptura": ruptura,
            "estado_efeito": estado_efeito,
            "mensagem_status": mensagem_status
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
