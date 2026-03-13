# Agente Oracle Fusion Cloud ERP – Verisure

Agente de IA especialista nos **fluxos de processos do Oracle Fusion Cloud ERP**
implementado no cliente **Verisure**.

O agente responde em Português (Brasil) a perguntas sobre processos de negócio,
etapas de execução, papéis envolvidos e particularidades de configuração
específicas da Verisure.

---

## Módulos cobertos

| Módulo | ID dos processos |
|---|---|
| Accounts Payable | AP-001, AP-002 |
| Accounts Receivable | AR-001, AR-002 |
| General Ledger | GL-001 |
| Procurement | PO-001, PO-002 |
| Order Management | OM-001 |
| Inventory Management | INV-001 |
| Fixed Assets | FA-001 |
| Cash Management | CM-001 |
| Human Capital Management | HCM-001, HCM-002 |
| Project Portfolio Management | PPM-001 |

---

## Pré-requisitos

- Python 3.12+
- Uma chave de API OpenAI (`OPENAI_API_KEY`)

---

## Instalação

```bash
# Clonar o repositório
git clone https://github.com/l2mlucas-ora/agent_flow_veri.git
cd agent_flow_veri

# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

---

## Configuração

Crie um arquivo `.env` na raiz do projeto (nunca comite este arquivo):

```env
OPENAI_API_KEY=sk-...
MODEL_NAME=gpt-4o          # opcional, padrão: gpt-4o
TEMPERATURE=0              # opcional, padrão: 0
VERBOSE=false              # opcional, mostrar raciocínio do agente
MAX_ITERATIONS=10          # opcional
```

---

## Uso

### Modo interativo (chat)

```bash
python main.py
```

### Pergunta única via linha de comando

```bash
python main.py "Quais são as etapas do fechamento contábil mensal?"
```

### Como biblioteca Python

```python
from agent import ask

resposta = ask("Explique o processo Procure-to-Pay para compra de equipamentos de alarme.")
print(resposta)
```

---

## Ferramentas do agente

O agente dispõe das seguintes ferramentas para consultar a base de conhecimento:

| Ferramenta | Descrição |
|---|---|
| `list_modules` | Lista todos os módulos Oracle disponíveis |
| `list_processes_by_module` | Lista processos de um módulo específico |
| `get_process_detail` | Detalhes completos de um processo por ID |
| `search_processes` | Busca processos por palavra-chave |
| `list_all_processes` | Lista todos os processos agrupados por módulo |
| `get_roles_for_process` | Papéis envolvidos em um processo |

---

## Estrutura do projeto

```
agent_flow_veri/
├── knowledge_base/
│   ├── __init__.py
│   └── process_flows.py     # Base de conhecimento dos fluxos de processo
├── tests/
│   ├── __init__.py
│   ├── test_knowledge_base.py
│   └── test_tools.py
├── agent.py                 # Construção do agente LangChain ReAct
├── config.py                # Configurações via variáveis de ambiente
├── main.py                  # CLI interativo
├── tools.py                 # Ferramentas LangChain para o agente
├── requirements.txt
└── README.md
```

---

## Testes

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## Exemplos de perguntas

- "Quais módulos do Oracle Fusion ERP estão implementados na Verisure?"
- "Explique o processo de fechamento contábil mensal."
- "Quais são as etapas para processar uma fatura de fornecedor?"
- "Como funciona o Order-to-Cash para venda de sistemas de alarme?"
- "Quais papéis estão envolvidos na folha de pagamento?"
- "Como é feita a conciliação bancária?"
- "Qual o fluxo de cobrança para clientes inadimplentes?"