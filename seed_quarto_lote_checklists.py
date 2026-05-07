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

def seed_bloco_b():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Bloco B",
        codigo="CL-BLB-012",
        descricao="Checklist diário de manutenção da subestação Bloco B (Rest. Montagem).",
        area_padrao="MP - SE - BLOCO B",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "Banco de Capacitor Nº 1 Integridade"),
        (9, "Banco de Capacitor Nº 1 Tensão"),
        (10, "Banco de Capacitor Nº 1 Corrente"),
        (11, "Banco de Capacitor Nº 1 Contatores"),
        (12, "Banco de Capacitor Nº 1 Cabos"),
        (13, "Banco de Capacitor Nº 2 Integridade"),
        (14, "Banco de Capacitor Nº 2 Tensão"),
        (15, "Banco de Capacitor Nº 2 Corrente"),
        (16, "Banco de Capacitor Nº 2 Contatores"),
        (17, "Banco de Capacitor Nº 2 Cabos"),
        (18, "Painel-QGBT-1 Integridade"),
        (19, "Painel-QGBT-1 Tensão QG2-TR2"),
        (20, "Painel-QGBT-1 Corrente QG2-TR2"),
        (21, "Painel-QGBT-1 Tensão QG1-TR1"),
        (22, "Painel-QGBT-1 Corrente QG1-TR1"),
        (23, "Extintores carregados"),
        (24, "UPS - Tensão Bateria"),
        (25, "UPS - Tensão Entrada"),
        (26, "UPS - Tensão Saída"),
        (27, "Baterias Integridade"),
        (28, "Leitos / Eletrocalhas Integridade"),
        (29, "Cabos Integridade"),
        (30, "Iluminação da SE Funcionamento"),
        (31, "Iluminação UPS Funcionamento"),
        (32, "Limpeza / organização"),
        (33, "Portas integridade"),
        (34, "Portas controle de acesso"),
        (35, "Aterramento Integridade"),
        (36, "Tapete de isolamento para manobra 1 peça"),
        (37, "Carrinho 1250A para manobra 1 peça"),
        (38, "Alavanca de Aterramento 1 peça"),
        (39, "Alavanca de Inserção / extração 1 peça"),
        (40, "Manivela de abertura de painel 1 peça"),
        (41, "SPDA-Integridade"),
        (42, "Telhado integridade / vazamento / goteira"),
        (43, "Tomadas Tensão / Integridade"),
        (44, "Climatização UPS funcionamento"),
        (45, "Diagramas Unifilar"),
        (46, "QGBT-BB-100 Tensão"),
        (47, "QGBT-BB-101 Tensão"),
    ]

    add_section(modelo, "Subestação Bloco B (Rest. Montagem)", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_treinamento():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Treinamento",
        codigo="CL-TRN-011",
        descricao="Checklist diário de manutenção da subestação Treinamento.",
        area_padrao="MP - SE - TREINAMENTO",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "Banco de Capacitor Nº 1 Integridade"),
        (7, "Banco de Capacitor Capacitores"),
        (8, "Banco de Capacitor Disjuntores"),
        (9, "Banco de Capacitor Contatores"),
        (10, "Banco de Capacitor Cabos"),
        (11, "Painel-QGBT-1 Integridade"),
        (12, "Painel-QGBT-1 Tensão QG1-TR1"),
        (13, "Painel-QGBT-1 Corrente QG1"),
        (14, "QAUX-Integridade"),
        (15, "QAUX-Tensão"),
        (16, "UPS - Tensão Bateria"),
        (17, "UPS - Tensão Entrada"),
        (18, "UPS - Tensão Saída"),
        (19, "Baterias - Integridade"),
        (20, "Extintores carregados"),
        (21, "Aterramento - Integridade"),
        (22, "Leitos / Eletrocalhas Integridade"),
        (23, "Cabos Integridade"),
        (24, "Iluminação da SE Funcionamento"),
        (25, "Iluminação UPS Funcionamento"),
        (26, "Telhado integridade / vazamento / goteira"),
        (27, "Tomadas Tensão / Integridade"),
        (28, "Limpeza e organização"),
        (29, "Diagramas Unifilar"),
        (30, "Climatização - Ventil./Exaustores"),
        (31, "SPDA-Integridade"),
        (32, "Capacitores QGEP - Integridade"),
        (33, "Disjuntores QGEP - Tensão"),
        (34, "QGEP - Corrente"),
        (35, "QAE-01 Integridade"),
        (36, "QAE-01 Tensão"),
        (37, "QAE-01 Corrente"),
        (38, "Portas controle de acesso"),
        (39, "Portas integridade"),
        (40, "Manivela de abertura de painel 1 peça"),
        (41, "Tapete de isolamento para manobra 1 peça"),
        (42, "Carrinho 1250A para manobra 1 peça"),
        (43, "Alavanca de Aterramento 1 peça"),
        (44, "Alavanca de Inserção / extração 1 peça"),
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

    add_section(modelo, "Subestação Treinamento", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

def seed_bloco_c():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Bloco C / Ilha Ecológica",
        codigo="CL-BLC-013",
        descricao="Checklist diário de manutenção da subestação Ilha Ecológica / Bloco C.",
        area_padrao="MP - SE - BLOCO C - ILHA ECOL",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "Banco de Capacitor Nº 1 Integridade"),
        (7, "Banco de Capacitor Nº 1 Capacitores"),
        (8, "Banco de Capacitor Nº 1 Disjuntores"),
        (9, "Banco de Capacitor Nº 1 Contatores"),
        (10, "Banco de Capacitor Nº 1 Cabos"),
        (11, "Painel-QGBT-1 Integridade"),
        (12, "Painel-QGBT-1 QG1-TR1 Tensão"),
        (13, "Painel-QGBT-1 QG1-TR1 Corrente"),
        (14, "Extintores carregados"),
        (15, "UPS - Tensão Bateria"),
        (16, "UPS - Tensão Entrada"),
        (17, "UPS - Tensão Saída"),
        (18, "Baterias - Integridade"),
        (19, "QAUX - Integridade"),
        (20, "QAUX - Tensão"),
        (21, "Leitos / Eletrocalhas Integridade"),
        (22, "Cabos Integridade"),
        (23, "Iluminação da SE Funcionamento"),
        (24, "Iluminação UPS Funcionamento"),
        (25, "Telhado integridade / vazamento / goteira"),
        (26, "Limpeza / organização"),
        (27, "Portas integridade"),
        (28, "Portas controle de acesso"),
        (29, "Aterramento Integridade"),
        (30, "Tapete de isolamento para manobra 1 peça"),
        (31, "Carrinho 1250A para manobra 1 peça"),
        (32, "Alavanca de Aterramento 1 peça"),
        (33, "Alavanca de Inserção / extração 1 peça"),
        (34, "Manivela de abertura de painel 1 peça"),
        (35, "QGBT-BC-100 Escritório Ilha Integridade"),
        (36, "QGBT-BC-100 Escritório Ilha Tensão"),
        (37, "QDLF-BC-033 Prensa Papel Tensão"),
        (38, "QDLF-BC-026 Rec. Plástico Integridade"),
        (39, "QDLF-BC-026 Rec. Plástico Tensão"),
        (40, "Q12-Reciclagem Madeira Integridade"),
        (41, "Q12-Reciclagem Madeira Tensão"),
        (42, "QDLF-BC-020 Desc. Integridade"),
        (43, "QDLF-BC-020 Desc. Tensão"),
        (44, "BP-01/02 Sist. Pluvial Integridade"),
        (45, "BP-01/02 Sist. Pluvial Tensão"),
        (46, "Tomadas Tensão / Integridade"),
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

    add_section(modelo, "Subestação Ilha Ecológica", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

def seed_bloco_e():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Bloco E / Expedição",
        codigo="CL-BLE-018",
        descricao="Checklist diário de manutenção da subestação Expedição / Bloco E.",
        area_padrao="MP - SE - BLOCO E EXPEDIÇÃO",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "Banco de Capacitor Nr-1 Integridade"),
        (7, "Banco de Capacitor Capacitores"),
        (8, "Banco de Capacitor Disjuntores"),
        (9, "Banco de Capacitor Contatores"),
        (10, "Banco de Capacitor Cabos"),
        (11, "Painel-QGBT-1 Integridade"),
        (12, "Painel-QGBT-1 Tensão QG1-TR1"),
        (13, "Painel-QGBT-1 Corrente QG1"),
        (14, "Extintores carregados"),
        (15, "UPS - Tensão Bateria"),
        (16, "UPS - Tensão Entrada"),
        (17, "UPS - Tensão Saída"),
        (18, "Baterias - Integridade"),
        (19, "QUPS-Integridade"),
        (20, "QUPS-Tensão"),
        (21, "Leitos / Eletrocalhas Integridade"),
        (22, "Cabos Integridade"),
        (23, "Iluminação da SE Funcionamento"),
        (24, "Iluminação UPS Funcionamento"),
        (25, "Limpeza e organização"),
        (26, "Portas integridade"),
        (27, "Portas controle de acesso"),
        (28, "Aterramento - Integridade"),
        (29, "Tapete de isolamento para manobra 1 peça"),
        (30, "Carrinho 1250A para manobra 1 peça"),
        (31, "Alavanca de Aterramento 1 peça"),
        (32, "Alavanca de Inserção / extração 1 peça"),
        (33, "Manivela de abertura de painel 1 peça"),
        (34, "Extintores carregados"),
        (35, "Telhado integridade / vazamento / goteira"),
        (36, "QGBT-BE-100 Sala Elétrica - Tensão"),
        (37, "QGBT-BE-100 Sala Elétrica - Integridade"),
        (38, "QGBT-61.3-100 P6 - Tensão"),
        (39, "QGBT-61.3-100 P6 - Integridade"),
        (40, "QDLF-84-001 Galpão Tensão"),
        (41, "QDLF-84-001 Galpão Integridade"),
        (42, "QDLF-15.3-001 Vest. Mot. - Tensão"),
        (43, "QDLF-15.3-001 Vest. Mot. Integridade"),
        (44, "BB-03/04 Elev. Casa Bomb. Integridade"),
        (45, "BB-03/04 Elev. Casa Bomb. Tensão"),
        (46, "Tomadas Tensão / Integridade"),
        (47, "SPDA-Integridade"),
        (48, "Diagramas Unifilar"),
        (49, "Climatização - Ventil./Exaustores"),
    ]

    add_section(modelo, "Subestação Expedição", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_portaria_p7():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Portaria P7",
        codigo="CL-P7-014",
        descricao="Checklist diário de manutenção da subestação Portaria P7.",
        area_padrao="MP - SE-P7",
    )

    principais = [
        (1, "QGBT-QS-P7 380V Integridade"),
        (2, "QGBT-QS-P7 Tensão"),
        (3, "QGBT-QS-P7 Corrente"),
        (4, "TR-AUX 400kVA Integridade"),
        (5, "TR-AUX Tensão"),
        (6, "TR-AUX Temperatura"),
        (7, "QE-IG-P7 Integridade"),
        (8, "QE-IG-P7 Tensão"),
        (9, "QE-IG-P7 Corrente"),
        (10, "QAE-02 Integridade"),
        (11, "QAE-02 Tensão"),
        (12, "QAE-02 Corrente"),
        (13, "QUPS-SE-P7 Integridade"),
        (14, "QUPS-SE-P7 Tensão"),
        (15, "QUPS-SE-P7 Corrente"),
        (16, "Q1 Alim. Conv. Motor. Tensão"),
        (17, "Q2 Alim. FIAT SERV. Tensão"),
        (18, "Q3 Alim. Port. Perim. Tensão"),
        (19, "Q4 Alim. Port. Mat. Dir. Tensão"),
        (20, "QS-P7 Integridade"),
        (21, "QS-P7 Tensão"),
        (22, "QS-P7 Corrente"),
        (23, "Circuito de Iluminação Interna"),
        (24, "Circuito Iluminação Emergência"),
        (25, "Portas controle de acesso"),
        (26, "Interruptores Integridade"),
        (27, "SPDA Integridade"),
        (28, "Aterramento Integridade"),
        (29, "Extintores carregados"),
        (30, "Limpeza / organização"),
        (31, "Tomadas Tensão / Integridade"),
    ]

    add_section(modelo, "Subestação SE-P7", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 6, tipo_secao="observacoes_gerais")

def seed_sala_eletrica_bloco_d():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Sala Elétrica Bloco D",
        codigo="CL-SBD-017",
        descricao="Checklist diário de manutenção da Sala Elétrica Bloco D.",
        area_padrao="MP - SALA ELÉTRICA BLOCO D",
    )

    principais = [
        (1, "QGBT-BD-101 Sala Elét. Rest. Tensão"),
        (2, "QGBT-37.1-100 Vest. Tensão"),
        (3, "QGBT-61.1-100 PP Tensão"),
        (4, "QE-BD-02 Rampa de Alimentação Tensão"),
        (5, "QE-BD-03 Câmara Fria-Caldeira Tensão"),
        (6, "QE-37.1-001 Corredor Vestiário Tensão"),
        (7, "QGBT-BD-100 Vest. Tensão"),
        (8, "QDLF-BD-008 Ilumin. Tomadas Tensão"),
        (9, "QDLF-BD-009 Tomadas Tensão"),
        (10, "QDLF-BD-010 Lava Panela Forno Tensão"),
        (11, "Iluminação SE Funcionando"),
        (12, "Circuito de Tomadas"),
        (13, "Extintores Carregados"),
    ]

    add_section(modelo, "Sala Elétrica Bloco D", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 6, tipo_secao="observacoes_gerais")

def seed_sala_eletrica_bloco_a():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Sala Elétrica Bloco A",
        codigo="CL-SBA-016",
        descricao="Checklist diário de manutenção da Sala Elétrica Bloco A.",
        area_padrao="MP - SALA ELÉTRICA BLOCO A",
    )

    principais = [
        (1, "QGBT-BA-100 Integridade"),
        (2, "QGBT-BA-100 Tensão"),
        (3, "QGBT-BA-100 Corrente"),
        (4, "QGBT-BA-101 Integridade"),
        (5, "QGBT-BA-101 Tensão"),
        (6, "QGBT-BA-101 Corrente"),
        (7, "QDLF-BA-009 Integridade"),
        (8, "QDLF-BA-009 Tensão"),
        (9, "QDLF-BA-009 Corrente"),
        (10, "Circuito de Iluminação"),
        (11, "Circuito de Iluminação Emerg."),
        (12, "Circuito de Aterramento"),
        (13, "Limpeza / organização"),
        (14, "Extintores Carregados"),
    ]

    add_section(modelo, "Sala Elétrica Bloco A", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 6, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_bloco_b()
        seed_treinamento()
        seed_bloco_c()
        seed_bloco_e()
        seed_portaria_p7()
        seed_sala_eletrica_bloco_d()
        seed_sala_eletrica_bloco_a()
        db.session.commit()
        print("\nQuarto lote cadastrado com sucesso.")
