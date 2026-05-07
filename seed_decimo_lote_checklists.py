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

def seed_convivencia_motoristas_p6():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Convivência Motoristas P6",
        codigo="CL-CMP6-059",
        descricao="Checklist diário de manutenção da convivência de motoristas P6.",
        area_padrao="SP - CONVIVÊNCIA MOTORISTAS P6",
    )
    principais = [
        (1, "QDLF-15.3-001 Integridade"),
        (2, "QDLF-15.3-001 Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Externa"),
        (5, "Circuito Iluminação Emergência"),
        (6, "Interruptores Integridades"),
        (7, "Chuveiros Integridade"),
        (8, "Circuito de Tomadas Tensão / Integridade"),
        (9, "Aterramento Integridade"),
    ]
    add_section(modelo, "Convivência Motoristas P6", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_convivencia_motoristas_p7():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Convivência Motoristas P7",
        codigo="CL-CMP7-060",
        descricao="Checklist diário de manutenção da convivência de motoristas P7.",
        area_padrao="CONVIVÊNCIA MOTORISTAS P7",
    )
    principais = [
        (1, "QDLF-15-1-001 Integridade"),
        (2, "QDLF-15-1-001 Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Circuito de Tomadas Tensão / Integridade"),
        (7, "Aterramento Integridade"),
        (8, "Chuveiros Integridade"),
        (9, "Interruptores Integridade"),
    ]
    add_section(modelo, "Convivência Motoristas P7", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_convivencia_motoristas_cdc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Convivência Motoristas CDC",
        codigo="CL-CMCDC-056",
        descricao="Checklist diário de manutenção da convivência de motoristas CDC.",
        area_padrao="MP - CONVIVÊNCIA MOTORISTAS CDC",
    )
    principais = [
        (1, "Painel-DAP Integridade"),
        (2, "Painel-DAP Tensão"),
        (3, "Circuito Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Climatização Funcionamento"),
        (7, "Circuito de Tomadas Tensão / Integridade"),
        (8, "Interruptores Integridade"),
        (9, "Aterramento / Integridade"),
    ]
    add_section(modelo, "Convivência Motoristas CDC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_convivencia_motoristas_p1():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Convivência Motoristas P1",
        codigo="CL-CMP1-057",
        descricao="Checklist diário de manutenção da convivência de motoristas P1.",
        area_padrao="MP - EXTERNA - CONVIVÊNCIA MOTORISTAS P1",
    )
    principais = [
        (1, "QDLF-15.2-001 Integridade"),
        (2, "QDLF-15.2-001 Tensão"),
        (3, "Circuito de Iluminação Interna"),
        (4, "Circuito Iluminação Emergência"),
        (5, "Circuito Iluminação Externa"),
        (6, "Circuito de Tomadas Tensão / Integridade"),
        (7, "Chuveiros Integridade"),
        (8, "Interruptores Integridade"),
        (9, "Aterramento Integridade"),
    ]
    add_section(modelo, "Convivência Motoristas P1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_convivencia_motoristas_p5():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Convivência Motoristas P5",
        codigo="CL-CMP5-058",
        descricao="Checklist diário de manutenção da convivência de motoristas P5.",
        area_padrao="EXTERNA - CONVIVÊNCIA MOTORISTAS P5",
    )
    principais = [
        (1, "GPCM Integridade"),
        (2, "GPCM Tensão"),
        (3, "GPCM Corrente"),
        (4, "QPMVM Integridade"),
        (5, "QPMVM Tensão"),
        (6, "QPMVM Corrente"),
        (7, "GPMVM-2 Integridade"),
        (8, "GPMVM-2 Tensão"),
        (9, "GPMVM-2 Corrente"),
        (10, "Circuito de Iluminação Interna"),
        (11, "Circuito Iluminação Emergência"),
        (12, "Circuito Iluminação Externa"),
        (13, "Circuito de Tomadas Tensão / Integridade"),
        (14, "Interruptores Integridade"),
        (15, "Chuveiros Integridades"),
        (16, "Aterramento Integridade"),
    ]
    add_section(modelo, "Convivência Motoristas P5", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_convivencia_motoristas_p6()
        seed_convivencia_motoristas_p7()
        seed_convivencia_motoristas_cdc()
        seed_convivencia_motoristas_p1()
        seed_convivencia_motoristas_p5()
        db.session.commit()
        print("\nDécimo lote cadastrado com sucesso.")
