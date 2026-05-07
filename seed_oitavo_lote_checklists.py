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

def seed_ps3():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria Externa PS3",
        codigo="CL-PS3-046",
        descricao="Checklist diário de manutenção da Portaria Externa PS3.",
        area_padrao="MP / SP - PORTARIA EXTERNA PS3",
    )
    principais = [
        (1, "QGBT-61.5-100 380V Integridade"),
        (2, "QGBT-61.5-100 380V Tensão"),
        (3, "QGBT-61.5-100 380V Corrente"),
        (4, "QDF-61.5-002 380V Integridade"),
        (5, "QDF-61.5-002 380V Tensão"),
        (6, "QDF-61.5-002 380V Corrente"),
        (7, "QDL-61.5-001 380V Integridade"),
        (8, "QDL-61.5-001 380V Tensão"),
        (9, "QDL-61.5-001 380V Corrente"),
        (10, "Circuito de Tomadas"),
        (11, "Circuito de Iluminação Interna"),
        (12, "Circuito de Iluminação Externa"),
        (13, "SPDA Integridade"),
        (14, "Aterramento"),
        (15, "Climatização da sala elétrica"),
    ]
    add_section(modelo, "PS3", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_ps1():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria Externa PS1",
        codigo="CL-PS1-045",
        descricao="Checklist diário de manutenção da Portaria Externa PS1.",
        area_padrao="MP / SP - PORTARIA EXTERNA PS1",
    )
    principais = [
        (1, "QGBT-61.4-001 380V Integridade"),
        (2, "QGBT-61.4-001 380V Tensão"),
        (3, "QGBT-61.4-001 380V Corrente"),
        (4, "QDF-61.4-002 380V Integridade"),
        (5, "QDF-61.4-002 380V Tensão"),
        (6, "QDF-61.4-002 380V Corrente"),
        (7, "QDL-61.4-001 380V Integridade"),
        (8, "QDL-61.4-001 380V Tensão"),
        (9, "QDL-61.4-001 380V Corrente"),
        (10, "Circuito de Iluminação Interna"),
        (11, "Circuito de Iluminação Externa"),
        (12, "Climatização da sala elétrica"),
        (13, "Extintores Carregados"),
    ]
    add_section(modelo, "PS1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_2_cdc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 2 CDC",
        codigo="CL-P2CDC-050",
        descricao="Checklist diário de manutenção da Portaria 2 - CDC.",
        area_padrao="MP - PORTARIA 2 CDC",
    )
    principais = [
        (1, "GPG-2 Integridade"),
        (2, "GPG-2 Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Climatização Funcionamento"),
        (7, "Aterramento Integridade"),
        (8, "Circuito de Tomadas Tensão / Integridade"),
        (9, "Interruptores Integridade"),
    ]
    add_section(modelo, "Portaria 2 - CDC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_1_cdc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria 1 CDC",
        codigo="CL-P1CDC-049",
        descricao="Checklist diário de manutenção da Portaria 1 - CDC.",
        area_padrao="MP - PORTARIA 1 CDC",
    )
    principais = [
        (1, "GPG-1 Integridade"),
        (2, "GPG-1 Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Climatização Funcionamento"),
        (7, "Aterramento Integridade"),
        (8, "Circuito de Tomadas Tensão / Integridade"),
        (9, "Interruptores Integridade"),
    ]
    add_section(modelo, "Portaria 1 - CDC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_pr7():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria PR7",
        codigo="CL-PR7-048",
        descricao="Checklist diário de manutenção da Portaria PR7.",
        area_padrao="EXTERNA - PORTARIA PR7",
    )
    principais = [
        (1, "QGBT-51.1-001 Integridade"),
        (2, "QGBT-51.1-001 Tensão"),
        (3, "QGBT-51.1-001 Corrente"),
        (4, "Circuito Iluminação Interna"),
        (5, "Circuito Iluminação Externa"),
        (6, "Circuito de Tomadas Tensão / Integridade"),
        (7, "Interruptores Integridade"),
        (8, "Aterramento Integridade"),
    ]
    add_section(modelo, "PR7", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_pr1():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Portaria PR1",
        codigo="CL-PR1-047",
        descricao="Checklist diário de manutenção da Portaria PR1.",
        area_padrao="EXTERNA - PORTARIA PR1",
    )
    principais = [
        (1, "QDLF-51.2-001 Integridade"),
        (2, "QDLF-51.2-001 Tensão"),
        (3, "QDLF-51.2-001 Corrente"),
        (4, "Circuito Iluminação Interna"),
        (5, "Circuito Iluminação Externa"),
        (6, "Circuito de Tomadas Tensão / Integridade"),
        (7, "Interruptores Integridade"),
        (8, "Aterramento Integridade"),
    ]
    add_section(modelo, "PR1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_ps3()
        seed_ps1()
        seed_portaria_2_cdc()
        seed_portaria_1_cdc()
        seed_pr7()
        seed_pr1()
        db.session.commit()
        print("\nOitavo lote cadastrado com sucesso.")
