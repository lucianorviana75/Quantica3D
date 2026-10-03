import math
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# ==========================================
# BANCO DE DADOS: MATERIAIS CONDUTORES
# ==========================================
MATERIAIS_CONDUTORES = {
    "cobre": {
        "nome": "Cobre (Cu) - NBR 5410",
        "resistividade": 0.0178,  # Ohm * mm² / m
        "temp_fusao": 1085,
    },
    "aluminio": {
        "nome": "Alumínio (Al) - NBR 5410",
        "resistividade": 0.0282,  # Ohm * mm² / m
        "temp_fusao": 660,
    },
}

# Bitolas normatizadas em mm² conforme NBR 5410
BITOLAS_PADRAO = [
    1.5,
    2.5,
    4.0,
    6.0,
    10.0,
    16.0,
    25.0,
    35.0,
    50.0,
    70.0,
    95.0,
    120.0,
    150.0,
    185.0,
    240.0,
]


@app.route("/")
def home():
  """Renderiza a página principal do simulador."""
  return render_template("circuito.html")


@app.route("/api/dados_iniciais", methods=["GET"])
def obter_dados_iniciais():
  """Retorna os dados dos materiais e bitolas para popular os selects HTML."""
  return jsonify(
      {"materiais": MATERIAIS_CONDUTORES, "bitolas": BITOLAS_PADRAO}
  )


@app.route("/api/calcular_circuito", methods=["POST"])
def calcular_circuito():
  """Cálculo Elétrico Residencial, Predial e Industrial.

  Suporta Monofásico, Bifásico e Trifásico.
  """
  dados = request.get_json() or {}

  tensao = float(dados.get("tensao", 220.0))  # Volts (V)
  potencia_w = float(dados.get("potencia_w", 5000.0))  # Watts (W)
  fator_potencia = float(dados.get("fator_potencia", 0.85))  # cos phi
  rendimento = float(dados.get("rendimento", 0.85))  # eta (0.1 a 1.0)
  sistema = dados.get(
      "sistema", "monofasico"
  )  # 'monofasico', 'bifasico', 'trifasico'
  material_fio = dados.get("material_fio", "cobre")
  seccao_fio_mm2 = float(dados.get("seccao_fio", 2.5))  # mm²
  comprimento_fio = float(dados.get("comprimento_fio", 20.0))  # metros (m)

  prop_material = MATERIAIS_CONDUTORES.get(
      material_fio, MATERIAIS_CONDUTORES["cobre"]
  )
  rho = prop_material["resistividade"]

  # 1. Cálculo da Corrente Nominal (I) conforme o Sistema Elétrico
  if sistema == "trifasico":
    # I = P / (V * sqrt(3) * FP * rendimento)
    corrente = (
        potencia_w / (tensao * math.sqrt(3) * fator_potencia * rendimento)
        if tensao > 0
        else 0
    )
    fator_distancia = math.sqrt(3)  # Queda de tensão trifásica
  elif sistema == "bifasico":
    corrente = (
        potencia_w / (tensao * fator_potencia * rendimento)
        if tensao > 0
        else 0
    )
    fator_distancia = 2.0  # Queda de tensão fiação ida e volta
  else:  # monofasico
    corrente = (
        potencia_w / (tensao * fator_potencia * rendimento)
        if tensao > 0
        else 0
    )
    fator_distancia = 2.0

  # 2. Resistência dos Condutores, Carga (Chuveiro/Equipamento) e Total
  resistencia_fio = (rho * comprimento_fio * fator_distancia) / seccao_fio_mm2
  resistencia_carga = (tensao / corrente) if corrente > 0 else 0.0
  resistencia_total = resistencia_fio + resistencia_carga

  # 3. Queda de Tensão (ΔV) e Percentual (NBR 5410)
  queda_tensao_v = corrente * resistencia_fio
  percentual_queda = (queda_tensao_v / tensao) * 100 if tensao > 0 else 0
  tensao_na_carga = max(0.0, tensao - queda_tensao_v)

  # 4. Potência Perfeita e Perda por Efeito Joule
  potencia_perda_fio = (corrente**2) * resistencia_fio

  # 5. Aquecimento dos Condutores
  temp_ambiente = 25.0
  dissipacao_metro = (
      potencia_perda_fio / (comprimento_fio * fator_distancia)
      if comprimento_fio > 0
      else 0
  )
  temp_fio = temp_ambiente + (
      dissipacao_metro * 10.0 / math.sqrt(seccao_fio_mm2)
  )

  # 6. Diagnóstico do Circuito
  estado_circuito = "normal"
  mensagem = "CIRCUITO OPERACIONAL (DENTRO DA NORMA NBR 5410)"

  if temp_fio >= prop_material["temp_fusao"]:
    estado_circuito = "fusao_fio"
    mensagem = (
        f"CURTO-CIRCUITO CRÍTICO! CONDUTOR DE {prop_material['nome'].upper()}"
        " DERRETEU!"
    )
  elif percentual_queda > 4.0:
    estado_circuito = "queda_tensao_alta"
    mensagem = (
        f"ALERTA NBR 5410: QUEDA DE TENSÃO ELEVADA ({percentual_queda:.1f}%)."
        " AUMENTE A BITOLA!"
    )
  elif corrente > (seccao_fio_mm2 * 9.5):
    estado_circuito = "sobrecarga"
    mensagem = "SOBRECARGA: DENSIDADE DE CORRENTE EXCESSIVA NO CABO!"

  velocidade_eletrons = min(corrente * 0.04, 3.0)

  return jsonify({
      "status": "ok",
      "resultados": {
          "tensao_fonte_v": round(tensao, 1),
          "tensao_carga_v": round(tensao_na_carga, 1),
          "potencia_w": round(potencia_w, 1),
          "corrente_a": round(corrente, 2),
          "amperagem": round(corrente, 2),
          "resistencia_fio_ohm": round(resistencia_fio, 4),
          "resistencia_carga_ohm": round(resistencia_carga, 2),
          "resistencia_total_ohm": round(resistencia_total, 2),
          "potencia_perda_fio_w": round(potencia_perda_fio, 1),
          "queda_tensao_v": round(queda_tensao_v, 2),
          "percentual_queda_tensao": round(percentual_queda, 2),
          "temp_fio_c": round(temp_fio, 1),
          "velocidade_eletrons": round(velocidade_eletrons, 3),
          "estado_circuito": estado_circuito,
          "mensagem": mensagem,
      },
  })


if __name__ == "__main__":
  print("Servidor QuanticaCircuits 3D iniciado em http://127.0.0.1:5001")
  app.run(debug=True, port=5001)