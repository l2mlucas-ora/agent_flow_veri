"""
Knowledge base for Oracle Fusion Cloud ERP process flows – Verisure.

Each process is stored as a dictionary with:
  - id: unique identifier
  - module: Oracle Cloud module (e.g. "Accounts Payable")
  - name: process name
  - description: brief description
  - steps: ordered list of steps
  - roles: Oracle roles / job functions involved
  - notes: Verisure-specific observations
"""

PROCESS_FLOWS: list[dict] = [
    # ──────────────────────────────────────────────────────────────
    # FINANCIALS – ACCOUNTS PAYABLE
    # ──────────────────────────────────────────────────────────────
    {
        "id": "AP-001",
        "module": "Accounts Payable",
        "name": "Processamento de Faturas de Fornecedores",
        "description": (
            "Fluxo completo de recepção, validação e pagamento de faturas "
            "de fornecedores no Oracle Fusion Cloud Accounts Payable."
        ),
        "steps": [
            "1. Recepção da fatura (e-mail, portal de fornecedores ou importação EDI)",
            "2. Criação/importação da fatura no Oracle Fusion AP",
            "3. Validação automática dos dados da fatura (CNPJ, valor, prazo)",
            "4. Associação com Ordem de Compra (PO Matching – 2 ou 3 vias)",
            "5. Aprovação da fatura pelo gestor responsável (workflow de aprovação)",
            "6. Contabilização automática no Razão Geral (GL)",
            "7. Seleção do pagamento na proposta de pagamento (Payment Batch)",
            "8. Aprovação do lote de pagamento pelo Tesoureiro",
            "9. Geração do arquivo de pagamento (CNAB 240 / SEPA / TED)",
            "10. Envio ao banco e confirmação de liquidação",
            "11. Baixa automática na conta a pagar e conciliação bancária",
        ],
        "roles": [
            "AP Invoice Processor",
            "AP Invoice Approver",
            "AP Payment Manager",
            "GL Accountant",
        ],
        "notes": (
            "Na Verisure, o prazo padrão de pagamento para fornecedores de equipamentos "
            "de alarme é de 30 dias. Fornecedores de serviços de campo têm prazo de 15 dias. "
            "A tolerância de matching de PO é de 5%."
        ),
    },
    {
        "id": "AP-002",
        "module": "Accounts Payable",
        "name": "Gestão de Adiantamentos a Fornecedores",
        "description": (
            "Fluxo para criação, aplicação e liquidação de adiantamentos (prepayments) "
            "a fornecedores no Oracle Fusion AP."
        ),
        "steps": [
            "1. Solicitação de adiantamento pelo comprador",
            "2. Aprovação do adiantamento pelo gestor financeiro",
            "3. Criação da fatura de adiantamento (tipo Prepayment) no Oracle AP",
            "4. Pagamento do adiantamento ao fornecedor",
            "5. Recepção da fatura definitiva do fornecedor",
            "6. Aplicação do adiantamento na fatura definitiva",
            "7. Pagamento do saldo remanescente",
            "8. Baixa do adiantamento e contabilização",
        ],
        "roles": [
            "AP Invoice Processor",
            "AP Payment Manager",
            "Finance Manager",
        ],
        "notes": (
            "Adiantamentos na Verisure requerem aprovação adicional do Diretor Financeiro "
            "para valores acima de R$ 50.000."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # FINANCIALS – ACCOUNTS RECEIVABLE
    # ──────────────────────────────────────────────────────────────
    {
        "id": "AR-001",
        "module": "Accounts Receivable",
        "name": "Faturamento de Clientes – Mensalidade de Monitoramento",
        "description": (
            "Geração e envio de faturas recorrentes referentes à mensalidade de "
            "monitoramento eletrônico para clientes Verisure."
        ),
        "steps": [
            "1. Geração automática das faturas recorrentes (Auto Invoice) via integração com sistema de contratos",
            "2. Validação dos dados do cliente e valores contratados",
            "3. Aprovação e liberação das faturas no Oracle AR",
            "4. Envio das faturas por e-mail / portal do cliente / boleto bancário",
            "5. Monitoramento de vencimentos e envio de lembretes automáticos",
            "6. Recebimento do pagamento (boleto, débito automático, cartão)",
            "7. Aplicação do recebimento na fatura correspondente",
            "8. Reconciliação bancária e contabilização no GL",
        ],
        "roles": [
            "AR Billing Specialist",
            "AR Collections Agent",
            "AR Cash Application Specialist",
            "GL Accountant",
        ],
        "notes": (
            "A Verisure fatura mensalmente cerca de 1 milhão de contratos ativos. "
            "O processo de Auto Invoice é executado no dia 1º de cada mês. "
            "Inadimplência acima de 60 dias aciona o fluxo de cancelamento de contrato."
        ),
    },
    {
        "id": "AR-002",
        "module": "Accounts Receivable",
        "name": "Gestão de Cobranças e Inadimplência",
        "description": (
            "Fluxo de acompanhamento de contas a receber vencidas, envio de cobranças "
            "e acionamento de fluxo de cancelamento para clientes inadimplentes."
        ),
        "steps": [
            "1. Identificação de faturas vencidas através do aging report no Oracle AR",
            "2. Envio de 1º aviso de cobrança (D+5 após vencimento)",
            "3. Envio de 2º aviso de cobrança com taxa de mora (D+15)",
            "4. Contato ativo pela equipe de cobrança (D+30)",
            "5. Envio para cobrança externa / protesto (D+60)",
            "6. Acionamento do fluxo de suspensão do serviço de monitoramento",
            "7. Acionamento do fluxo de cancelamento de contrato (D+90)",
            "8. Baixa de devedores duvidosos (Provisão para Créditos de Liquidação Duvidosa)",
        ],
        "roles": [
            "AR Collections Agent",
            "Collections Manager",
            "Credit Analyst",
        ],
        "notes": (
            "O processo de cobrança da Verisure é integrado ao CRM e ao sistema de monitoramento. "
            "A suspensão do serviço é automática após 60 dias de inadimplência."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # FINANCIALS – GENERAL LEDGER
    # ──────────────────────────────────────────────────────────────
    {
        "id": "GL-001",
        "module": "General Ledger",
        "name": "Fechamento Contábil Mensal",
        "description": (
            "Processo de fechamento do período contábil mensal no Oracle Fusion GL, "
            "incluindo reconciliações, provisões e geração de demonstrativos."
        ),
        "steps": [
            "1. Verificação do status de todos os subledgers (AP, AR, FA, CM)",
            "2. Lançamento de provisões manuais (férias, 13º, imposto de renda)",
            "3. Processamento de depreciação de ativos fixos no Oracle FA",
            "4. Transferência dos subledgers para o GL (Transfer to GL)",
            "5. Reconciliação de contas intercompany",
            "6. Revisão e aprovação dos lançamentos pelo Controller",
            "7. Execução do processo de tradução de moeda (se aplicável)",
            "8. Geração dos relatórios financeiros (Balanço, DRE, DFC)",
            "9. Fechamento do período no Oracle GL (Close Period)",
            "10. Aprovação do fechamento pelo CFO",
        ],
        "roles": [
            "GL Accountant",
            "Senior Accountant",
            "Controller",
            "CFO",
        ],
        "notes": (
            "O fechamento mensal da Verisure ocorre no 3º dia útil do mês subsequente. "
            "A Verisure opera com múltiplas unidades de negócio no Oracle (Brasil, Portugal, Espanha)."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # PROCUREMENT
    # ──────────────────────────────────────────────────────────────
    {
        "id": "PO-001",
        "module": "Procurement",
        "name": "Procure-to-Pay (P2P) – Aquisição de Equipamentos de Alarme",
        "description": (
            "Fluxo completo de compras de equipamentos de segurança eletrônica "
            "(sensores, câmeras, painéis de alarme) desde a requisição até o pagamento."
        ),
        "steps": [
            "1. Criação da Requisição de Compra (Purchase Requisition) pelo solicitante",
            "2. Aprovação da Requisição conforme política de alçadas",
            "3. Conversão da Requisição em Ordem de Compra (Purchase Order)",
            "4. Aprovação da PO conforme política de compras (até R$10k: comprador; acima: gerente)",
            "5. Envio da PO ao fornecedor",
            "6. Acompanhamento do status de entrega",
            "7. Recepção dos equipamentos no almoxarifado (Receiving)",
            "8. Inspeção de qualidade e registro no Oracle Inventory",
            "9. Criação da fatura de fornecedor e PO Matching",
            "10. Aprovação e pagamento da fatura (fluxo AP-001)",
        ],
        "roles": [
            "Requester",
            "Purchasing Agent",
            "Purchasing Manager",
            "Warehouse Receiver",
            "AP Invoice Processor",
        ],
        "notes": (
            "A Verisure utiliza contratos globais com principais fornecedores de equipamentos "
            "(Hikvision, Bosch, Ajax Systems). O prazo médio de entrega é de 45 dias para importados."
        ),
    },
    {
        "id": "PO-002",
        "module": "Procurement",
        "name": "Gestão de Contratos com Fornecedores de Serviços de Campo",
        "description": (
            "Fluxo de criação e gestão de contratos de prestação de serviço com "
            "técnicos e empresas parceiras para instalação e manutenção de alarmes."
        ),
        "steps": [
            "1. Criação do contrato de serviço no Oracle Procurement Contracts",
            "2. Negociação de cláusulas e SLA com o fornecedor",
            "3. Aprovação jurídica e financeira do contrato",
            "4. Assinatura digital do contrato",
            "5. Ativação do contrato e configuração de ordens de serviço recorrentes",
            "6. Acompanhamento de SLA e indicadores de performance do fornecedor",
            "7. Medição e aprovação dos serviços prestados mensalmente",
            "8. Pagamento das faturas de serviço vinculadas ao contrato",
            "9. Renovação ou encerramento do contrato no vencimento",
        ],
        "roles": [
            "Contract Manager",
            "Procurement Manager",
            "Legal Counsel",
            "Finance Manager",
        ],
        "notes": (
            "Os técnicos de campo da Verisure são em parte próprios e em parte terceirizados. "
            "Os contratos de terceirização são revisados anualmente com reajuste pelo IPCA."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # ORDER MANAGEMENT – ORDER TO CASH
    # ──────────────────────────────────────────────────────────────
    {
        "id": "OM-001",
        "module": "Order Management",
        "name": "Order-to-Cash (O2C) – Venda e Instalação de Sistema de Alarme",
        "description": (
            "Fluxo completo desde a contratação do cliente até a ativação do "
            "sistema de alarme e início da cobrança da mensalidade."
        ),
        "steps": [
            "1. Proposta comercial gerada pelo vendedor no CRM",
            "2. Assinatura do contrato de monitoramento pelo cliente",
            "3. Criação do pedido de venda (Sales Order) no Oracle Order Management",
            "4. Análise de crédito do cliente",
            "5. Reserva dos equipamentos no estoque (Inventory Reservation)",
            "6. Agendamento da instalação com técnico de campo",
            "7. Separação e expedição dos equipamentos (Pick, Pack, Ship)",
            "8. Instalação no endereço do cliente pelo técnico",
            "9. Ativação do monitoramento no centro de controle",
            "10. Geração da NF-e de venda dos equipamentos (se aplicável)",
            "11. Ativação do contrato recorrente no AR (início da cobrança)",
        ],
        "roles": [
            "Sales Representative",
            "Order Entry Specialist",
            "Credit Analyst",
            "Warehouse Operator",
            "Field Technician",
            "AR Billing Specialist",
        ],
        "notes": (
            "A Verisure oferece kits de alarme em venda direta ou em comodato incluído "
            "na mensalidade. O prazo máximo para instalação é de 5 dias úteis após a assinatura."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # INVENTORY MANAGEMENT
    # ──────────────────────────────────────────────────────────────
    {
        "id": "INV-001",
        "module": "Inventory Management",
        "name": "Gestão de Estoque de Equipamentos de Segurança",
        "description": (
            "Controle de entrada, saída, transferência e inventário dos equipamentos "
            "eletrônicos nos armazéns e centros de distribuição da Verisure."
        ),
        "steps": [
            "1. Recepção de equipamentos importados/nacionais (PO Receipt)",
            "2. Inspeção de qualidade e aprovação para estoque",
            "3. Armazenagem nos lockers/prateleiras do armazém",
            "4. Reserva de itens para pedidos de venda ou ordens de serviço",
            "5. Separação (Pick) e expedição (Ship) para instaladores ou clientes",
            "6. Transferência entre armazéns (HQ → filiais regionais)",
            "7. Gestão de devoluções de clientes (RMA)",
            "8. Contagem cíclica de inventário (Cycle Count)",
            "9. Inventário anual e ajustes de estoque",
            "10. Reposição automática via min/max planning",
        ],
        "roles": [
            "Inventory Manager",
            "Warehouse Operator",
            "Inventory Analyst",
            "Logistics Coordinator",
        ],
        "notes": (
            "A Verisure opera com armazém central em Barueri/SP e 12 centros regionais. "
            "Os equipamentos são rastreados por número de série no Oracle Inventory. "
            "O ponto de reposição (reorder point) é definido por categoria de equipamento."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # FIXED ASSETS
    # ──────────────────────────────────────────────────────────────
    {
        "id": "FA-001",
        "module": "Fixed Assets",
        "name": "Ciclo de Vida de Ativos Fixos – Equipamentos em Comodato",
        "description": (
            "Gerenciamento do ciclo de vida dos equipamentos de alarme instalados "
            "em comodato nas residências e empresas clientes da Verisure."
        ),
        "steps": [
            "1. Adição do ativo no Oracle Fixed Assets (após instalação no cliente)",
            "2. Classificação do ativo (tipo, vida útil, método de depreciação)",
            "3. Cálculo e lançamento mensal de depreciação",
            "4. Transferência do ativo quando o equipamento é relocado",
            "5. Manutenção/substituição: capitalização de benfeitorias ou baixa parcial",
            "6. Baixa do ativo quando o contrato é cancelado e equipamento retirado",
            "7. Reconciliação do FA com o GL mensalmente",
        ],
        "roles": [
            "Asset Manager",
            "GL Accountant",
            "Controller",
        ],
        "notes": (
            "A Verisure possui mais de 500.000 ativos em comodato no Oracle FA. "
            "A vida útil padrão dos equipamentos eletrônicos é de 5 anos. "
            "O método de depreciação utilizado é Linha Reta (Straight-Line)."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # CASH MANAGEMENT
    # ──────────────────────────────────────────────────────────────
    {
        "id": "CM-001",
        "module": "Cash Management",
        "name": "Conciliação Bancária e Gestão de Caixa",
        "description": (
            "Processo de importação de extratos bancários, conciliação automática "
            "e gestão de posição de caixa no Oracle Fusion Cash Management."
        ),
        "steps": [
            "1. Importação automática do extrato bancário (arquivo OFX/CNAB 240)",
            "2. Matching automático de transações (pagamentos AP e recebimentos AR)",
            "3. Revisão das transações não conciliadas automaticamente",
            "4. Reconciliação manual de itens pendentes",
            "5. Aprovação da conciliação pelo Gestor de Tesouraria",
            "6. Transferência dos lançamentos para o GL",
            "7. Análise da posição de caixa e projeção de fluxo de caixa",
        ],
        "roles": [
            "Treasury Analyst",
            "Cash Manager",
            "GL Accountant",
        ],
        "notes": (
            "A Verisure opera com contas correntes em Itaú, Bradesco e Santander. "
            "A conciliação bancária é executada diariamente. "
            "O fluxo de caixa projetado é gerado semanalmente para o Diretor Financeiro."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # HUMAN CAPITAL MANAGEMENT
    # ──────────────────────────────────────────────────────────────
    {
        "id": "HCM-001",
        "module": "Human Capital Management",
        "name": "Onboarding de Novos Colaboradores",
        "description": (
            "Fluxo de admissão e integração de novos funcionários no Oracle Fusion HCM, "
            "incluindo técnicos de campo, vendedores e equipe administrativa."
        ),
        "steps": [
            "1. Aprovação da requisição de pessoal pelo gestor",
            "2. Processo seletivo e oferta de emprego no Oracle Recruiting",
            "3. Criação do cadastro do colaborador no Oracle HCM",
            "4. Configuração de benefícios (vale-transporte, vale-refeição, plano de saúde)",
            "5. Provisionamento de acesso aos sistemas (Oracle, e-mail, CRM)",
            "6. Treinamento inicial e certificação técnica (para técnicos de campo)",
            "7. Integração com a folha de pagamento (Oracle Payroll ou ADP)",
            "8. Configuração de metas e avaliação de desempenho",
        ],
        "roles": [
            "HR Specialist",
            "Recruiter",
            "Hiring Manager",
            "IT Administrator",
            "Payroll Specialist",
        ],
        "notes": (
            "A Verisure contrata em média 200 novos técnicos de campo por mês no Brasil. "
            "A certificação técnica é obrigatória antes de iniciar atendimentos aos clientes."
        ),
    },
    {
        "id": "HCM-002",
        "module": "Human Capital Management",
        "name": "Folha de Pagamento Mensal",
        "description": (
            "Processamento da folha de pagamento mensal dos colaboradores da Verisure "
            "no Oracle Fusion Payroll, incluindo comissões de vendedores e horas extras."
        ),
        "steps": [
            "1. Fechamento do ponto eletrônico e validação de horas extras",
            "2. Lançamento de eventos variáveis (comissões, bônus, descontos)",
            "3. Cálculo da folha de pagamento no Oracle Payroll",
            "4. Revisão e aprovação dos resultados pelo RH",
            "5. Aprovação final pelo Diretor de RH",
            "6. Geração do arquivo de pagamento bancário (CNAB 240)",
            "7. Pagamento dos salários até o 5º dia útil do mês",
            "8. Geração do holerite eletrônico no portal do colaborador",
            "9. Recolhimento de encargos (FGTS, INSS, IR)",
            "10. Contabilização da folha no GL",
        ],
        "roles": [
            "Payroll Specialist",
            "HR Manager",
            "Finance Director",
            "GL Accountant",
        ],
        "notes": (
            "A Verisure possui aproximadamente 8.000 colaboradores no Brasil. "
            "Os comissionistas (vendedores) têm folha variável calculada no dia 20 do mês. "
            "O sistema de ponto é integrado ao Oracle HCM via API."
        ),
    },
    # ──────────────────────────────────────────────────────────────
    # PROJECT MANAGEMENT
    # ──────────────────────────────────────────────────────────────
    {
        "id": "PPM-001",
        "module": "Project Portfolio Management",
        "name": "Gestão de Projetos de Expansão – Novas Filiais",
        "description": (
            "Fluxo de criação e controle de projetos de abertura de novas filiais "
            "e centros de monitoramento no Oracle Fusion Project Management."
        ),
        "steps": [
            "1. Criação do projeto no Oracle PPM com escopo, prazo e orçamento",
            "2. Aprovação do business case pelo Comitê de Expansão",
            "3. Detalhamento do plano de trabalho (WBS) e alocação de recursos",
            "4. Contratação de fornecedores (reforma, TI, infraestrutura)",
            "5. Controle de avanço físico e financeiro do projeto",
            "6. Lançamento de custos do projeto (mão de obra, materiais, serviços)",
            "7. Capitalização de ativos ao fim do projeto (integração FA)",
            "8. Encerramento do projeto e lições aprendidas",
        ],
        "roles": [
            "Project Manager",
            "Project Controller",
            "Finance Manager",
            "Expansion Director",
        ],
        "notes": (
            "A Verisure tem plano de abrir 5 novas filiais por ano no Brasil. "
            "O orçamento médio de abertura de filial é de R$ 2 milhões. "
            "Os projetos são monitorados em dashboards no Oracle Analytics Cloud."
        ),
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# Module descriptions (used for module-level queries)
# ──────────────────────────────────────────────────────────────────────────────

MODULE_DESCRIPTIONS: dict[str, str] = {
    "Accounts Payable": (
        "Módulo responsável pelo controle de contas a pagar, processamento e pagamento "
        "de faturas de fornecedores, gestão de adiantamentos e conciliação com o GL."
    ),
    "Accounts Receivable": (
        "Módulo responsável pelo faturamento de clientes, controle de recebíveis, "
        "gestão de cobranças, aplicação de recebimentos e reconciliação com o GL."
    ),
    "General Ledger": (
        "Módulo central de contabilidade que consolida as transações de todos os "
        "subledgers, suporta fechamento contábil e geração de demonstrativos financeiros."
    ),
    "Procurement": (
        "Módulo de compras que abrange desde a requisição até o pagamento (Procure-to-Pay), "
        "incluindo gestão de fornecedores, cotações, POs e contratos."
    ),
    "Order Management": (
        "Módulo de gestão de pedidos de venda que suporta o ciclo Order-to-Cash, "
        "desde a criação do pedido até o faturamento e recebimento."
    ),
    "Inventory Management": (
        "Módulo de controle de estoque que gerencia recepção, armazenagem, expedição, "
        "transferências e inventários de equipamentos eletrônicos."
    ),
    "Fixed Assets": (
        "Módulo de controle de ativos imobilizados, incluindo adição, depreciação, "
        "transferências, manutenções e baixas de equipamentos em comodato."
    ),
    "Cash Management": (
        "Módulo de tesouraria responsável pela conciliação bancária automática, "
        "gestão de posição de caixa e projeção de fluxo de caixa."
    ),
    "Human Capital Management": (
        "Suite completa de RH que abrange recrutamento, admissão, folha de pagamento, "
        "benefícios e gestão de desempenho dos colaboradores Verisure."
    ),
    "Project Portfolio Management": (
        "Módulo de gestão de projetos para controle de escopo, prazo, custo e recursos "
        "em projetos estratégicos como expansão de filiais e centros de monitoramento."
    ),
}
