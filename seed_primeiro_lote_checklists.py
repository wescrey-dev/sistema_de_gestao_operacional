from app import (
    app,
    db,
    ChecklistModelo,
    ChecklistCampoCabecalho,
    ChecklistSecao,
    ChecklistItemModelo,
)

COMMON_HEADER = [
    ("area_local", "Área / Local", "text", True),
    ("semana_numero", "Semana Nº", "text", False),
    ("data_execucao", "Data", "date", True),
    ("om", "OM", "text", False),
    ("responsavel_1", "Responsável 1", "text", False),
    ("responsavel_2", "Responsável 2", "text", False),
    ("inicio", "Início", "time", False),
    ("termino", "Término", "time", False),
    ("tempo_base", "Tempo Base (min)", "text", False),
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

def seed_se_02_pintura():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Pintura 2 / Pintura 2",
        codigo="CL-EC-002",
        descricao="Checklist diário de manutenção da SE 02 - Pintura",
        area_padrao="MP - SE 02 - PINTURA",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "TR-3 Integridade"),
        (9, "TR-3 Temperaturas"),
        (10, "Banco de Capacitor Nº 1 Integridade"),
        (11, "Banco de Capacitor Nº 1 Tensão"),
        (12, "Banco de Capacitor Nº 1 Corrente"),
        (13, "Banco de Capacitor Nº 1 Contatores"),
        (14, "Banco de Capacitor Nº 1 Cabos"),
        (15, "Banco de Capacitor Nº 2 Integridade"),
        (16, "Banco de Capacitor Nº 2 Tensão"),
        (17, "Banco de Capacitor Nº 2 Corrente"),
        (18, "Banco de Capacitor Nº 2 Contatores"),
        (19, "Banco de Capacitor Nº 2 Cabos"),
        (20, "Banco de Capacitor Nº 3 Integridade"),
        (21, "Banco de Capacitor Nº 3 Tensão"),
        (22, "Banco de Capacitor Nº 3 Corrente"),
        (23, "Banco de Capacitor Nº 3 Contatores"),
        (24, "Banco de Capacitor Nº 3 Cabos"),
        (25, "Painel-QGBT-1 Integridade"),
        (26, "Painel-QGBT-1 Tensão QG1-TR1"),
        (27, "Painel-QGBT-1 Corrente QG1-TR1"),
        (28, "Painel-QGBT-1 Tensão QG2-TR2"),
        (29, "Painel-QGBT-1 Corrente QG2-TR2"),
        (30, "Painel-QGBT-1 Tensão QG3-TR3"),
        (31, "Painel-QGBT-1 Corrente QG3-TR3"),
        (32, "UPS - Integridade"),
        (33, "UPS - Tensão Bateria"),
        (34, "UPS - Tensão Entrada"),
        (35, "UPS - Tensão Saída"),
        (36, "Baterias - Integridade"),
        (37, "QAUX - Integridade"),
        (38, "QAUX - Tensão"),
        (39, "Leitos / Eletrocalhas Integridade"),
        (40, "Cabos Integridade"),
        (41, "Iluminação da SE Funcionamento"),
        (42, "Iluminação UPS Funcionamento"),
        (43, "Limpeza e organização"),
        (44, "Portas integridade"),
        (45, "Portas controle de acesso"),
        (46, "Aterramento - Integridade"),
        (47, "Tapete de isolamento para manobra 1 peça"),
        (48, "Carrinho 1250A para manobra 1 peça"),
        (49, "Alavanca de Aterramento 1 peça"),
        (50, "Alavanca de Inserção e extração 1 peça"),
        (51, "Manivela de abertura de painel 1 peça"),
        (52, "Extintores carregados"),
        (53, "Telhado integridade / vazamento / goteira"),
        (54, "Tomadas Tensão / Integridade"),
        (55, "SPDA - Integridade"),
        (56, "Diagramas Unifilar"),
        (57, "Climatização - Ventiladores / Exaustores"),
        (58, "TR AUX-1 Integridade"),
        (59, "TR AUX-1 Temperaturas"),
        (60, "TR AUX-2 Integridade"),
        (61, "TR AUX-2 Temperaturas"),
        (62, "Painel QS-SE-PE Integridade"),
        (63, "Painel QS-SE-PE Tensão"),
        (64, "Painel QS-SE-PE Corrente"),
        (65, "Painel QDAT - Integridade"),
        (66, "Painel QBT - Integridade"),
        (67, "Painel QBT - Tensão"),
        (68, "Painel QBT - Corrente"),
    ]

    ups_sec = [
        (1, "Integridade"),
        (2, "Funcionamento"),
    ]

    ups_status = [
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação Energy Center", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, ups_sec, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

def seed_se_montagem():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Montagem",
        codigo="CL-MTG-008",
        descricao="Checklist diário de manutenção da SE - Montagem.",
        area_padrao="MP - SE - MONTAGEM",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "TR-3 Integridade"),
        (9, "TR-3 Temperaturas"),
        (10, "TR-4 Integridade"),
        (11, "TR-4 Temperaturas"),
        (12, "Banco de Capacitor Nº 1 Integridade"),
        (13, "Banco de Capacitor Nº 1 Tensão"),
        (14, "Banco de Capacitor Nº 1 Corrente"),
        (15, "Banco de Capacitor Nº 1 Contatores"),
        (16, "Banco de Capacitor Nº 1 Cabos"),
        (17, "Banco de Capacitor Nº 2 Integridade"),
        (18, "Banco de Capacitor Nº 2 Tensão"),
        (19, "Banco de Capacitor Nº 2 Corrente"),
        (20, "Banco de Capacitor Nº 2 Contatores"),
        (21, "Banco de Capacitor Nº 2 Cabos"),
        (22, "Banco de Capacitor Nº 3 Integridade"),
        (23, "Banco de Capacitor Nº 3 Tensão"),
        (24, "Banco de Capacitor Nº 3 Corrente"),
        (25, "Banco de Capacitor Nº 3 Contatores"),
        (26, "Banco de Capacitor Nº 3 Cabos"),
        (27, "Banco de Capacitor Nº 4 Integridade"),
        (28, "Banco de Capacitor Nº 4 Tensão"),
        (29, "Banco de Capacitor Nº 4 Corrente"),
        (30, "Banco de Capacitor Nº 4 Contatores"),
        (31, "Banco de Capacitor Nº 4 Cabos"),
        (32, "Painel-QGBT-1 Integridade"),
        (33, "Painel-QGBT-1 Tensão QG1-TR4"),
        (34, "Painel-QGBT-1 Corrente QG1-TR4"),
        (35, "Painel-QGBT-1 Tensão QG2-TR2"),
        (36, "Painel-QGBT-1 Corrente QG2-TR2"),
        (37, "Painel-QGBT-2 Integridade"),
        (38, "Painel-QGBT-2 Tensão QG1-TR3"),
        (39, "Painel-QGBT-2 Corrente QG1-TR3"),
        (40, "Painel-QGBT-2 Tensão QG2-TR1"),
        (41, "Painel-QGBT-2 Corrente QG2-TR1"),
        (42, "UPS - Integridade"),
        (43, "UPS - Tensão Bateria"),
        (44, "UPS - Tensão Entrada"),
        (45, "UPS - Tensão Saída"),
        (46, "Baterias - Integridade"),
        (47, "QAUX - Integridade"),
        (48, "QAUX - Tensão"),
        (49, "Leitos / Eletrocalhas Integridade"),
        (50, "Cabos Integridade"),
        (51, "Iluminação da SE Funcionamento"),
        (52, "Iluminação UPS Funcionamento"),
        (53, "Limpeza e organização"),
        (54, "Portas integridade"),
        (55, "Aterramento Integridade"),
        (56, "Diagramas Unifilar"),
        (57, "Tapete de isolamento para manobra 1 peça"),
        (58, "Carrinho 1250A para manobra 1 peça"),
        (59, "Alavanca de Aterramento 1 peça"),
        (60, "Alavanca de Inserção e extração 1 peça"),
        (61, "Manivela de abertura de painel 1 peça"),
        (62, "Extintores carregados"),
        (63, "Telhado integridade / vazamento / goteira"),
        (64, "Tomadas de uso geral - Integridade"),
        (65, "Climatização - Ventil./Exaustores"),
        (66, "PBT-42.2-100 Oficina Mont. Tensão"),
    ]

    sala_ups_ar = [
        (1, "Integridade"),
        (2, "Funcionamento"),
    ]

    sala_ups_status = [
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação Montagem", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

def seed_se_prensas():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Prensas",
        codigo="CL-PRN-005",
        descricao="Checklist diário de manutenção da SE - Prensas.",
        area_padrao="MP - SE - PRENSAS",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "TR-3 Integridade"),
        (9, "TR-3 Temperaturas"),
        (10, "TR-4 Integridade"),
        (11, "TR-4 Temperaturas"),
        (12, "Banco de Capacitor Nº 1 Integridade"),
        (13, "Banco de Capacitor Nº 1 Tensão"),
        (14, "Banco de Capacitor Nº 1 Corrente"),
        (15, "Banco de Capacitor Nº 1 Contatores"),
        (16, "Banco de Capacitor Nº 1 Cabos"),
        (17, "Banco de Capacitor Nº 2 Integridade"),
        (18, "Banco de Capacitor Nº 2 Tensão"),
        (19, "Banco de Capacitor Nº 2 Corrente"),
        (20, "Banco de Capacitor Nº 2 Contatores"),
        (21, "Banco de Capacitor Nº 2 Cabos"),
        (22, "Banco de Capacitor Nº 3 Integridade"),
        (23, "Banco de Capacitor Nº 3 Tensão"),
        (24, "Banco de Capacitor Nº 3 Corrente"),
        (25, "Banco de Capacitor Nº 3 Contatores"),
        (26, "Banco de Capacitor Nº 3 Cabos"),
        (27, "Banco de Capacitor Nº 4 Integridade"),
        (28, "Banco de Capacitor Nº 4 Tensão"),
        (29, "Banco de Capacitor Nº 4 Corrente"),
        (30, "Banco de Capacitor Nº 4 Contatores"),
        (31, "Banco de Capacitor Nº 4 Cabos"),
        (32, "Painel-QGBT-1 Integridade"),
        (33, "Painel-QGBT-1 Tensão QG1-TR1"),
        (34, "Painel-QGBT-1 Corrente QG1"),
        (35, "Painel-QGBT-1 Tensão QG2-TR4"),
        (36, "Painel-QGBT-1 Corrente QG2-TR4"),
        (37, "Painel-QGBT-2 Integridade"),
        (38, "Painel-QGBT-2 Tensão QG1-TR2"),
        (39, "Painel-QGBT-2 Corrente QG1-TR2"),
        (40, "Painel-QGBT-2 Tensão QG2-TR3"),
        (41, "Painel-QGBT-2 Corrente QG2-TR3"),
        (42, "UPS - Integridade"),
        (43, "UPS - Tensão Bateria"),
        (44, "UPS - Tensão Entrada"),
        (45, "UPS - Tensão Saída"),
        (46, "Baterias - Integridade"),
        (47, "QAUX - Integridade"),
        (48, "QAUX - Tensão"),
        (49, "Leitos / Eletrocalhas Integridade"),
        (50, "Cabos Integridade"),
        (51, "Iluminação da SE Funcionamento"),
        (52, "Iluminação UPS Funcionamento"),
        (53, "Limpeza / organização"),
        (54, "Portas integridade"),
        (55, "Portas controle de acesso"),
        (56, "Aterramento Integridade"),
        (57, "Tapete de isolamento para manobra 1 peça"),
        (58, "Carrinho 1250A para manobra 1 peça"),
        (59, "Alavanca de Aterramento 1 peça"),
        (60, "Alavanca de Inserção / extração 1 peça"),
        (61, "Extintores carregados"),
        (62, "SPDA Integridade"),
        (63, "Climatização - Ventil./Exaustores"),
    ]

    sala_ups_ar = [
        (1, "Integridade"),
        (2, "Funcionamento"),
    ]

    sala_ups_status = [
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação Prensas", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_se_02_pintura()
        seed_se_montagem()
        seed_se_prensas()
        db.session.commit()
        print("\nPrimeiro lote cadastrado com sucesso.")
