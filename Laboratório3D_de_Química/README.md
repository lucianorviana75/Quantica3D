### Por que Python + Web 3D?

O Python é excelente para processar **fórmulas físico-químicas, estequiometria, equilíbrio químico, termodinâmica e cálculo de pH**.
Para renderizar em **3D interativo** no navegador, usamos **JavaScript + Three.js** conectado ao servidor Python.

## 🏗️ Estrutura do Projeto no VS Code

Crie uma pasta para o seu projeto no VS Code com a seguinte estrutura:

simulador-quimica/
├── app.py                 # Servidor Flask com a lógica físico-química
├── requirements.txt       # Dependências Python
└── templates/
└── index.html         # Interface Web 3D com Three.js e controles

## 🛠️ Passo 1: Instalação das Dependências Python

No terminal do VS Code, crie e ative o ambiente virtual (opcional, mas recomendado) e instale o **Flask**:

pip install flask

# 🧪 Tabela Periódica Interativa (Web App)

Uma aplicação web completa e responsiva para consulta e visualização da Tabela Periódica dos Elementos Químicos. A interface possui um layout dividido onde a Tabela Periódica é renderizada dinamicamente no **lado direito da tela** via CSS Grid/Flexbox, enquanto o **lado esquerdo** exibe um painel interativo de detalhes, busca e filtros por categoria.

## 📑 Tabela de Conteúdos

- Visão Geral
- Funcionalidades Principais
- Estrutura do Projeto
- Requisitos do Sistema
- Instalação e Configuração
- Como Executar
- Documentação da API (Endpoints)
- Estrutura do Banco de Dados (JSON)
- Detalhamento do Front-end (Layout à Direita)
- Estilização e Categorias (CSS)
- Testes
- Licença

## 👁️ Visão Geral

O projeto foi construído para fornecer uma ferramenta de estudo e consulta rápida. O backend em Python (Flask) serve os dados padronizados a partir de um arquivo JSON estruturado, enquanto o front-end processa as posições $(x, y)$ de cada elemento para montar a grade periódica padrão (18 colunas por 10 linhas), destacando os blocos de Lantanídeos, Actinídeos e até os elementos sintéticos/hipotéticos ($119$ e $120$).

## ✨ Funcionalidades Principais

1. **Grid Dinâmico no Lado Direito:** Renderização automatizada da tabela respeitando `xpos` e `ypos`.
2. **Painel de Detalhes no Lado Esquerdo:** Exibição imediata ao clicar ou passar o mouse em um elemento (Massa, Ponto de Fusão, Ebulição, Categoria e Número Atômico).
3. **Filtro por Categorias:** Destaque visual por grupos (*metais de transição*, *gases nobres*, *halogênios*, etc.).
4. **Barra de Busca Instantânea:** Busca em tempo real por nome, símbolo ou número atômico.
5. **Suporte a Temas e Responsividade:** Ajuste de escala para diferentes resoluções de tela.

## 📁 Estrutura do Projeto

Plaintext

```
tabela-periodica-app/
│
├── app.py                      # Servidor Flask e rotas da aplicação
├── tabela_periodica.json       # Base de dados estruturada dos elementos (1-120)
├── requirements.txt            # Dependências Python do projeto
├── README.md                   # Documentação completa do projeto
│
├── static/
│   ├── css/
│   │   ├── layout.css          # Estrutura flexbox do painel principal
│   │   ├── grid.css            # Regras do CSS Grid da Tabela Periódica
│   │   └── categories.css      # Cores e estilos por categoria química
│   └── js/
│       ├── main.js             # Inicialização e chamadas de API
│       ├── gridRenderer.js     # Lógica de renderização das células no Grid
│       └── detailsPanel.js     # Atualização do painel esquerdo ao clicar
│
└── templates/
    └── index.html              # Template HTML principal
```

## ⚙️ Requisitos do Sistema

- **Python:** 3.8 ou superior
- **Gerenciador de Pacotes:** `pip`
- **Navegador Web:** Google Chrome, Mozilla Firefox, Safari ou Edge com suporte a CSS Grid.

## 🛠️ Instalação e Configuração

### 1. Clonar ou Baixar o Repositório

Bash

```
git clone https://github.com/seu-usuario/tabela-periodica-app.git
cd tabela-periodica-app
```

### 2. Criar e Ativar um Ambiente Virtual (Recomendado)

- **Linux / macOS:**Bash
    
    ```
    python3 -m venv venv
    source venv/bin/venv/bin/activate
    ```
    
- **Windows:**DOS
    
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
    

### 3. Instalar Dependências

Crie um arquivo `requirements.txt` com o seguinte conteúdo se ainda não houver:

Plaintext

```
Flask==3.0.2
```

Instale executando:

Bash

```
pip install -r requirements.txt
```

## 🚀 Como Executar

1. Inicie o servidor Flask executando o arquivo `app.py`:Bash
    
    ```
    python app.py
    ```
    
2. Abra o navegador e acesse:Plaintext
    
    ```
    http://127.0.0.1:5000
    ```
    

## 🔌 Documentação da API (Endpoints)

O backend disponibiliza os seguintes endpoints RESTful:

| **Método** | **Endpoint** | **Descrição** |
| --- | --- | --- |
| `GET` | `/` | Retorna a página principal (`index.html`). |
| `GET` | `/api/elementos` | Retorna o JSON completo com todos os elementos. |
| `GET` | `/api/elemento/<simbolo>` | Retorna os detalhes de um elemento específico (ex: `/api/elemento/Fe`). |

### Exemplo de Resposta (`GET /api/elemento/Fe`):

JSON

```
{
  "numero": 26,
  "simbolo": "Fe",
  "nome": "Ferro",
  "categoria": "metal_transicao",
  "fusao": 1538,
  "ebulicao": 2862,
  "xpos": 8,
  "ypos": 4
}
```

## 🗄️ Estrutura do Banco de Dados (JSON)

Cada elemento dentro de `tabela_periodica.json` segue a chave padrão do seu **Símbolo Químico**:

JSON

```
{
  "H": {
    "numero": 1,
    "simbolo": "H",
    "nome": "Hidrogênio",
    "categoria": "nao_metal",
    "fusao": -259.1,
    "ebulicao": -252.9,
    "xpos": 1,
    "ypos": 1
  }
}
```

## 📐 Detalhamento do Front-end (Layout à Direita)

### 1. Estrutura Dividida (`static/css/layout.css`)

Inverte a distribuição padrão da tela dividindo-a em um painel esquerdo (informações) e um painel direito (tabela):

CSS

```
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #0f172a;
  color: #f8fafc;
}

.app-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Lado Esquerdo: 30% da largura */
.painel-esquerdo {
  flex: 0 0 30%;
  padding: 24px;
  background-color: #1e293b;
  border-right: 2px solid #334155;
  overflow-y: auto;
}

/* Lado Direito: 70% da largura - Contém a Tabela */
.painel-direito {
  flex: 0 0 70%;
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: auto;
}
```

### 2. Grid CSS da Tabela (`static/css/grid.css`)

CSS

```
.tabela-grid {
  display: grid;
  grid-template-columns: repeat(18, minmax(40px, 1fr));
  grid-template-rows: repeat(10, minmax(40px, 1fr));
  gap: 6px;
  width: 100%;
  max-width: 1200px;
}

.card-elemento {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 4px;
  border-radius: 6px;
  background-color: #334155;
  cursor: pointer;
  user-select: none;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.card-elemento:hover {
  transform: scale(1.15);
  z-index: 20;
  box-shadow: 0 8px 16px rgba(0,0,0,0.4);
}

.card-elemento .num { font-size: 0.7rem; color: #94a3b8; }
.card-elemento .simbolo { font-size: 1.1rem; font-weight: bold; text-align: center; }
.card-elemento .nome { font-size: 0.6rem; text-align: center; text-overflow: ellipsis; overflow: hidden; }
```

### 3. Código do Servidor (`app.py`)

Python

```
from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

def carregar_dados():
    caminho = os.path.join(app.root_path, 'tabela_periodica.json')
    with open(caminho, 'r', encoding='utf-8') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/elementos')
def get_elementos():
    dados = carregar_dados()
    return jsonify(dados)

@app.route('/api/elemento/<simbolo>')
def get_elemento(simbolo):
    dados = carregar_dados()
    elemento = dados.get(simbolo)
    if elemento:
        return jsonify(elemento)
    return jsonify({"erro": "Elemento não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🎨 Estilização e Categorias (CSS)

Cores atribuídas a cada categoria química no arquivo `static/css/categories.css`:

CSS

```
.nao_metal          { background-color: #22c55e; color: #fff; }
.gas_nobre          { background-color: #a855f7; color: #fff; }
.metal_alcalino     { background-color: #ef4444; color: #fff; }
.alcalino_terroso   { background-color: #f97316; color: #fff; }
.semimetal          { background-color: #14b8a6; color: #fff; }
.halogenio          { background-color: #06b6d4; color: #fff; }
.metal_transicao    { background-color: #3b82f6; color: #fff; }
.metal_pos_transicao{ background-color: #64748b; color: #fff; }
.lantanideo         { background-color: #ec4899; color: #fff; }
.actinideo          { background-color: #d946ef; color: #fff; }
```

## 🧪 Testes

Para garantir o correto carregamento do JSON e funcionamento dos endpoints, crie um arquivo `test_app.py`:

Python

```
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_status_code_home(client):
    resposta = client.get('/')
    assert resposta.status_code == 200

def test_api_elementos(client):
    resposta = client.get('/api/elementos')
    assert resposta.status_code == 200
    assert 'H' in resposta.get_json()
```

Execute os testes com o comando:

Bash

```
pytest
```

## 📜 Licença

Este projeto está sob a licença **MIT**. Sinta-se livre para modificar e distribuir conforme necessário.