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

def seed_se_01_pintura():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE 01 Pintura",
        codigo="CL-P1-003",
        descricao="Checklist diário de manutenção da SE 01 - Pintura.",
        area_padrao="MP - SE 01 - PINTURA",
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
        (33, "Painel-QGBT-1 Tensão QG3-TR1"),
        (34, "Painel-QGBT-1 Corrente QG3-TR1"),
        (35, "Painel-QGBT-1 Tensão QG4-TR2"),
        (36, "Painel-QGBT-1 Corrente QG4-TR2"),
        (37, "Painel-QGBT-2 Integridade"),
        (38, "Painel-QGBT-2 Tensão QG1-TR3"),
        (39, "Painel-QGBT-2 Corrente QG1-TR3"),
        (40, "Painel-QGBT-2 Tensão QG2-TR4"),
        (41, "Painel-QGBT-2 Corrente QG2-TR4"),
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
        (55, "Portas controle de acesso"),
        (56, "Aterramento - Integridade"),
        (57, "Tapete de isolamento para manobra 1 peça"),
        (58, "Carrinho 1250A para manobra 1 peça"),
        (59, "Alavanca de Aterramento 1 peça"),
        (60, "Alavanca de Inserção e extração 1 peça"),
        (61, "Manivela de abertura de painel 1 peça"),
        (62, "Extintores carregados"),
        (63, "Telhado integridade / vazamento / goteira"),
        (64, "Tomadas de uso geral - Integridade"),
        (65, "Tomadas de uso geral - Tensão"),
        (66, "Diagramas Unifilar"),
        (67, "Climatização - Ventil./Exaustores"),
        (68, "SPDA - Integridade"),
    ]

    ups1 = [
        (1, "Integridade"),
        (2, "Funcionamento"),
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    ups2 = [
        (1, "Integridade"),
        (2, "Funcionamento"),
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação Pintura 1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "UPS 1 Subestação 01 - 80 KVA", 2, ups1, usa_rst=False, usa_obs=True)
    add_section(modelo, "UPS 2 Subestação 01 - 40 KVA", 3, ups2, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 10, tipo_secao="observacoes_gerais")

def seed_se_zero():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - SE Zero",
        codigo="CL-ZRO-001",
        descricao="Checklist diário de manutenção da Subestação 0.",
        area_padrao="MP - SE-ZERO",
    )

    principais = [
        (1, 'PMT - Barra "A" Integridade'),
        (2, 'PMT - Barra "A" Tensão - Entrada'),
        (3, 'PMT - Barra "A" Corrente - Entrada'),
        (4, 'PMT - Barra "B" Integridade'),
        (5, 'PMT - Barra "B" Tensão - Entrada'),
        (6, 'PMT - Barra "B" Corrente - Entrada'),
        (7, 'PMT - Barra "C" Integridade'),
        (8, 'PMT - Barra "C" Tensão - Entrada'),
        (9, 'PMT - Barra "C" Corrente - Entrada'),
        (10, "UPS - Integridade"),
        (11, "UPS - Tensão Bateria"),
        (12, "UPS - Tensão Entrada"),
        (13, "UPS - Tensão Saída"),
        (14, "Baterias - Integridade"),
        (15, "TR01 440V-380/220V 315 KVA Integridade"),
        (16, "QCDZ-0 Climatização Integridade"),
        (17, "QCDZ-0 Climatização Tensão"),
        (18, "QCS-G Rede/Ger. Integridade"),
        (19, "QCS-G Rede/Ger. Tensão"),
        (20, "QAUX-HV-MV-380V Integridade"),
        (21, "QAUX-HV-MV-380V Tensão"),
        (22, "QAUX-MV-0 Integridade"),
        (23, "QAUX-MV-0 Tensão"),
        (24, "Leitos / Eletrocalhas Integridade"),
        (25, "Cabos Integridade"),
        (26, "SPDA - Integridade"),
        (27, "Iluminação Porão - Funcionamento"),
        (28, "Iluminação da SE Funcionamento"),
        (29, "Iluminação Bateria Funcionamento"),
        (30, "Limpeza e organização"),
        (31, "Portas integridade"),
        (32, "Portas controle de acesso"),
        (33, "Aterramento - Integridade"),
        (34, "Tapete de isolamento para manobra 3 peças"),
        (35, "Carrinho 1250A para manobra 1 peça"),
        (36, "Carrinho 4000A para manobra 1 peça"),
        (37, "Alavanca de Aterramento 1 peça"),
        (38, "Alavanca de Inserção e extração 1 peça"),
        (39, "Manivela de abertura de painel 3 peças"),
        (40, "Extintores carregados"),
        (41, "Telhado integridade / vazamento / goteira"),
        (42, "Tomadas Tensão / Integridade"),
        (43, "Climatização Funcionamento"),
        (44, "Diagramas Unifilar"),
    ]

    ups_zero = [
        (1, "Integridade"),
        (2, "Funcionamento"),
    ]

    status_zero = [
        (3, "Alarme"),
        (4, "Baterias"),
        (5, "Etiqueta baterias"),
    ]

    add_section(modelo, "Subestação 0", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "UPS Subestação 0", 2, ups_zero, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, status_zero, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 6, tipo_secao="observacoes_gerais")

def seed_bloco_d_rest_prensas():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Bloco D / Restaurante Prensas",
        codigo="CL-BLD-006",
        descricao="Checklist diário de manutenção da subestação Restaurante Prensas (Bloco D).",
        area_padrao="MP - SE - BLOCO D / REST. PRENSAS",
    )

    principais = [
        (1, "QS-PP Integridade"),
        (2, "QS-PP Tensão"),
        (3, "QS-PP Corrente"),
        (4, "QE-IG-PP Integridade"),
        (5, "QE-IG-PP Tensão"),
        (6, "QE-IG-PP Corrente"),
        (7, "TR-1 Auxiliar Integridade"),
        (8, "TR-1 Auxiliar Temperaturas"),
        (9, "QAE-02 Integridade"),
        (10, "QAE-02 Tensão"),
        (11, "QAE-02 Corrente"),
        (12, "QUPS-SE-PP Integridade"),
        (13, "QUPS-SE-PP Tensão"),
        (14, "QUPS-SE-PP Corrente"),
        (15, "Leitos / Eletrocalhas Integridade"),
        (16, "Cabos Integridade"),
        (17, "Iluminação SE Funcionamento"),
        (18, "Limpeza e organização"),
        (19, "Portas integridade"),
        (20, "Portas controle de acesso"),
        (21, "Aterramento Integridade"),
        (22, "Extintores carregados"),
        (23, "SPDA Integridade"),
        (24, "Climatização - Ventil./Exaustores"),
    ]

    add_section(modelo, "Subestação Restaurante Prensas", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 6, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_se_01_pintura()
        seed_se_zero()
        seed_bloco_d_rest_prensas()
        db.session.commit()
        print("\nTerceiro lote cadastrado com sucesso.")
