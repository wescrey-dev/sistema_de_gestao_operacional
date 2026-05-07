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

def seed_portaria_principal():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria Principal",
        codigo="CL-PP-038",
        descricao="Checklist diário de manutenção da Portaria Principal.",
        area_padrao="MP - PORTARIA PRINCIPAL",
    )
    principais = [
        (1, "QDFL-46-2-001 Integridade"),
        (2, "QDFL-46-2-001 Tensão"),
        (3, "QDFL-46-2-001 Corrente"),
        (4, "QDL-61-1-001 Integridade"),
        (5, "QDL-61-1-001 Tensão"),
        (6, "QDL-61-1-001 Corrente"),
        (7, "QGBT-61-1-100 Integridade"),
        (8, "QGBT-61-1-100 Tensão"),
        (9, "QGBT-61-1-100 Corrente"),
        (10, "QDF-61-1-002 Integridade"),
        (11, "QDF-61-1-002 Tensão"),
        (12, "QDF-61-1-002 Corrente"),
        (13, "Circuito de Iluminação Interna"),
        (14, "Circuito de Iluminação Externa"),
        (15, "Circuito de Iluminação Emergência"),
        (16, "Tomadas"),
        (17, "Interruptores"),
        (18, "SPDA Integridade"),
        (19, "Aterramento"),
        (20, "Extintores Carregados"),
        (21, "Climatização Funcionamento"),
        (22, "Circuito de iluminação plataforma embarque de ônibus"),
    ]
    add_section(modelo, "Portaria Principal", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_01():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 1",
        codigo="CL-P1-039",
        descricao="Checklist diário de manutenção da Portaria 1.",
        area_padrao="MP - PORTARIA 01",
    )
    principais = [
        (1, "QS-P1 Integridade"),
        (2, "QS-P1 Tensão"),
        (3, "QS-P1 Corrente"),
        (4, "QDL-52.1-001 Integridade"),
        (5, "QDL-52.1-001 Tensão"),
        (6, "QDL-52.1-001 Corrente"),
        (7, "QGBT-52.1-100 Integridade"),
        (8, "QGBT-52.1-100 Tensão"),
        (9, "QGBT-52.1-100 Corrente"),
        (10, "QDF-52.1-002 Integridade"),
        (11, "QDF-52.1-002 Tensão"),
        (12, "QDF-52.1-002 Corrente"),
        (13, "Circuito de Iluminação Interna"),
        (14, "Circuito de Iluminação Externa"),
        (15, "Circuito Iluminação Emergência"),
        (16, "Tomadas Integridades"),
        (17, "Interruptores Integridades"),
        (18, "SPDA Integridade"),
        (19, "Aterramento Integridade"),
        (20, "Climatização Funcionamento"),
    ]
    add_section(modelo, "Portaria 1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_02():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 2",
        codigo="CL-P2-040",
        descricao="Checklist diário de manutenção da Portaria 2.",
        area_padrao="MP - PORTARIA 2",
    )
    principais = [
        (1, "QDLF-46.5-001 Integridade"),
        (2, "QDLF-46.5-001 Tensão"),
        (3, "QDLF-46.5-001 Corrente"),
        (4, "QDL-61.2-001 Integridade"),
        (5, "QDL-61.2-001 Tensão"),
        (6, "QDL-61.2-001 Corrente"),
        (7, "QGBT-61.2-100 Integridade"),
        (8, "QGBT-61.2-100 Tensão"),
        (9, "QGBT-61.2-100 Corrente"),
        (10, "QDF-61.2-002 Integridade"),
        (11, "QDF-61.2-002 Tensão"),
        (12, "QDF-61.2-002 Corrente"),
        (13, "QDLF-46.1-001 Integridade"),
        (14, "QDLF-46.1-001 Tensão"),
        (15, "QDLF-46.1-001 Corrente"),
        (16, "Circuito de Iluminação Interna"),
        (17, "Circuito de Iluminação Externa"),
        (18, "Circuito Iluminação Emergência"),
        (19, "Tomadas"),
        (20, "SPDA Integridade"),
        (21, "Aterramento"),
        (22, "Extintores Carregados"),
        (23, "Climatização Funcionamento"),
    ]
    add_section(modelo, "Portaria 2", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_04():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 4",
        codigo="CL-P4-041",
        descricao="Checklist diário de manutenção da Portaria 4.",
        area_padrao="SP - PORTARIA 4",
    )
    principais = [
        (1, "GPG - 4 Integridade"),
        (2, "GPG - 4 Tensão"),
        (3, "GPG - 4 Corrente"),
        (4, "GPR - 5 Integridade"),
        (5, "GPR - 5 Tensão"),
        (6, "GPR - 5 Corrente"),
        (7, "Circuito Iluminação Interna"),
        (8, "Circuito Iluminação Plataforma-Ônibus"),
        (9, "Circuito Iluminação Refletores Estac."),
        (10, "Tomadas"),
        (11, "Interruptores"),
        (12, "Extintores carregados"),
        (13, "SPDA Integridade"),
        (14, "Aterramento"),
        (15, "Climatização"),
        (16, "Circuito Iluminação externa portaria"),
    ]
    add_section(modelo, "Portaria 4", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_05():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 5",
        codigo="CL-P5-042",
        descricao="Checklist diário de manutenção da Portaria 5.",
        area_padrao="SP - PORTARIA 5",
    )
    principais = [
        (1, "PN-GPG-5 380V Integridade"),
        (2, "PN-GPG-5 Tensão"),
        (3, "PN-GPG-5 Corrente"),
        (4, "Circuito de Iluminação Interna"),
        (5, "Circuito de Iluminação Externa"),
        (6, "Circuito de Tomadas"),
        (7, "Interruptores"),
        (8, "Extintores carregados"),
        (9, "SPDA Integridade"),
        (10, "Aterramento"),
    ]
    add_section(modelo, "Portaria 5", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_06():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 6",
        codigo="CL-P6-043",
        descricao="Checklist diário de manutenção da Portaria 6.",
        area_padrao="SP - PORTARIA 6",
    )
    principais = [
        (1, "QGBT-61.3-100 380V Integridade"),
        (2, "QGBT-61.3-100 380V Tensão"),
        (3, "QGBT-61.3-100 380V Corrente"),
        (4, "QDL-55-001 Integridade"),
        (5, "QDL-55-001 Tensão"),
        (6, "QDL-55-001 Corrente"),
        (7, "QDF-61.3-002 Integridade"),
        (8, "QDF-61.3-002 Tensão"),
        (9, "QDF-61.3-002 Corrente"),
        (10, "QDLF-46.3-001 Integridade"),
        (11, "QDLF-46.3-001 Tensão"),
        (12, "QDLF-46.3-001 Corrente"),
        (13, "Circuito de Iluminação Interna"),
        (14, "Circuito de Iluminação Externa"),
        (15, "Circuito Iluminação Emergência"),
        (16, "Tomadas"),
        (17, "Interruptores"),
        (18, "SPDA Integridade"),
        (19, "Aterramento"),
        (20, "Extintores Carregados"),
        (21, "Climatização Funcionamento"),
        (22, "Iluminação plataforma de embarque"),
    ]
    add_section(modelo, "Portaria 6", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_07_complemento():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 7 e Complemento Pensilina",
        codigo="CL-P7-044",
        descricao="Checklist diário de manutenção da Portaria 7 com complemento da Portaria Pensilina.",
        area_padrao="MP - PORTARIA 7",
    )
    principais = [
        (1, "QGBT-52.2-100 Integridade"),
        (2, "QGBT-52.2-100 Tensão"),
        (3, "QGBT-52.2-100 Corrente"),
        (4, "QDF-52.2-002 Integridade"),
        (5, "QDF-52.2-002 Tensão"),
        (6, "QDL-52.2-001 Integridade"),
        (7, "QDL-52.2-001 Tensão"),
        (8, "Circuito de Iluminação Interna"),
        (9, "Circuito de Iluminação Externa"),
        (10, "Circuito Iluminação Emergência"),
        (11, "Tomadas"),
        (12, "Interruptores"),
        (13, "SPDA Integridade"),
        (14, "Aterramento"),
        (15, "Extintores carregados"),
    ]
    pensilina = [
        (24, "QDLF-85-001 Integridade"),
        (25, "QDLF-85-001 Tensão"),
        (26, "Iluminação Funcionamento"),
        (27, "Iluminação Emerg. Funcionamento"),
        (28, "Circuito de Tomadas"),
        (29, "Climatização da sala elétrica Funcionamento"),
        (30, "Aterramento"),
        (31, "Iluminação Externa"),
    ]
    add_section(modelo, "Portaria 7", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Complemento da Portaria Pensilina", 2, pensilina, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 3, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_portaria_principal()
        seed_portaria_01()
        seed_portaria_02()
        seed_portaria_04()
        seed_portaria_05()
        seed_portaria_06()
        seed_portaria_07_complemento()
        db.session.commit()
        print("\nSétimo lote cadastrado com sucesso.")
