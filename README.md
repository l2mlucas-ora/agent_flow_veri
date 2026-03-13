# 🔒 Verisure Oracle Fusion Cloud ERP – Agent

Agente conversacional especialista nos fluxos de processos do **Oracle Fusion Cloud ERP** da **Verisure Brasil**, construído com [LangChain](https://www.langchain.com/) + [OpenAI](https://openai.com/).

---

## 📋 Funcionalidades

- **Consulta de processos por módulo** – Financials, Procurement, Supply Chain, HCM, Projects
- **Busca por palavra-chave** – encontre processos por tema (ex: "fechamento contábil")
- **Detalhes passo a passo** – etapas completas de cada processo
- **Papéis e responsabilidades** – quem faz o quê em cada fluxo
- **Notas específicas da Verisure** – configurações, alçadas e regras de negócio locais
- **Pontos de integração** – como cada módulo se conecta com os outros
- **Interface interativa** via CLI (modo chat) ou query única

---

## 🗂️ Estrutura do Projeto

```
agent_flow_veri/
├── .env.example              # Template de variáveis de ambiente
├── .gitignore
├── requirements.txt          # Dependências Python
├── config.py                 # Configurações (carregadas do .env)
├── knowledge_base/
│   ├── __init__.py
│   └── oracle_processes.py   # Base de conhecimento dos processos ERP
├── tools.py                  # LangChain tools para consulta à base de conhecimento
├── agent.py                  # Construção do agente ReAct (LangChain)
├── main.py                   # CLI entrypoint
└── tests/
    ├── __init__.py
    └── test_agent.py         # Testes unitários
```

---

## 🚀 Instalação e Configuração

### 1. Pré-requisitos

- Python 3.11+
- Chave de API da OpenAI ([obter aqui](https://platform.openai.com/api-keys))

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env e preencha sua OPENAI_API_KEY
```

Variáveis disponíveis:

| Variável          | Descrição                                 | Padrão         |
|-------------------|-------------------------------------------|----------------|
| `OPENAI_API_KEY`  | Chave da API OpenAI (**obrigatório**)      | –              |
| `OPENAI_MODEL`    | Modelo OpenAI a utilizar                  | `gpt-4o-mini`  |
| `LLM_TEMPERATURE` | Temperatura do LLM (0.0 = determinístico) | `0.0`          |
| `VECTORSTORE_DIR` | Diretório para persistência do vetor store | `./vectorstore`|

---

## 💬 Uso

### Modo interativo (chat)

```bash
python main.py
```

### Consulta única

```bash
python main.py --query "Como funciona o processo de contas a pagar na Verisure?"
```

### Listar todos os módulos e processos

```bash
python main.py --list-modules
```

### Modo verboso (exibe o raciocínio ReAct do agente)

```bash
python main.py --verbose
```

---

## 📚 Base de Conhecimento

A base de conhecimento cobre os seguintes módulos e processos:

### 💰 Financials
| ID         | Processo                                             |
|------------|------------------------------------------------------|
| `fi-ap-01` | Ciclo Completo de Contas a Pagar (P2P)               |
| `fi-ar-01` | Ciclo de Contas a Receber – Faturamento e Cobrança   |
| `fi-gl-01` | Fechamento Contábil Mensal (Period Close)             |
| `fi-fa-01` | Gestão de Ativos Fixos – Adição, Depreciação e Baixa |
| `fi-bc-01` | Controle Orçamentário – Budget Check e Variâncias    |
| `fi-ex-01` | Gestão de Despesas de Viagem e Reembolso             |

### 🛒 Procurement
| ID          | Processo                                          |
|-------------|---------------------------------------------------|
| `scm-po-01` | Compras – Requisição até Ordem de Compra (P2P)   |

### 📦 Supply Chain
| ID           | Processo                                        |
|--------------|-------------------------------------------------|
| `scm-inv-01` | Gestão de Estoque – Recebimento e Inventário   |

### 📊 Project Portfolio Management
| ID         | Processo                                                |
|------------|---------------------------------------------------------|
| `ppm-pc-01`| Gestão de Custos de Projetos – Instalação de Sistemas  |

### 👥 Human Capital Management
| ID          | Processo                                      |
|-------------|-----------------------------------------------|
| `hcm-hr-01` | Admissão de Colaboradores (Hire-to-Retire)   |
| `hcm-py-01` | Processamento de Folha de Pagamento Mensal   |

---

## 🧪 Testes

Os testes unitários **não requerem conexão com a OpenAI** e validam:
- Integridade da base de conhecimento
- Funções de busca e filtragem
- Outputs das ferramentas LangChain

```bash
pytest tests/ -v
```

---

## 🔧 Exemplos de Perguntas

```
Como funciona o processo de contas a pagar na Verisure?
Quais são os passos para o fechamento contábil mensal?
Quem aprova as ordens de compra acima de R$ 100.000?
Como é feito o inventário de estoque de equipamentos de alarme?
Quais módulos do Oracle ERP a Verisure utiliza?
Descreva o processo de admissão de um novo técnico de campo.
Quais são as regras específicas da Verisure para despesas de viagem?
Como funciona a folha de pagamento e o cálculo de FGTS?
Qual é o processo de baixa de ativos fixos (equipamentos)?
Como funciona o controle orçamentário para CAPEX?
```

---

## 🛠️ Arquitetura

```
Usuário (CLI)
     │
     ▼
  main.py  ──► build_agent() (agent.py)
                      │
                      ▼
          AgentExecutor (LangChain ReAct)
                      │
              ┌───────┴───────┐
              │               │
          ChatOpenAI      Tools (tools.py)
          (OpenAI API)        │
                              ▼
                    Knowledge Base
                  (oracle_processes.py)
```

O agente utiliza a estratégia **ReAct** (Reasoning + Acting): para cada pergunta, raciocina sobre qual ferramenta usar, executa a ferramenta, observa o resultado e repete até chegar à resposta final.

---

## 📄 Licença

Uso interno – Verisure Brasil.
