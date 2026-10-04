# ⚡ QuanticaCircuits 3D - Simulador de Circuitos Elétricos

* ⚡ **Simulador de Circuitos Elétricos 3D:**
  [https://circuitos-eletricos-3d.onrender.com](https://circuitos-eletricos-3d.onrender.com)


O **QuanticaCircuits 3D** é uma aplicação web desenvolvida em Python e Flask para cálculo, dimensionamento e verificação de circuitos elétricos residenciais, prediais e industriais, alinhada com as normas da **NBR 5410**.

A aplicação permite simular o comportamento de condutores em circuitos monofásicos, bifásicos e trifásicos, calculando perdas por efeito Joule, aquecimento do condutor, queda de tensão e emitindo diagnósticos automáticos de segurança.

## 💻 Estrutura do Projeto

Plaintext

```
Quantica3D/
├── Simulador_circuitos_eletricos3D/
│   ├── templates/
│   │   └── circuito.html       # Interface HTML e visualização do simulador
│   └── app_eletrica.py         # Servidor Flask e motor de cálculo elétrico
├── Simulador_quantico3D/       # Módulo complementar 3D
└── venv/                       # Ambiente virtual Python
```

## 🚀 Funcionalidades

- **Sistemas Elétricos:** Suporte a circuitos Monofásicos, Bifásicos e Trifásicos.
- **Dimensionamento de Condutores:** Materiais normatizados (**Cobre** e **Alumínio**) com bitolas padrão de $1.5\text{ mm}^2$ a $240\text{ mm}^2$.
- **Análise Elétrica & Térmica:**
    - Cálculo de Corrente Nominal ($I$), Relação de Resistências e Queda de Tensão ($\Delta V$).
    - Estimativa do aquecimento do cabo e velocidade de derivação dos eletrões.
    - Alerta de risco de fusão/curto-circuito.
- **Diagnósticos NBR 5410:** Avisos em tempo real para quedas de tensão superiores a 4% ou densidade excessiva de corrente.
- **API RESTful:** Endpoints JSON para envio de parâmetros e receção de diagnósticos instantâneos.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (renderizado via Jinja2 templates)
- **Matemática & Física:** Módulo standard `math` para equações elétricas

## 🔧 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior instalado.

### Passo a Passo

1. **Aceda à pasta do simulador elétrico:**Bash
    
    ```
    cd Quantica3D/Simulador_circuitos_eletricos3D
    ```
    
2. **Ative o ambiente virtual (`venv`):**
    - **Linux / macOS:**Bash
        
        ```
        source ../venv/bin/activate
        ```
        
    - **Windows:**DOS
        
        ```
        ..\venv\Scripts\activate
        ```
        
3. **Instale as dependências (caso necessário):**Bash
    
    ```
    pip install flask
    ```
    
4. **Inicie o servidor Flask:**Bash
    
    ```
    python app_eletrica.py
    ```
    
5. **Aceda no navegador:**
Abra o endereço http://127.0.0.1:5001 para utilizar a interface.

## 📡 Endpoints da API

### `GET /api/dados_iniciais`

Retorna a lista de materiais disponíveis e as bitolas normatizadas pela NBR 5410.

### `POST /api/calcular_circuito`

Recebe as especificações do circuito em formato JSON e devolve a análise técnica detalhada.

**Exemplo de Pedido (Body JSON):**

JSON

```
{
  "tensao": 220.0,
  "potencia_w": 5000.0,
  "fator_potencia": 0.85,
  "rendimento": 0.85,
  "sistema": "monofasico",
  "material_fio": "cobre",
  "seccao_fio": 2.5,
  "comprimento_fio": 20.0
}
```

**Exemplo de Resposta (JSON):**

JSON

```
{
  "status": "ok",
  "resultados": {
    "tensao_fonte_v": 220.0,
    "tensao_carga_v": 211.8,
    "potencia_w": 5000.0,
    "corrente_a": 31.48,
    "resistencia_fio_ohm": 0.2608,
    "resistencia_carga_ohm": 6.99,
    "resistencia_total_ohm": 7.25,
    "potencia_perda_fio_w": 258.4,
    "queda_tensao_v": 8.21,
    "percentual_queda_tensao": 3.73,
    "temp_fio_c": 65.9,
    "velocidade_eletrons": 1.259,
    "estado_circuito": "normal",
    "mensagem": "CIRCUITO OPERACIONAL (DENTRO DA NORMA NBR 5410)"
  }
}
```

## 📜 Licença

Projeto desenvolvido para fins educacionais e de simulação técnica.
