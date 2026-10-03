# 🧪 Quantica3D — Simulação Físico-Química
🚀 **Acesse o Simulador Quântico 3D online:**
[https://quantica3d.onrender.com](https://quantica3d.onrender.com)


O **Quantica3D** é uma aplicação web construída com **Flask** que simula o comportamento físico e químico de gases ideais contidos em vasos de pressão de diferentes materiais e geometrias. 

A aplicação calcula a pressão interna, a tensão mecânica nas paredes do recipiente e determina o estado do sistema (estabilidade, risco de explosão por sobrepressão, congelamento ou corrosão química).

---

## 🚀 Funcionalidades

- **Cálculo da Equação dos Gases Ideais:** Determina a pressão interna com base na massa do elemento/composto, temperatura e volume.
- **Análise de Tensão Mecânica em Paredes Finas:** Calcula a tensão de fratura e compara com o limite de resistência do material escolhido.
- **Detecção de Efeitos Físico-Químicos:**
  - 💥 **Explosão:** Ruptura mecânica quando o estresse atinge 100%.
  - ❄️ **Congelamento:** Cristalização para temperaturas inferiores a -10 °C.
  - 🧪 **Corrosão:** Reação de incompatibilidade entre halogénios e metais.
- **API RESTful JSON:** Pronta para integração com interfaces e renderizadores 3D no front-end.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.x
- **Framework Web:** Flask
- **Matemática/Física:** Módulo nativo `math` de Python

---

## 📂 Estrutura do Projeto

Quantica3D/
│
├── app.py              # Ficheiro principal do servidor Flask e lógica do backend
├── templates/
│   └── index.html      # Interface web / Visualizador 3D
├── venv/               # Ambiente virtual Python
└── README.md           # Documentação do projeto

---

## 📋 Pré-requisitos e Instalação do Python

Antes de executar o projeto, precisas do **Python 3.8+** e do **pip** instalados no teu sistema.

### 🐧 Ubuntu / Debian (Linux)
Executa no terminal para instalar o Python, o gestor de pacotes `pip` e o módulo `venv`:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y### 🪟 Windows

1. Transfere o instalador no site oficial: https://www.python.org/downloads/
2. **Importante:** Marcar a opção **"Add Python to PATH"** durante a instalação.
3. O `pip` e o `venv` já vêm incluídos por padrão no instalador do Windows.

### 🍎 macOS

Podes instalar através do Homebrew no terminal:

Bash

```
brew install python
```

## 🔧 Passo a Passo de Execução do Projeto

### 1. Aceder ao Diretório do Projeto

Abre o terminal e navega até à pasta do projeto:

Bash

```
cd Quantica3D
```

### 2. Criar e Ativar o Ambiente Virtual (`venv`)

- **No Linux / macOS:**Bash
    
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
    
- **No Windows (PowerShell / Prompt):**PowerShell
    
    ```
    python -m venv venv
    venv\Scripts\activate
    ```
    

*(Nota: Quando o ambiente estiver ativo, verás `(venv)` no início da linha do terminal).*

### 3. Instalar as Dependências

Com o ambiente virtual ativo, instala o **Flask**:

Bash

```
pip install flask
```

### 4. Executar a Aplicação

Inicia o servidor de desenvolvimento:

Bash

```
python app.py
```

Após executar o comando, verás uma mensagem no terminal:

Plaintext

```
Servidor Quantica3D iniciado com sucesso!
 * Running on http://127.0.0.1:5000
```

### 5. Aceder no Navegador

Abre o teu navegador e acede ao endereço:

👉 **http://127.0.0.1:5000**

## 📡 Endpoints da API

| **Método** | **Rota** | **Descrição** |
| --- | --- | --- |
| `GET` | `/` | Renderiza a página principal (`index.html`). |
| `GET` | `/api/elementos` | Retorna a lista de elementos químicos e materiais suportados. |
| `POST` | `/api/calcular` | Executa os cálculos físicos/químicos e devolve os resultados e alertas. |

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de simulação.

```

---

### 💡 Dica no VS Code ao colar:
No VS Code, para garantir que cola sem formatação de estilos ou perdas de quebras de linha, podes usar a atalho de colar texto puro:
- **Linux/Windows:** `Ctrl + Shift + V`
- **Mac:** `Cmd + Shift + V`
```
🚀 **Acesse o Simulador Quântico 3D online:**
[https://quantica3d.onrender.com](https://quantica3d.onrender.com)
