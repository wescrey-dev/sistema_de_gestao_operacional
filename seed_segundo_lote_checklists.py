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

def seed_se_ete():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE WWT (ETE)",
        codigo="CL-ETE-002",
        descricao="Checklist diário de manutenção da subestação WWT (ETE).",
        area_padrao="MP - SE-WWT (ETE)",
    )

    principais = [
        (1, "PMT - Integridade"),
        (2, "PMT - Tensão"),
        (3, "PMT - Corrente"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "Painel-QGBT Integridade"),
        (9, "Painel-QGBT Tensão QG1"),
        (10, "Painel-QGBT Corrente QG1"),
        (11, "Painel-QGBT Tensão QG2"),
        (12, "Painel-QGBT Corrente QG2"),
        (13, "UPS - Integridade"),
        (14, "UPS - Tensão Bateria"),
        (15, "UPS - Tensão Entrada"),
        (16, "UPS - Tensão Saída"),
        (17, "Baterias - Integridade"),
        (18, "QAUX - Integridade"),
        (19, "QAUX - Tensão"),
        (20, "Leitos / Eletrocalhas Integridade"),
        (21, "Cabos Integridade"),
        (22, "Iluminação da SE Funcionamento"),
        (23, "Iluminação Sala UPS Funcionamento"),
        (24, "Limpeza e organização"),
        (25, "Portas integridade"),
        (26, "Portas controle de acesso"),
        (27, "Aterramento - Integridade"),
        (28, "Tapete de isolamento para manobra 1 peça"),
        (29, "Carrinho 1250A para manobra 1 peça"),
        (30, "Alavanca de Aterramento 1 peça"),
        (31, "Alavanca de Inserção e extração 1 peça"),
        (32, "Manivela de abertura de painel 1 peça"),
        (33, "Extintores carregados"),
        (34, "Telhado integridade / vazamento / goteira"),
        (35, "Tomadas de uso geral - Integridade"),
        (36, "Tomadas de uso geral - Tensão"),
        (37, "Diagramas Unifilar"),
        (38, "Climatização - Ventil./Exaustores"),
        (39, "SPDA - Integridade"),
        (40, "Banco de Capacitor Nº 1 Integridade"),
        (41, "Banco de Capacitor Nº 1 Tensão"),
        (42, "Banco de Capacitor Nº 1 Corrente"),
        (43, "Banco de Capacitor Nº 1 Contatores"),
        (44, "Banco de Capacitor Nº 1 Cabos"),
        (45, "Banco de Capacitor Nº 2 Integridade"),
        (46, "Banco de Capacitor Nº 2 Tensão"),
        (47, "Banco de Capacitor Nº 2 Corrente"),
        (48, "Banco de Capacitor Nº 2 Contatores"),
        (49, "Banco de Capacitor Nº 2 Cabos"),
    ]

    ups_ete = [
        (1, "Integridade"),
        (2, "Funcionamento"),
    ]

    status_ete = [
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação WWT", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "UPS Subestação WWT", 2, ups_ete, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, status_ete, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_se_cdc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE CDC",
        codigo="CL-CDC-010",
        descricao="Checklist diário de manutenção da subestação CDC.",
        area_padrao="MP - SE - CDC",
    )

    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão Entrada"),
        (3, "PMT Corrente Entrada"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-1 Vent. Forçada Teste"),
        (7, "TR-2 Integridade"),
        (8, "TR-2 Temperaturas"),
        (9, "TR-2 Vent. Forçada Teste"),
        (10, "PN-QGBT Integridade"),
        (11, "PN-QGBT Tensão QG1"),
        (12, "PN-QGBT Corrente QG1"),
        (13, "PN-QGBT Tensão QG2"),
        (14, "PN-QGBT Corrente QG2"),
        (15, "PAINEL ASP Integridade"),
        (16, "PAINEL ASP Tensão"),
        (17, "TRAFO AUX-3 Integridade"),
        (18, "TRAFO AUX-3 Temperaturas"),
        (19, "TRAFO AUX-4 Integridade"),
        (20, "TRAFO AUX-4 Temperaturas"),
        (21, "TRAFO AUX-5 Integridade"),
        (22, "TRAFO AUX-5 Temperaturas"),
        (23, "UPS - Integridade"),
        (24, "UPS - Tensão Bateria"),
        (25, "UPS - Tensão Entrada"),
        (26, "UPS - Tensão Saída"),
        (27, "Baterias - Integridade"),
        (28, "QAUX - Integridade"),
        (29, "QAUX - Tensão"),
        (30, "Leitos / Eletrocalhas Integridade"),
        (31, "Cabos Integridade"),
        (32, "Iluminação da SE Funcionamento"),
        (33, "Iluminação UPS Funcionamento"),
        (34, "Tomadas Tensão / Integridade"),
        (35, "Limpeza e organização"),
        (36, "Diagramas Unifilar"),
        (37, "Climatização Funcionamento"),
        (38, "Climatização - Ventil./Exaustores"),
        (39, "SPDA - Integridade"),
        (40, "Portas integridade"),
        (41, "Telhado integridade / vazamento / goteira"),
        (42, "Portas controle de acesso"),
        (43, "Aterramento Integridade"),
        (44, "Tapete de isolamento para manobra 1 peça"),
        (45, "Alavanca de Inserção e extração 1 peça"),
        (46, "Manivela de abertura de painel 1 peça"),
        (47, "Extintores carregados"),
        (48, "QGIP - Alim. QG Ilum. Pátios"),
        (49, "QGIP1 Tensão"),
        (50, "QGIP2 Tensão"),
        (51, "QGIP3 Tensão"),
        (52, "Painel Gerador 2 440V Alim SL Bat."),
        (53, "SP/Col.6QGBT Alim. Pressere Col.A16"),
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

    add_section(modelo, "Subestação CDC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_se_funilaria():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Funilaria",
        codigo="CL-FUN-007",
        descricao="Checklist diário de manutenção da subestação Funilaria.",
        area_padrao="MP - SE-FUNILARIA",
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
        (12, "TR-5 Integridade"),
        (13, "TR-5 Temperaturas"),
        (14, "Banco de Capacitor Nº 1 Integridade"),
        (15, "Banco de Capacitor Nº 1 Tensão"),
        (16, "Banco de Capacitor Nº 1 Corrente"),
        (17, "Banco de Capacitor Nº 1 Contatores"),
        (18, "Banco de Capacitor Nº 1 Cabos"),
        (19, "Banco de Capacitor Nº 2 Integridade"),
        (20, "Banco de Capacitor Nº 2 Tensão"),
        (21, "Banco de Capacitor Nº 2 Corrente"),
        (22, "Banco de Capacitor Nº 2 Contatores"),
        (23, "Banco de Capacitor Nº 2 Cabos"),
        (24, "Banco de Capacitor Nº 3 Integridade"),
        (25, "Banco de Capacitor Nº 3 Tensão"),
        (26, "Banco de Capacitor Nº 3 Corrente"),
        (27, "Banco de Capacitor Nº 3 Contatores"),
        (28, "Banco de Capacitor Nº 3 Cabos"),
        (29, "Painel-QGBT-1 Integridade"),
        (30, "Painel-QGBT-1 Tensão QG1-TR1"),
        (31, "Painel-QGBT-1 Corrente QG1-TR1"),
        (32, "Painel-QGBT-1 Tensão QG2-TR2"),
        (33, "Painel-QGBT-1 Corrente QG2-TR2"),
        (34, "Painel-QGBT-1 Tensão QG3-TR5"),
        (35, "Painel-QGBT-1 Corrente QG3-TR5"),
        (36, "Painel-QGBT-2 Integridade"),
        (37, "Painel-QGBT-2 Tensão QG1-TR3"),
        (38, "Painel-QGBT-2 Corrente QG1-TR3"),
        (39, "Painel-QGBT-2 Tensão QG2-TR4"),
        (40, "Painel-QGBT-2 Corrente TR4"),
        (41, "UPS - Integridade"),
        (42, "UPS - Tensão Bateria"),
        (43, "UPS - Tensão Entrada"),
        (44, "UPS - Tensão Saída"),
        (45, "Baterias - Integridade"),
        (46, "QAUX - Integridade"),
        (47, "QAUX - Tensão"),
        (48, "Cabos Integridade"),
        (49, "Iluminação da SE Funcionamento"),
        (50, "Limpeza e organização"),
        (51, "Portas integridade"),
        (52, "Aterramento Integridade"),
        (53, "Tapete de isolamento para manobra 1 peça"),
        (54, "Carrinho 1250A para manobra 1 peça"),
        (55, "Alavanca de Aterramento 1 peça"),
        (56, "Alavanca de Inserção e extração 1 peça"),
        (57, "Extintores carregados"),
        (58, "Climatização - Ventil./Exaustores"),
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

    add_section(modelo, "Subestação Funilaria", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_se_ete()
        seed_se_cdc()
        seed_se_funilaria()
        db.session.commit()
        print("\nSegundo lote cadastrado com sucesso.")
