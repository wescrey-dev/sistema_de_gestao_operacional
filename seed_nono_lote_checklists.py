from app import (
    app,
    db,
    ChecklistModelo,
    ChecklistCampoCabecalho,
    ChecklistSecao,
    ChecklistItemModelo,
)

COMMON_HEADER = [
    ("area_local", "Área / Local", "texto", True),
    ("semana_numero", "Semana Nº", "texto", False),
    ("data_execucao", "Data", "data", True),
    ("om", "OM", "texto", False),
    ("responsavel_1", "Responsável 1", "texto", False),
    ("responsavel_2", "Responsável 2", "texto", False),
    ("inicio", "Início", "hora", False),
    ("termino", "Término", "hora", False),
    ("tempo_base", "Tempo Base (min)", "texto", False),
]

def get_or_create_model(nome, codigo, descricao, area_padrao):
    modelo = ChecklistModelo.query.filter_by(codigo=codigo).first()
    if modelo:
        print(f"[OK] Modelo já existe: {codigo} - {nome}")
        return modelo

    modelo = ChecklistModelo(
        nome=nome,
        codigo=codigo,
        descricao=descricao,
        area_padrao=area_padrao,
        ativo=True,
    )
    db.session.add(modelo)
    db.session.flush()

    for ordem, (nome_campo, label_campo, tipo_campo, obrigatorio) in enumerate(COMMON_HEADER, start=1):
        db.session.add(
            ChecklistCampoCabecalho(
                checklist_modelo_id=modelo.id,
                nome_campo=nome_campo,
                label_campo=label_campo,
                tipo_campo=tipo_campo,
                obrigatorio=obrigatorio,
                ordem=ordem,
            )
        )
    return modelo

def add_item(secao, numero_item, descricao, ordem, usa_rst=True, usa_obs=True):
    db.session.add(
        ChecklistItemModelo(
            checklist_secao_id=secao.id,
            numero_item=str(numero_item) if numero_item is not None else "",
            descricao=descricao,
            tipo_resposta="padrao",
            usa_normal_anormal=True,
            usa_valores_rst=usa_rst,
            usa_observacao=usa_obs,
            usa_resolvido=False,
            ordem=ordem,
        )
    )

def add_section(modelo, titulo, ordem, itens, tipo_secao="itens", usa_rst=True, usa_obs=True):
    secao = ChecklistSecao(
        checklist_modelo_id=modelo.id,
        titulo=titulo,
        tipo_secao=tipo_secao,
        ordem=ordem,
    )
    db.session.add(secao)
    db.session.flush()

    if tipo_secao == "observacoes_gerais":
        for i in range(1, itens + 1):
            db.session.add(
                ChecklistItemModelo(
                    checklist_secao_id=secao.id,
                    numero_item=str(i),
                    descricao=f"Ocorrência {i}",
                    tipo_resposta="observacao_geral",
                    usa_normal_anormal=False,
                    usa_valores_rst=False,
                    usa_observacao=False,
                    usa_resolvido=True,
                    ordem=i,
                )
            )
        return

    for ordem_item, (numero_item, descricao) in enumerate(itens, start=1):
        add_item(secao, numero_item, descricao, ordem_item, usa_rst=usa_rst, usa_obs=usa_obs)

def seed_pensilina():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Pensilina",
        codigo="CL-PEN-052",
        descricao="Checklist diário de manutenção da Pensilina.",
        area_padrao="MP - EXPED. PENSILINA",
    )
    principais = [
        (1, "QDF-55-002 Integridade"),
        (2, "QDF-55-002 Tensão"),
        (3, "QDF-55-002 Corrente"),
        (4, "QDL-55-001 Integridade"),
        (5, "QDL-55-001 Tensão"),
        (6, "QDL-55-001 Corrente"),
        (7, "QGBT-55-100 Integridade"),
        (8, "QGBT-55-100 Tensão"),
        (9, "QGBT-55-100 Corrente"),
        (10, "Circuito de Ilum. Interna Escritório"),
        (11, "Circuito Iluminação Emergência"),
        (12, "Circuito Iluminação Externa"),
        (13, "Circuito de Tomadas Tensão / Integridade"),
        (14, "Chuveiros Integr. Masc. e Femin."),
        (15, "Circuito Iluminação WC masc. e femin."),
        (16, "Climatização Funcionamento"),
    ]
    add_section(modelo, "Pensilina", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_escritorio_central():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Escritório Central",
        codigo="CL-ESC-051",
        descricao="Checklist diário de manutenção do Escritório Central.",
        area_padrao="MP - ESCRITÓRIO CENTRAL",
    )
    principais = [
        (1, "QGBT-E Integridade"),
        (2, "QGBT-E Tensão"),
        (3, "QGBT-E Corrente"),
        (4, "QDLF-01 Integridade"),
        (5, "QDLF-01 Tensão"),
        (6, "QDLF-02 Integridade"),
        (7, "QDLF-02 Tensão"),
        (8, "QDF-SL TI Integridade"),
        (9, "QDF-SL TI Tensão"),
        (10, "Circ. Ilum. Vestiário Masculino"),
        (11, "Circ. Ilum. Vestiário Feminino"),
        (12, "Circ. Iluminação WC-Masculino"),
        (13, "Circ. Iluminação WC-Feminino"),
        (14, "Circuito de Iluminação Interna"),
        (15, "Circuito de Iluminação Externa"),
        (16, "Circuito Iluminação Emergência"),
        (17, "Circuito de Tomadas Tensão / Integridade"),
        (18, "Interruptores Integridade"),
        (19, "Chuveiros Integridade"),
        (20, "SPDA Integridade"),
        (21, "Aterramento Integridade"),
        (22, "Extintores Carregados"),
        (23, "GTA-235 Transf. Ger. Integridade"),
    ]
    add_section(modelo, "Escritório Central", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_balanca_ilha_ecologica():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Balança Ilha Ecológica",
        codigo="CL-BIE-055",
        descricao="Checklist diário de manutenção da Balança Ilha Ecológica.",
        area_padrao="MP - BALANÇA ILHA ECOLÓGICA",
    )
    principais = [
        (1, "QDLF-BC-004 Integridade"),
        (2, "QDLF-BC-004 Tensão"),
        (3, "QDLF-BC-004 Corrente"),
        (4, "QDL-BC-005 Integridade"),
        (5, "QDL-BC-005 Tensão"),
        (6, "QDL-BC-005 Corrente"),
        (7, "Circuito de Iluminação Interna"),
        (8, "Circuito de Iluminação Emerg."),
        (9, "Circuito de Tomadas Tensão / Integridade"),
        (10, "Descidas do subsistema de captação (SPDA)"),
        (11, "Caixas de inspeções do aterramento / SPDA"),
    ]
    add_section(modelo, "Balança Ilha Ecológica", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_balanca_p5():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Balança P5",
        codigo="CL-BP5-054",
        descricao="Checklist diário de manutenção da Balança P5.",
        area_padrao="SP - BALANÇA P5",
    )
    principais = [
        (1, "GPTS Integridade"),
        (2, "GPTS Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Climatização Funcionamento"),
        (7, "Aterramento Integridade"),
        (8, "Circuito de Tomadas Tensão / Integridade"),
    ]
    add_section(modelo, "Subestação 1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_balanca_p1():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Prédio e Balança P1",
        codigo="CL-BP1-053",
        descricao="Checklist diário de manutenção do Prédio e Balança P1.",
        area_padrao="MP - PRÉDIO E BALANÇA P1",
    )
    principais = [
        (1, "QDFL-48-001 Integridade"),
        (2, "QDFL-48-001 Tensão"),
        (3, "QDFL-48-001 Corrente"),
        (4, "QDLF-50-001 Integridade"),
        (5, "QDLF-50-001 Tensão"),
        (6, "QDLF-50-001 Corrente"),
        (7, "QDF-50.2-002 Integridade"),
        (8, "QDF-50.2-002 Tensão"),
        (9, "QDF-50.2-002 Corrente"),
        (10, "QDL-50.2-001 Integridade"),
        (11, "QDL-50.2-001 Tensão"),
        (12, "QDL-50.2-001 Corrente"),
        (13, "Circuito de Iluminação Interna"),
        (14, "Circuito de Iluminação Externa"),
        (15, "Circuito Iluminação Emergência"),
        (16, "Circuitos de Tomadas Tensão / Integridade"),
        (17, "Interruptores Integridade"),
        (18, "SPDA Integridade"),
        (19, "Aterramento Integridade"),
        (20, "Climatização Funcionamento"),
    ]
    add_section(modelo, "Prédio e Balança P1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_pensilina()
        seed_escritorio_central()
        seed_balanca_ilha_ecologica()
        seed_balanca_p5()
        seed_balanca_p1()
        db.session.commit()
        print("\nNono lote cadastrado com sucesso.")
