from flask import Flask, render_template, request, jsonify
from collections import Counter
from functools import lru_cache
import requests
import json
import os

app = Flask(__name__)

def carregar_tabela_periodica():
    caminho = os.path.join(os.path.dirname(__file__), 'tabela_periodica.json')
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

ELEMENTOS = carregar_tabela_periodica()
historico = []

# Cache com lru_cache para evitar requisições lentas repetidas à API do PubChem
@lru_cache(maxsize=128)
def consultar_pubchem(formula_hill):
    url_composto = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/formula/{formula_hill}/property/Title,IUPACName,MolecularWeight/JSON"
    
    try:
        # Timeout reduzido para 1 segundo para o servidor não travar
        resp = requests.get(url_composto, timeout=1.0)
        if resp.status_code != 200:
            return None
        
        dados = resp.json()['PropertyTable']['Properties'][0]
        cid = dados['CID']
        nome = dados.get('Title', formula_hill)
        
        url_perigos = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON?heading=GHS+Classification"
        resp_ghs = requests.get(url_perigos, timeout=1.0)
        
        eh_explosivo, eh_inflamavel, eh_corrosivo = False, False, False
        
        if resp_ghs.status_code == 200:
            texto_ghs = resp_ghs.text.lower()
            eh_explosivo = 'explosive' in texto_ghs or 'unstable explosive' in texto_ghs
            eh_inflamavel = 'flammable' in texto_ghs or 'pyrophoric' in texto_ghs
            eh_corrosivo = 'corrosive' in texto_ghs or 'skin corrosion' in texto_ghs

        return {
            'cid': cid,
            'nome': nome,
            'peso': dados.get('MolecularWeight', 0),
            'explosivo': eh_explosivo,
            'inflamavel': eh_inflamavel,
            'corrosivo': eh_corrosivo
        }
    except Exception:
        return None

def gerar_formula_hill(contagem_elementos):
    elementos = list(contagem_elementos.keys())
    resultado = []
    
    if 'C' in elementos:
        resultado.append(f"C{contagem_elementos['C'] if contagem_elementos['C'] > 1 else ''}")
        elementos.remove('C')
        if 'H' in elementos:
            resultado.append(f"H{contagem_elementos['H'] if contagem_elementos['H'] > 1 else ''}")
            elementos.remove('H')
            
    for elem in sorted(elementos):
        qtd = contagem_elementos[elem]
        resultado.append(f"{elem}{qtd if qtd > 1 else ''}")
        
    return "".join(resultado)

@app.route('/')
def home():
    elementos_ordenados = dict(sorted(ELEMENTOS.items(), key=lambda x: x[1]['numero']))
    return render_template('index.html', elementos=elementos_ordenados)

@app.route('/calcular', methods=['POST'])
def calcular():
    global historico
    data = request.get_json()
    
    acao = data.get('acao')
    temp_usuario = float(data.get('temperatura', 25))

    if acao == 'adicionar':
        elem_id = data.get('substancia')
        qtd = float(data.get('volume', 10))
        if elem_id in ELEMENTOS:
            historico.append({'id': elem_id, 'qtd': qtd})
    elif acao == 'desfazer' and historico:
        historico.pop()
    elif acao == 'limpar':
        historico = []

    if not historico:
        return jsonify({
            'volume': 0, 
            'temperatura': temp_usuario,
            'explicacao': 'Selecione elementos da tabela periódica.', 
            'itens': [],
            'gerar_gas': False,
            'explodir': False,
            'perigo': 'NENHUM',
            'cor_perigo': '#22c55e',
            'estado': 'liquido'
        })

    vol_total = sum(item['qtd'] for item in historico)
    contagem = Counter(item['id'] for item in historico)
    
    explicacao = []
    gerar_gas = False
    explodir = False
    nivel_perigo = "NENHUM"
    cor_perigo = "#22c55e"
    composto_estavel_formado = False
    estado_geral = 'liquido'

    # --- 1. REGRAS DE REAÇÃO ESPECÍFICAS ---
    
    # Sintese de Água (H2O)
    if contagem['H'] == 2 and contagem['O'] == 1 and len(contagem) == 2:
        explicacao.append("💧 REAÇÃO DE SÍNTESE: Formação de Água (H₂O) no béquer!")
        composto_estavel_formado = True
        if temp_usuario < 0:
            estado_geral = 'solido'
            explicacao.append(f"🧊 A água congelou a {temp_usuario} °C (Gelo).")
            gerar_gas = False
        elif temp_usuario >= 100:
            estado_geral = 'gasoso'
            explicacao.append(f"💨 A água evaporou a {temp_usuario} °C (Vapor de água).")
            gerar_gas = True
        else:
            estado_geral = 'liquido'
            explicacao.append(f"💧 A água encontra-se no estado LÍQUIDO a {temp_usuario} °C.")
            gerar_gas = False

    # Sintese de Hidreto de Potássio (KH)
    elif contagem['H'] == 1 and contagem['K'] == 1 and len(contagem) == 2:
        explicacao.append("🧪 REAÇÃO DE SÍNTESE: Formação de Hidreto de Potássio (KH)!")
        composto_estavel_formado = True
        if temp_usuario < 400:
            estado_geral = 'solido'
            explicacao.append(f"🧊 O Hidreto de Potássio (KH) é um sólido cristalino a {temp_usuario} °C.")
            gerar_gas = False
        else:
            estado_geral = 'gasoso'
            explicacao.append(f"🔥 A {temp_usuario} °C, o KH decompõe-se e vaporiza.")
            gerar_gas = True

    # Explosão H2 + O2 em proporção alta
    elif contagem['H'] >= 2 and contagem['O'] >= 2:
        explicacao.append("💥 EXPLOSÃO! Ignição da mistura gasosa de H₂ e O₂!")
        explodir = True
        gerar_gas = True
        estado_geral = 'gasoso'
        nivel_perigo = "EXTREMO - EXPLOSÃO"
        cor_perigo = "#dc2626"

    # Metal alcalino com excesso de água/hidrogénio
    elif any(elem in contagem for elem in ['Na', 'K', 'Cs', 'Rb', 'Fr']) and contagem['H'] > 1:
        explicacao.append("💥 EXPLOSÃO VIOLENTA! Reação com excesso de Hidrogénio/Água!")
        explodir = True
        gerar_gas = True
        estado_geral = 'gasoso'
        nivel_perigo = "EXTREMO - EXPLOSÃO"
        cor_perigo = "#dc2626"

    # --- 2. CÁLCULO DE FUSÃO/EBULIÇÃO PARA ELEMENTOS ISOLADOS ---
    if not composto_estavel_formado and not explodir:
        estados_elementos = []
        for item in historico:
            elem = ELEMENTOS.get(item['id'])
            if elem:
                pf = elem.get('fusao', 0)
                pe = elem.get('ebulicao', 100)

                if temp_usuario >= pe:
                    explicacao.append(f"💨 {elem['nome']} ({elem['simbolo']}) evaporou a {pe} °C (GASOSO).")
                    estados_elementos.append('gasoso')
                    gerar_gas = True
                elif temp_usuario < pf:
                    explicacao.append(f"🧊 {elem['nome']} ({elem['simbolo']}) congelou/solidificou a {pf} °C (SÓLIDO).")
                    estados_elementos.append('solido')
                else:
                    estados_elementos.append('liquido')

        if 'gasoso' in estados_elementos and not ('liquido' in estados_elementos or 'solido' in estados_elementos):
            estado_geral = 'gasoso'
        elif 'solido' in estados_elementos and 'liquido' not in estados_elementos:
            estado_geral = 'solido'
        else:
            estado_geral = 'liquido'

    # --- 3. CONSULTA AO PUBCHEM ---
    formula = gerar_formula_hill(contagem)
    dados_composto = consultar_pubchem(formula)

    if dados_composto:
        explicacao.append(f"\n🧪 Base PubChem: {dados_composto['nome']} (CID: {dados_composto['cid']})")
    else:
        explicacao.append(f"\n⚗️ Proporção ({formula}): Mistura livre de elementos.")

    lista_itens = [f"{ELEMENTOS[i['id']]['nome']} ({ELEMENTOS[i['id']]['simbolo']}) - {i['qtd']} g/mL" for i in historico if i['id'] in ELEMENTOS]

    return jsonify({
        'volume': vol_total,
        'temperatura': round(temp_usuario, 1),
        'gerar_gas': gerar_gas,
        'explodir': explodir,
        'perigo': nivel_perigo,
        'cor_perigo': cor_perigo,
        'estado': estado_geral,
        'explicacao': "\n".join(explicacao),
        'itens': lista_itens
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)