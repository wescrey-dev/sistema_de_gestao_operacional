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

def seed_bloco_b_paineis():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Bloco B Painéis",
        codigo="CL-BBP-029",
        descricao="Checklist de manutenção dos painéis do Prédio Bloco B.",
        area_padrao="MP - Bloco B",
    )
    principais = [
        (1, "QDLF-BB-008 Sala elétrica cozinha - Integridade"),
        (2, "QDLF-BB-008 Sala elétrica cozinha - Tensão"),
        (3, "QE-BB-07 Tagueamento dos disjuntores - Integridade"),
        (4, "QE-BB-07 Tagueamento dos disjuntores - Tensão"),
        (5, "QE-BB-06 - Integridade"),
        (6, "QE-BB-06 - Tensão"),
        (7, "QE-BB-04 Tagueamento dos disjuntores - Integridade"),
        (8, "QE-BB-04 Tagueamento dos disjuntores - Tensão"),
        (9, "ADMINISTRAÇÃO - Tensão"),
        (10, "QE-BB-02 - Integridade"),
        (11, "QE-BB-02 Tagueamento dos disjuntores - Integridade"),
        (12, "QE-BB-02 Tagueamento dos disjuntores - Tensão"),
        (13, "QDF-BB-10 - Integridade"),
        (14, "QDF-BB-10 - Tensão"),
        (15, "QDLF-BB-005 - Integridade"),
        (16, "QDLF-BB-005 - Tensão"),
        (17, "QDF-BB-11 - Integridade"),
        (18, "QDF-BB-11 - Tensão"),
        (19, "QDLF-BB-007 - Integridade"),
        (20, "QDLF-BB-007 - Tensão"),
        (21, "QDF-BB-009 - Integridade"),
        (22, "QDF-BB-009 - Tensão"),
        (23, "QDF-BB-006 Tagueamento dos disjuntores"),
        (24, "QDF-BB-006 - Tensão"),
        (25, "Vestiário Feminino - Tensão"),
        (26, "QDF-BB-004 - Integridade"),
        (27, "QDF-BB-004 Tagueamento dos disjuntores"),
        (28, "QDF-BB-004 - Tensão"),
        (29, "QDF-BB-003 - Integridade"),
        (30, "QDF-BB-003 Tagueamento dos disjuntores"),
        (31, "QDF-BB-003 - Tensão"),
        (32, "Portaria PS1 - Tensão"),
        (33, "QDLF-BB-002 - Integridade"),
        (34, "QDLF-BB-002 Tagueamento dos disjuntores"),
        (35, "QDLF-BB-002 - Tensão"),
        (36, "QGBT-61.4-001 Circuito 03F - Tensão"),
        (37, "QE-BB-001 - Integridade"),
        (38, "QE-BB-001 Tagueamento dos disjuntores"),
        (39, "QE-BB-001 - Tensão"),
        (40, "Portaria PS3 - Tensão"),
        (41, "QGBT-61.5-100 Circuito 04F - Tensão"),
        (42, "Panificadora - Tensão"),
        (43, "QE-BB-05 - Integridade"),
        (44, "QE-BB-05 Tagueamento dos disjuntores"),
        (45, "QE-BB-05 - Tensão"),
        (46, "QGBT-BA-101 - Integridade"),
        (47, "QGBT-BA-101 - Tensão"),
        (48, "Corredor vestiário - Tensão"),
        (49, "QDLF-BB-002 Tagueamento dos disjuntores"),
        (50, "QDLF-BB-002 - Tensão"),
        (51, "Iluminação externa"),
        (52, "Iluminação interna"),
        (53, "Iluminação de emergência"),
        (54, "Tomadas"),
        (55, "Extintores"),
        (56, "Caixa de tomadas"),
        (57, "Luminárias"),
        (58, "Lâmpadas"),
        (59, "Interruptores"),
        (60, "Caixa de interruptores"),
        (61, "Módulo das tomadas"),
        (62, "Módulo dos interruptores"),
        (63, "Tampa das tomadas"),
        (64, "Tampa dos interruptores"),
        (65, "Luminárias - Iluminação externa"),
        (66, "Lâmpadas - Iluminação externa"),
        (67, "Timer"),
        (68, "Carga"),
        (69, "Sinalização"),
        (70, "Validade"),
    ]
    add_section(modelo, "Prédio Bloco B", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_bloco_a_paineis():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Bloco A Painéis",
        codigo="CL-BAP-028",
        descricao="Checklist de manutenção de painéis, iluminação, tomadas e extintores do Prédio Bloco A.",
        area_padrao="MP - Bloco A",
    )
    principais = [
        (1, "Corredor Banco Santander"),
        (2, "Sala das cestas básicas"),
        (3, "QDLF-BA-014 - Integridade"),
        (4, "QDLF-BA-014 Tagueamento dos disjuntores"),
        (5, "QDLF-BA-014 - Tensão"),
        (6, "Sala Correios"),
        (7, "Oficina Expansão"),
        (8, "QDLF-BA-012 - Integridade"),
        (9, "QDLF-BA-012 Tagueamento dos disjuntores"),
        (10, "QDLF-BA-012 - Tensão"),
        (11, "QDLF-BA-004 Oficina Expansão - Integridade"),
        (12, "QDLF-BA-004 Oficina Expansão - Tensão"),
        (13, "Banco Santander"),
        (14, "QDLF-BA-019 Oficina Expansão - Integridade"),
        (15, "QDLF-BA-019 Oficina Expansão - Tensão"),
        (16, "QDLF-BA-018 Oficina Expansão - Integridade"),
        (17, "QDLF-BA-018 Oficina Expansão - Tensão"),
        (18, "QDLF-BA-027 Oficina Expansão - Integridade"),
        (19, "QDLF-BA-027 Oficina Expansão - Tensão"),
        (20, "QE-BA-01 Banco Santander - Integridade"),
        (21, "QE-BA-01 Banco Santander - Tensão"),
        (22, "Sala de Arquivo"),
        (23, "QE-BA-03 - Integridade"),
        (24, "QE-BA-03 Tagueamento dos disjuntores"),
        (25, "QE-BA-03 - Tensão"),
        (26, "QE-BA-02 Oficina Expansão"),
        (27, "QDF-BA-023 - Integridade"),
        (28, "QDF-BA-023 Tagueamento dos disjuntores"),
        (29, "QDF-BA-023 - Tensão"),
        (30, "Iluminação externa"),
        (31, "Iluminação interna"),
        (32, "Tomadas"),
        (33, "Iluminação de emergência"),
        (34, "Extintores"),
        (35, "Oficina expansão - Luminárias"),
        (36, "Oficina expansão - Lâmpadas"),
        (37, "Oficina expansão - Interruptores"),
        (38, "Oficina expansão - Caixa de interruptores"),
        (39, "Oficina expansão - Módulo dos interruptores"),
        (40, "Oficina expansão - Tampa dos interruptores"),
        (41, "Sala Raio X - Luminárias"),
        (42, "Sala Raio X - Lâmpadas"),
        (43, "Sala Raio X - Interruptores"),
        (44, "Sala Raio X - Caixa de interruptores"),
        (45, "Sala Raio X - Módulo dos interruptores"),
        (46, "Sala Raio X - Tampa dos interruptores"),
        (47, "Sala de arquivo - Luminárias"),
        (48, "Sala de arquivo - Lâmpadas"),
        (49, "Sala de arquivo - Interruptores"),
        (50, "Sala de arquivo - Caixa de interruptores"),
        (51, "Sala de arquivo - Módulo dos interruptores"),
        (52, "Sala de arquivo - Tampa dos interruptores"),
        (53, "Tomadas / módulos / tampas"),
        (54, "Carga"),
        (55, "Sinalização"),
        (56, "Validade"),
    ]
    add_section(modelo, "Prédio Bloco A", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_bloco_d_paineis():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Bloco D Painéis Elétricos",
        codigo="CL-BDP-030",
        descricao="Checklist de manutenção dos painéis elétricos do Prédio Bloco D.",
        area_padrao="MP - Bloco D - Painéis elétricos",
    )
    principais = [
        (1, "QE-BD-02 Rampa Alim. Tensão"),
        (2, "QE-BD-03 Câmara Fria Tensão"),
        (3, "QGBT-BD-101 Refeitório Tensão"),
        (4, "QGBT-BD-100 Vestiário Tensão"),
        (5, "QE-37.1-01 Corredor Vestiário Tensão"),
        (6, "QGBT-37.1-100 Vestiário Tensão"),
        (7, "QDF-BD-003 Ar e Condensad. Tensão"),
        (8, "QDLF-BD-005 Ilumin. Externa Tensão"),
        (9, "QDF-BD-006 Distr. Tomadas Tensão"),
        (10, "QDF-BD-007 Esteira Lava-louças Tensão"),
        (11, "QDL-37.1-001 Ilum. Ext. Vest. Tensão"),
        (12, "QDF-37.1-002 Vest. Femin. Chuv. Tensão"),
        (13, "QDF-37.1-003 Vest. Femin. Chuv. Tensão"),
        (14, "QDF-37.1-004 Vest. Tomadas Tensão"),
        (15, "QDF-BD-002 Exaustores Tensão"),
        (16, "QDF-BD-011 Comp. Evaporadores Tensão"),
        (17, "Circuito de Iluminação Interna"),
        (18, "Circuito de Iluminação Externa"),
        (19, "Circuito de Iluminação Emergência"),
        (20, "Circuito de Tomadas"),
        (21, "Extintores carregados"),
    ]
    add_section(modelo, "Prédio Bloco D", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 6, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_bloco_b_paineis()
        seed_bloco_a_paineis()
        seed_bloco_d_paineis()
        db.session.commit()
        print("\nSexto lote cadastrado com sucesso.")
