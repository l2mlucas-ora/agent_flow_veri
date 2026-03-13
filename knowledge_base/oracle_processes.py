"""
Oracle Fusion Cloud ERP – Knowledge base of process flows for Verisure.

Each entry in PROCESS_FLOWS is a dictionary with the following structure:

{
    "id": str,                      # unique slug
    "module": str,                  # ERP module (e.g. "Financials", "SCM")
    "sub_module": str,              # sub-area within the module
    "name": str,                    # process / flow name
    "description": str,             # what the process does
    "trigger": str,                 # what starts this process
    "steps": list[str],             # ordered list of steps
    "roles": list[str],             # Oracle roles / job functions involved
    "integration_points": list[str],# other modules or external systems touched
    "key_tables_views": list[str],  # main Oracle DB objects (informational)
    "verisure_notes": str,          # Verisure-specific observations / config
}
"""

from __future__ import annotations

from typing import Any

PROCESS_FLOWS: list[dict[str, Any]] = [
    # ------------------------------------------------------------------ #
    # FINANCIALS – Accounts Payable                                        #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-ap-01",
        "module": "Financials",
        "sub_module": "Accounts Payable",
        "name": "Ciclo Completo de Contas a Pagar (P2P – Pagamento)",
        "description": (
            "Processo de registro, aprovação e pagamento de faturas de fornecedores "
            "desde o recebimento do documento fiscal até a quitação do pagamento e "
            "baixa contábil."
        ),
        "trigger": "Recebimento de fatura/NF do fornecedor (manual ou EDI).",
        "steps": [
            "1. Recebimento da fatura pelo AP Clerk (Portal de Fornecedores ou entrada manual).",
            "2. Validação dos dados obrigatórios: CNPJ, valor, data, número de documento.",
            "3. Match automático com Ordem de Compra (PO Matching 2-way ou 3-way).",
            "4. Resolução de exceções de match (tolerâncias de preço/quantidade).",
            "5. Roteamento para aprovação conforme alçada de aprovação da Verisure.",
            "6. Aprovação pelo gestor responsável (Workflow de Aprovação Oracle).",
            "7. Criação de distribuições contábeis (Accounting Distributions).",
            "8. Validação e aprovação contábil (Accounting Validation).",
            "9. Criação do pagamento (Payment Batch ou pagamento individual).",
            "10. Aprovação do pagamento conforme política financeira.",
            "11. Envio do arquivo de remessa ao banco (CNAB240 / SEPA).",
            "12. Confirmação do pagamento pelo banco (retorno bancário).",
            "13. Baixa da fatura (Invoice Cleared) e reconciliação bancária.",
        ],
        "roles": [
            "AP Clerk",
            "AP Supervisor",
            "Financial Approver",
            "Payment Manager",
            "Cash Manager",
        ],
        "integration_points": [
            "Procurement (Purchase Orders)",
            "Inventory (Receipt confirmations)",
            "General Ledger (Journal Entries)",
            "Cash Management (Bank Reconciliation)",
            "Tax (Tax Calculation – ICMS, IPI, PIS, COFINS)",
        ],
        "key_tables_views": [
            "AP_INVOICES_ALL",
            "AP_INVOICE_LINES_ALL",
            "AP_INVOICE_DISTRIBUTIONS_ALL",
            "AP_CHECKS_ALL",
            "AP_PAYMENT_SCHEDULES_ALL",
        ],
        "verisure_notes": (
            "A Verisure utiliza aprovação em dois níveis para faturas acima de R$ 50.000. "
            "Fornecedores nacionais são integrados via portal Ariba. "
            "Retenção de IR/CSRF calculada automaticamente pelo módulo de Tax."
        ),
    },
    # ------------------------------------------------------------------ #
    # FINANCIALS – Accounts Receivable                                     #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-ar-01",
        "module": "Financials",
        "sub_module": "Accounts Receivable",
        "name": "Ciclo de Contas a Receber – Faturamento e Cobrança",
        "description": (
            "Processo de geração de faturas para clientes, cobrança e baixa de "
            "recebimentos, incluindo gestão de inadimplência."
        ),
        "trigger": "Ordem de serviço concluída ou contrato de assinatura ativo.",
        "steps": [
            "1. Geração automática da fatura a partir do contrato (Subscription Billing).",
            "2. Revisão e aprovação da fatura pelo AR Supervisor.",
            "3. Emissão da Nota Fiscal Eletrônica (NF-e) via integração SEFAZ.",
            "4. Envio da fatura ao cliente (e-mail, portal ou EDI).",
            "5. Aplicação de recebimentos (Cash Application) – boleto, PIX ou cartão.",
            "6. Reconciliação dos recebimentos com extratos bancários.",
            "7. Follow-up de cobranças para faturas vencidas (Dunning Letters).",
            "8. Escalada para processo de cobrança jurídica se necessário.",
            "9. Baixa de perdas (Write-off) com aprovação do CFO.",
            "10. Relatório de aging e DSO para a diretoria financeira.",
        ],
        "roles": [
            "AR Clerk",
            "AR Supervisor",
            "Collections Agent",
            "Credit Manager",
            "CFO",
        ],
        "integration_points": [
            "Order Management (Sales Orders)",
            "Subscription Management (Contracts)",
            "General Ledger",
            "Cash Management",
            "Tax (NF-e / SEFAZ)",
        ],
        "key_tables_views": [
            "AR_PAYMENT_SCHEDULES_ALL",
            "AR_RECEIVABLE_APPLICATIONS_ALL",
            "AR_CASH_RECEIPTS_ALL",
            "RA_CUSTOMER_TRX_ALL",
            "RA_CUST_TRX_LINE_GL_DIST_ALL",
        ],
        "verisure_notes": (
            "Mensalidades de clientes residenciais são geradas em lote no dia 1 de cada mês. "
            "Integração com sistema de monitoramento para confirmar serviço ativo antes do faturamento. "
            "PIX configurado como meio preferencial de recebimento."
        ),
    },
    # ------------------------------------------------------------------ #
    # FINANCIALS – General Ledger                                          #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-gl-01",
        "module": "Financials",
        "sub_module": "General Ledger",
        "name": "Fechamento Contábil Mensal (Period Close)",
        "description": (
            "Processo de encerramento do período contábil mensal, incluindo "
            "conciliações, reclassificações, provisões e geração de relatórios gerenciais."
        ),
        "trigger": "Último dia útil do mês ou conforme calendário contábil aprovado.",
        "steps": [
            "1. Verificação do status de todos os lançamentos pendentes (sub-ledgers abertos).",
            "2. Execução do processo de transferência dos sub-ledgers para o GL (Subledger Accounting – SLA).",
            "3. Conciliação de contas intercompany (Intercompany Reconciliation).",
            "4. Lançamento de provisões manuais (accruals) pelo Controller.",
            "5. Revisão e aprovação de journals manuais.",
            "6. Execução do processo de revalorização de moeda estrangeira (Revaluation).",
            "7. Consolidação de entidades legais (Consolidation).",
            "8. Execução do balanço de verificação (Trial Balance) e revisão de anomalias.",
            "9. Geração de relatórios financeiros: DRE, Balanço, Fluxo de Caixa.",
            "10. Aprovação do fechamento pelo CFO e encerramento do período (Close Period).",
        ],
        "roles": [
            "GL Accountant",
            "Controller",
            "Financial Analyst",
            "CFO",
            "External Auditor (read-only)",
        ],
        "integration_points": [
            "Accounts Payable",
            "Accounts Receivable",
            "Fixed Assets",
            "Procurement",
            "Payroll",
            "Projects",
            "Intercompany",
        ],
        "key_tables_views": [
            "GL_JE_BATCHES",
            "GL_JE_HEADERS",
            "GL_JE_LINES",
            "GL_BALANCES",
            "GL_CODE_COMBINATIONS",
        ],
        "verisure_notes": (
            "A Verisure adota IFRS como padrão contábil. "
            "Entidades legais: Verisure Brasil, Verisure Portugal, consolidação via Hyperion. "
            "Prazo de fechamento: D+3 após o último dia do mês."
        ),
    },
    # ------------------------------------------------------------------ #
    # FINANCIALS – Fixed Assets                                            #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-fa-01",
        "module": "Financials",
        "sub_module": "Fixed Assets",
        "name": "Gestão de Ativos Fixos – Adição, Depreciação e Baixa",
        "description": (
            "Controle do ciclo de vida dos ativos fixos da Verisure, desde a capitalização "
            "até a depreciação periódica e eventual baixa ou venda."
        ),
        "trigger": "Recebimento e ativação de um ativo (equipamento de alarme, veículo, imóvel, TI).",
        "steps": [
            "1. Identificação do ativo para capitalização a partir da fatura de compra ou WIP.",
            "2. Criação do ativo no Oracle FA (Asset Addition) com categoria, localização e responsável.",
            "3. Definição do método e taxa de depreciação conforme política contábil.",
            "4. Execução mensal da depreciação (Run Depreciation).",
            "5. Transferência de ativos entre localidades ou centros de custo.",
            "6. Inventário físico anual (Physical Inventory Reconciliation).",
            "7. Reavaliação de ativos (se aplicável por IFRS).",
            "8. Processo de baixa: venda, sucateamento ou perda (Asset Retirement).",
            "9. Transferência automática dos lançamentos para o GL.",
        ],
        "roles": [
            "Asset Accountant",
            "Controller",
            "Operations Manager (validação física)",
        ],
        "integration_points": [
            "Accounts Payable (invoice source)",
            "Projects (CIP / Work-in-Progress)",
            "General Ledger",
            "Procurement",
        ],
        "key_tables_views": [
            "FA_ADDITIONS",
            "FA_ASSET_HISTORY",
            "FA_DEPRN_SUMMARY",
            "FA_BOOKS",
            "FA_RETIREMENTS",
        ],
        "verisure_notes": (
            "Equipamentos de alarme instalados em clientes são classificados como ativos "
            "operacionais (IFRS 16 / IAS 16). "
            "Taxa de depreciação dos alarmes: 5 anos (20% a.a. – método linear). "
            "Inventário físico realizado em setembro de cada ano."
        ),
    },
    # ------------------------------------------------------------------ #
    # PROCUREMENT – Purchase-to-Pay                                        #
    # ------------------------------------------------------------------ #
    {
        "id": "scm-po-01",
        "module": "Procurement",
        "sub_module": "Purchasing",
        "name": "Processo de Compras – Requisição até Ordem de Compra (P2P)",
        "description": (
            "Fluxo completo de aquisição de bens e serviços, desde a requisição interna "
            "até a emissão, aprovação e envio da Ordem de Compra ao fornecedor."
        ),
        "trigger": "Criação de Requisição de Compra (Purchase Requisition) por colaborador autorizado.",
        "steps": [
            "1. Colaborador cria Purchase Requisition no Oracle Self-Service Procurement.",
            "2. Validação automática: saldo orçamentário, categoria de compra, política de gastos.",
            "3. Roteamento para aprovação conforme hierarquia de aprovação (até 3 níveis).",
            "4. Aprovação da requisição pelo gestor de área.",
            "5. Comprador recebe a requisição aprovada e inicia o processo de cotação (RFQ) se necessário.",
            "6. Seleção do fornecedor e negociação de preço/prazo.",
            "7. Criação da Purchase Order (PO) pelo comprador.",
            "8. Aprovação da PO conforme alçada (FMoA – Financial Matrix of Authority).",
            "9. Envio automático da PO ao fornecedor via portal ou e-mail.",
            "10. Confirmação de recebimento da PO pelo fornecedor.",
            "11. Recebimento físico dos bens/serviços (Receipt) pelo almoxarife ou gestor.",
            "12. Três vias de conferência (3-way match): PO × Recebimento × Fatura.",
        ],
        "roles": [
            "Requester",
            "Department Manager",
            "Buyer",
            "Procurement Manager",
            "Warehouse / Receiving Clerk",
        ],
        "integration_points": [
            "Accounts Payable (invoice matching)",
            "Inventory Management",
            "Budgetary Control",
            "General Ledger",
            "Supplier Portal (Oracle Supplier Portal)",
        ],
        "key_tables_views": [
            "PO_HEADERS_ALL",
            "PO_LINES_ALL",
            "PO_DISTRIBUTIONS_ALL",
            "PO_REQUISITION_HEADERS_ALL",
            "RCV_SHIPMENT_HEADERS",
        ],
        "verisure_notes": (
            "Compras de equipamentos de segurança acima de R$ 100.000 exigem cotação com "
            "mínimo de 3 fornecedores (política de sourcing da Verisure). "
            "Fornecedores críticos de alarmes são pré-aprovados pelo Procurement Manager. "
            "Integração com sistema de gestão de estoque de kits de alarme."
        ),
    },
    # ------------------------------------------------------------------ #
    # SUPPLY CHAIN – Inventory Management                                  #
    # ------------------------------------------------------------------ #
    {
        "id": "scm-inv-01",
        "module": "Supply Chain",
        "sub_module": "Inventory Management",
        "name": "Gestão de Estoque – Recebimento, Movimentação e Inventário",
        "description": (
            "Controle do estoque de equipamentos de segurança (alarmes, sensores, câmeras) "
            "e insumos de instalação, incluindo recebimento, movimentação interna e inventário."
        ),
        "trigger": "Recebimento de mercadoria de fornecedor ou transferência entre depósitos.",
        "steps": [
            "1. Recebimento físico dos equipamentos no depósito (Receiving Transaction).",
            "2. Inspeção de qualidade e confirmação das quantidades.",
            "3. Atualização do saldo de estoque no Oracle Inventory.",
            "4. Alocação de equipamentos para ordens de serviço de instalação.",
            "5. Baixa de estoque na expedição para técnicos instaladores.",
            "6. Devolução de equipamentos com defeito ao fornecedor (RMA).",
            "7. Contagem cíclica mensal de itens críticos (Cycle Counting).",
            "8. Inventário geral anual e reconciliação de divergências.",
            "9. Reposição automática via min/max ou MRP quando estoque mínimo atingido.",
        ],
        "roles": [
            "Warehouse Manager",
            "Receiving Clerk",
            "Quality Inspector",
            "Field Technician",
            "Inventory Analyst",
        ],
        "integration_points": [
            "Procurement (Purchase Orders / Receipts)",
            "Accounts Payable",
            "Fixed Assets (equipamentos capitalizáveis)",
            "Field Service (alocação para ordens de serviço)",
            "General Ledger (custo dos estoques)",
        ],
        "key_tables_views": [
            "MTL_SYSTEM_ITEMS_B",
            "MTL_MATERIAL_TRANSACTIONS",
            "MTL_ONHAND_QUANTITIES_DETAIL",
            "MTL_CYCLE_COUNT_HEADERS",
            "MTL_PHYSICAL_INVENTORIES",
        ],
        "verisure_notes": (
            "Estoque centralizado no CD de Alphaville (SP) com depósitos regionais em "
            "Rio de Janeiro, Belo Horizonte, Curitiba e Porto Alegre. "
            "Itens de alto giro: central de alarme, sensores de movimento, baterias 12V. "
            "Custo médio ponderado utilizado como método de avaliação de estoque."
        ),
    },
    # ------------------------------------------------------------------ #
    # PROJECTS – Project Costing                                           #
    # ------------------------------------------------------------------ #
    {
        "id": "ppm-pc-01",
        "module": "Project Portfolio Management",
        "sub_module": "Project Costing",
        "name": "Gestão de Custos de Projetos – Instalação de Sistemas de Segurança",
        "description": (
            "Controle de custos de projetos de instalação e manutenção de sistemas de "
            "segurança nos clientes, rastreando mão-de-obra, materiais e despesas diretas."
        ),
        "trigger": "Criação de projeto de instalação a partir de contrato de cliente aprovado.",
        "steps": [
            "1. Criação do projeto no Oracle Projects com template padrão de instalação.",
            "2. Definição da estrutura analítica do projeto (WBS – Work Breakdown Structure).",
            "3. Definição do orçamento do projeto (Project Budget).",
            "4. Alocação de recursos (técnicos, veículos, equipamentos).",
            "5. Registro de horas trabalhadas pelos técnicos (Timecards).",
            "6. Importação de custos de materiais do Inventory e AP.",
            "7. Capitalização de custos em Ativos Fixos (CIP → FA) quando aplicável.",
            "8. Monitoramento de variação orçamentária (Budget vs. Actual).",
            "9. Faturamento do projeto ao cliente (Project Billing) conforme marco contratual.",
            "10. Encerramento do projeto e transferência de custos residuais.",
        ],
        "roles": [
            "Project Manager",
            "Project Accountant",
            "Field Technician",
            "Resource Manager",
            "Billing Specialist",
        ],
        "integration_points": [
            "Procurement (material costs)",
            "Inventory (material issues)",
            "Payroll (labor costs)",
            "Fixed Assets (capitalization)",
            "Accounts Receivable (project billing)",
            "General Ledger",
        ],
        "key_tables_views": [
            "PA_PROJECTS_ALL",
            "PA_TASKS",
            "PA_EXPENDITURE_ITEMS_ALL",
            "PA_BUDGETS",
            "PA_DRAFT_INVOICES_ALL",
        ],
        "verisure_notes": (
            "Projetos de instalação residencial têm duração média de 1 dia. "
            "Projetos corporativos (grandes contas) podem durar de 30 a 180 dias. "
            "Capitalização de equipamentos instalados no cliente somente quando contrato "
            "prevê devolução ao final (modelo de leasing de equipamentos)."
        ),
    },
    # ------------------------------------------------------------------ #
    # HUMAN RESOURCES – Core HR                                            #
    # ------------------------------------------------------------------ #
    {
        "id": "hcm-hr-01",
        "module": "Human Capital Management",
        "sub_module": "Core HR",
        "name": "Processo de Admissão de Colaboradores (Hire-to-Retire)",
        "description": (
            "Fluxo de onboarding de novos colaboradores desde a requisição de vaga "
            "até a ativação no sistema de folha de pagamento."
        ),
        "trigger": "Aprovação de requisição de pessoal pelo gestor de área e RH.",
        "steps": [
            "1. Criação da Requisição de Pessoal (Job Requisition) pelo gestor.",
            "2. Aprovação da vaga pelo HRBP e Diretor da área.",
            "3. Processo seletivo (Recruiting – Oracle Talent Acquisition).",
            "4. Oferta de emprego e aceite pelo candidato.",
            "5. Pré-admissão: envio de documentação via portal do candidato.",
            "6. Criação do registro do colaborador no Oracle HCM (Person Record).",
            "7. Definição de cargo, departamento, gestor, localização e data de início.",
            "8. Configuração de benefícios (plano de saúde, VT, VR).",
            "9. Integração com folha de pagamento (Payroll Interface).",
            "10. Criação de acesso ao Oracle e demais sistemas (provisioning).",
            "11. Orientação e integração (onboarding checklist).",
        ],
        "roles": [
            "Hiring Manager",
            "HR Business Partner",
            "Recruiter",
            "HR Admin",
            "Payroll Specialist",
            "IT Security (provisioning)",
        ],
        "integration_points": [
            "Talent Acquisition (Recruiting)",
            "Payroll",
            "Benefits Administration",
            "Time and Labor",
            "Learning Management",
            "Identity Management (SSO / AD)",
        ],
        "key_tables_views": [
            "PER_ALL_PEOPLE_F",
            "PER_ALL_ASSIGNMENTS_F",
            "PER_POSITIONS",
            "PER_JOBS",
            "PAY_PAYROLL_ASSIGNMENTS",
        ],
        "verisure_notes": (
            "A Verisure opera com dois tipos principais de contrato: CLT e PJ (prestadores). "
            "Técnicos de campo são admitidos em maior volume em outubro/novembro (alta temporada). "
            "Integração com sistema de controle de acesso físico ativada automaticamente na admissão."
        ),
    },
    # ------------------------------------------------------------------ #
    # HUMAN CAPITAL MANAGEMENT – Payroll                                   #
    # ------------------------------------------------------------------ #
    {
        "id": "hcm-py-01",
        "module": "Human Capital Management",
        "sub_module": "Payroll",
        "name": "Processamento de Folha de Pagamento Mensal",
        "description": (
            "Cálculo, aprovação e pagamento da folha de pagamento mensal dos colaboradores CLT, "
            "incluindo salários, benefícios, descontos, impostos e encargos trabalhistas."
        ),
        "trigger": "Abertura do período de folha no calendário de payroll (geralmente dia 20 do mês).",
        "steps": [
            "1. Bloqueio do período de folha e encerramento de lançamentos de RH.",
            "2. Importação de marcações de ponto e horas extras (Time and Labor).",
            "3. Processamento da folha: cálculo de salários, adicionais e descontos.",
            "4. Cálculo de impostos: IRRF, INSS, FGTS.",
            "5. Cálculo de benefícios: VT, VR, Plano de Saúde, Seguro de Vida.",
            "6. Geração de relatório de pré-folha para revisão do Payroll Specialist.",
            "7. Correções e reprocessamento se necessário.",
            "8. Aprovação da folha pelo Gerente de RH e Controller.",
            "9. Geração de arquivo de pagamento (CNAB240) para o banco.",
            "10. Envio do arquivo ao banco e confirmação de pagamento.",
            "11. Emissão de contracheques (holerites) no portal do colaborador.",
            "12. Geração de obrigações acessórias: eSocial, SEFIP, DIRF.",
            "13. Transferência de custos de folha para GL e Projects.",
        ],
        "roles": [
            "Payroll Specialist",
            "Payroll Manager",
            "HR Manager",
            "Controller",
            "Tax Specialist",
        ],
        "integration_points": [
            "Core HR (employee master data)",
            "Time and Labor",
            "Benefits",
            "General Ledger (cost distribution)",
            "Projects (labor costs)",
            "Tax (eSocial, SEFIP, DIRF)",
            "Banking (CNAB240)",
        ],
        "key_tables_views": [
            "PAY_PAYROLL_ACTIONS",
            "PAY_ASSIGNMENT_ACTIONS",
            "PAY_RUN_RESULTS",
            "PAY_RUN_RESULT_VALUES",
            "PAY_ELEMENT_ENTRIES_F",
        ],
        "verisure_notes": (
            "Folha processada até o dia 28 de cada mês. "
            "Banco principal: Bradesco (pagamento de salários e FGTS). "
            "eSocial S-1200 gerado automaticamente após aprovação da folha. "
            "Técnicos de campo possuem adicional de insalubridade de 20%."
        ),
    },
    # ------------------------------------------------------------------ #
    # BUDGETARY CONTROL                                                    #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-bc-01",
        "module": "Financials",
        "sub_module": "Budgetary Control",
        "name": "Controle Orçamentário – Budget Check e Gestão de Variâncias",
        "description": (
            "Processo de controle orçamentário que verifica a disponibilidade de saldo "
            "orçamentário antes de aprovar requisições, ordens de compra e despesas."
        ),
        "trigger": "Submissão de transação financeira (requisição, PO, journal) que consome orçamento.",
        "steps": [
            "1. Submissão da transação (Requisição, PO, despesa) pelo solicitante.",
            "2. Reserva orçamentária automática (Funds Reservation) pelo Oracle.",
            "3. Verificação de disponibilidade de saldo (Funds Check): Aprovado / Alerta / Falha.",
            "4. Se falha: notificação ao solicitante e gestor com saldo disponível.",
            "5. Solicitante pode solicitar suplementação orçamentária (Budget Transfer).",
            "6. Aprovação de suplementação pelo Controller e CFO.",
            "7. Execução da transferência orçamentária e liberação da transação.",
            "8. Relatório mensal de execução orçamentária (Budget vs. Actual).",
            "9. Revisão orçamentária trimestral (Forecast Update).",
        ],
        "roles": [
            "Requester",
            "Budget Manager",
            "Controller",
            "CFO",
            "Financial Analyst",
        ],
        "integration_points": [
            "Procurement",
            "Accounts Payable",
            "General Ledger",
            "Projects",
            "Expenses",
        ],
        "key_tables_views": [
            "FUN_BUDGET_VERSIONS",
            "GL_BC_PACKETS",
            "GL_BUDORG_BC_OPTIONS",
            "GL_BUDGET_ASSIGNMENTS",
            "GL_BUDGET_VERSIONS",
        ],
        "verisure_notes": (
            "Controle orçamentário configurado em modo 'Advisory' para centros de custo "
            "operacionais e 'Absolute' para despesas de capital (CAPEX). "
            "Revisão orçamentária nos meses de março, junho e setembro."
        ),
    },
    # ------------------------------------------------------------------ #
    # EXPENSES – Travel & Expense                                          #
    # ------------------------------------------------------------------ #
    {
        "id": "fi-ex-01",
        "module": "Financials",
        "sub_module": "Expenses",
        "name": "Gestão de Despesas de Viagem e Reembolso",
        "description": (
            "Processo de submissão, aprovação e reembolso de despesas de viagem e "
            "despesas corporativas dos colaboradores da Verisure."
        ),
        "trigger": "Retorno de viagem corporativa ou incorrência de despesa autorizada.",
        "steps": [
            "1. Colaborador registra despesas no aplicativo Oracle Expenses (mobile ou web).",
            "2. Upload de comprovantes fiscais (notas fiscais, recibos).",
            "3. Categorização automática por tipo de despesa (viagem, alimentação, hospedagem).",
            "4. Verificação de conformidade com política de viagens da Verisure.",
            "5. Submissão do relatório de despesas para aprovação.",
            "6. Aprovação pelo gestor direto.",
            "7. Auditoria pelo time de AP (verificação de comprovantes e limites).",
            "8. Aprovação final e criação de pagamento ao colaborador.",
            "9. Lançamento contábil no GL e distribuição por centro de custo/projeto.",
        ],
        "roles": [
            "Employee",
            "Manager",
            "AP Auditor",
            "AP Manager",
        ],
        "integration_points": [
            "Accounts Payable",
            "General Ledger",
            "Budgetary Control",
            "Projects (project expenses)",
            "Credit Card (corporate card reconciliation)",
        ],
        "key_tables_views": [
            "AP_EXPENSE_REPORT_HEADERS_ALL",
            "AP_EXPENSE_REPORT_LINES_ALL",
            "AP_CREDIT_CARD_TRXNS_ALL",
        ],
        "verisure_notes": (
            "Política de viagens: voos classe econômica para voos nacionais, "
            "business class permitida para voos internacionais acima de 6 horas. "
            "Limite diário de diárias: R$ 400 (cidades tipo A) e R$ 300 (demais). "
            "Cartão corporativo disponível para gestores e acima."
        ),
    },
]


def get_all_modules() -> list[str]:
    """Return a deduplicated sorted list of ERP modules in the knowledge base."""
    return sorted({flow["module"] for flow in PROCESS_FLOWS})


def get_all_sub_modules() -> list[str]:
    """Return a deduplicated sorted list of sub-modules in the knowledge base."""
    return sorted({flow["sub_module"] for flow in PROCESS_FLOWS})


def get_process_by_id(process_id: str) -> dict[str, Any] | None:
    """Return a single process flow by its unique ID, or None if not found."""
    for flow in PROCESS_FLOWS:
        if flow["id"] == process_id:
            return flow
    return None


def get_processes_by_module(module: str) -> list[dict[str, Any]]:
    """Return all process flows that belong to the given ERP module (case-insensitive)."""
    module_lower = module.lower()
    return [f for f in PROCESS_FLOWS if f["module"].lower() == module_lower]


def search_processes(query: str) -> list[dict[str, Any]]:
    """
    Simple keyword search across process name, description, steps,
    module and sub_module fields.
    Returns flows sorted by relevance (number of keyword hits).
    """
    keywords = [kw.strip().lower() for kw in query.split() if kw.strip()]
    if not keywords:
        return PROCESS_FLOWS

    scored: list[tuple[int, dict[str, Any]]] = []
    for flow in PROCESS_FLOWS:
        searchable = " ".join(
            [
                flow["name"],
                flow["description"],
                flow["module"],
                flow["sub_module"],
                flow.get("verisure_notes", ""),
                " ".join(flow["steps"]),
                " ".join(flow["roles"]),
                " ".join(flow["integration_points"]),
            ]
        ).lower()
        score = sum(searchable.count(kw) for kw in keywords)
        if score > 0:
            scored.append((score, flow))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [flow for _, flow in scored]
