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


def seed_subestacao_denso():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Denso",
        codigo="CL-DEN-069",
        descricao="Checklist diário de manutenção da Subestação Denso.",
        area_padrao="SP06 - SE DENSO",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "UPS Integridade"),
        (5, "UPS Tensão Bateria"),
        (6, "UPS Tensão Entrada"),
        (7, "UPS Tensão Saída"),
        (8, "Baterias Integridade"),
        (9, "TR-1 Integridade"),
        (10, "TR-1 Temperaturas"),
        (11, "TR-1 Ventilação Forçada"),
        (12, "TR-2 Integridade"),
        (13, "TR-2 Temperaturas"),
        (14, "TR-2 Ventilação Forçada"),
        (15, "PN-QGBT-380V Integridade"),
        (16, "PN-QGBT-380V Tensão QG1-TR1"),
        (17, "PN-QGBT-380V Corrente QG1-TR1"),
        (18, "PN-QGBT-380V Integridade 2"),
        (19, "PN-QGBT-380V Tensão QG1-TR2"),
        (20, "PN-QGBT-380V Corrente QG1-TR2"),
        (21, "Painel ASP Integridade"),
        (22, "Painel ASP Tensão"),
        (23, "Leitos / Eletrocalhas Integridade"),
        (24, "Cabos Integridade"),
        (25, "Tomadas Integridade e Tensão"),
        (26, "Chave de abertura de painel 1 pç"),
        (27, "Quadro de Iluminação Viária"),
        (28, "Ar Condicionado - Sala de Baterias"),
        (29, "Diagrama Unifilar"),
        (30, "SPDA Integridade"),
        (31, "Climatização - Ventil./Exaustores"),
        (32, "Interruptores Integridade"),
        (33, "Extintores Carregados"),
        (34, "Iluminação da Sala Funcionamento"),
        (35, "Iluminação Bateria Funcionamento"),
        (36, "Limpeza e organização"),
        (37, "Portas integridade"),
        (38, "Portas controle de acesso"),
        (39, "Aterramento Integridade"),
        (40, "Tapete de isolamento para manobra 1 pç"),
        (41, "Alavanca de Aterramento 1 pç"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação Denso", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")


def seed_subestacao_2_pmc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 2 PMC SP01",
        codigo="CL-PMC2-068",
        descricao="Checklist diário de manutenção da Subestação 2 PMC.",
        area_padrao="SP01 - SE-2 PMC",
    )
    principais = [
        (1, "PMT-1 Integridade"),
        (2, "PMT-1 Tensão"),
        (3, "PMT-2 Integridade"),
        (4, "PMT-2 Tensão"),
        (5, "TR-3 Integridade"),
        (6, "TR-3 Temperaturas"),
        (7, "TR-4 Integridade"),
        (8, "TR-4 Temperaturas"),
        (9, "TR-4 Ventilação Forçada"),
        (10, "Painel-QGBT-440V Integridade"),
        (11, "Painel-QGBT-440V Tensão QG1-TR3"),
        (12, "Painel-QGBT-440V Corrente QG1-TR3"),
        (13, "Painel-QGBT-440V Integridade 2"),
        (14, "Painel-QGBT-440V Tensão QG1-TR4"),
        (15, "Painel-QGBT-440V Corrente QG1-TR4"),
        (16, "Painel ASP Integridade"),
        (17, "Painel ASP Tensão"),
        (18, "Leitos / Eletrocalhas Integridade"),
        (19, "Cabos Integridade"),
        (20, "Chave de abertura de painel 1 peça"),
        (21, "Quadro de Iluminação Viária"),
        (22, "Ar Condicionado - Sala de Baterias"),
        (23, "Climatização - Ventil./Exaustores"),
        (24, "TR-AUX Integridade"),
        (25, "TR-AUX Temperatura"),
        (26, "Interruptores Integridade"),
        (27, "Extintores Carregados"),
        (28, "Iluminação da Sala Funcionamento"),
        (29, "Limpeza e organização"),
        (30, "Portas integridade"),
        (31, "Portas controle de acesso"),
        (32, "Aterramento Integridade"),
        (33, "Tapete de isolamento para manobra 1 peça"),
        (34, "Alavanca de Aterramento 1 peça"),
        (35, "Diagrama Unifilar"),
        (36, "SPDA Integridade"),
    ]
    add_section(modelo, "Subestação 2", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_subestacao_1_pmc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 1 PMC SP01",
        codigo="CL-PMC1-067",
        descricao="Checklist diário de manutenção da Subestação 1 PMC.",
        area_padrao="SP01 - SE-1 PMC",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "UPS Integridade"),
        (5, "UPS Tensão Bateria"),
        (6, "UPS Tensão Entrada"),
        (7, "UPS Tensão Saída"),
        (8, "Baterias Integridade"),
        (9, "TR-1 Integridade"),
        (10, "TR-1 Temperaturas"),
        (11, "TR-1 Ventilação Forçada"),
        (12, "TR-2 Integridade"),
        (13, "TR-2 Temperaturas"),
        (14, "TR-2 Ventilação Forçada"),
        (15, "PN-QGBT-440V Integridade"),
        (16, "PN-QGBT-440V Tensão QG1-TR1"),
        (17, "PN-QGBT-440V Corrente QG1-TR1"),
        (18, "PN-QGBT-440V Integridade 2"),
        (19, "PN-QGBT-440V Tensão QG1-TR2"),
        (20, "PN-QGBT-440V Corrente QG1-TR2"),
        (21, "Painel ASP Integridade"),
        (22, "Painel ASP Tensão"),
        (23, "Leitos / Eletrocalhas Integridade"),
        (24, "Cabos Integridade"),
        (25, "Interruptores Integridade"),
        (26, "Quadro de Iluminação Viária"),
        (27, "Ar Condicionado - Sala de Baterias"),
        (28, "Diagrama Unifilar"),
        (29, "SPDA Integridade"),
        (30, "Climatização - Ventil./Exaustores"),
        (31, "TR-AUX Integridade"),
        (32, "TR-AUX Temperatura"),
        (33, "Extintores Carregados"),
        (34, "Iluminação da Sala Funcionamento"),
        (35, "Iluminação Bateria Funcionamento"),
        (36, "Limpeza e organização"),
        (37, "Portas integridade"),
        (38, "Portas controle de acesso"),
        (39, "Aterramento Integridade"),
        (40, "Tapete de isolamento para manobra 1 pç"),
        (41, "Alavanca de Aterramento 1 pç"),
        (42, "Chave de abertura de painel 1 pç"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação 1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")


def seed_subestacao_2_fmm():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 2 FMM SP09",
        codigo="CL-FMM2-071",
        descricao="Checklist diário de manutenção da Subestação 2 FMM.",
        area_padrao="SP09 - SE-2 FMM",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "TR-1 Integridade"),
        (5, "TR-1 Temperaturas"),
        (6, "TR-1 Ventilação Forçada"),
        (7, "TR-2 Integridade"),
        (8, "TR-2 Temperaturas"),
        (9, "TR-2 Ventilação Forçada"),
        (10, "Painel-QGBT-1-440V Integridade"),
        (11, "Painel-QGBT-1-440V Tensão QG1-TR-1"),
        (12, "Painel-QGBT-1-440V Corrente QG1-TR-1"),
        (13, "Painel-QGBT-2-440V Integridade"),
        (14, "Painel-QGBT-2-440V Tensão QG2-TR-2"),
        (15, "Painel-QGBT-2-440V Corrente QG2-TR-2"),
        (16, "TR-AUX Integridade"),
        (17, "TR-AUX Temperaturas"),
        (18, "Painel ASP Tensão"),
        (19, "Leitos / Eletrocalhas Integridade"),
        (20, "Cabos Integridade"),
        (21, "Tomadas Integridade e Tensão"),
        (22, "Interruptores Integridade"),
        (23, "Extintores Carregados"),
        (24, "Iluminação da SE Funcionamento"),
        (25, "Climatização - Ventil./Exaustores"),
        (26, "Limpeza e organização"),
        (27, "Portas integridade"),
        (28, "Portas controle de acesso"),
        (29, "Aterramento Integridade"),
        (30, "Tapete de isolamento para manobra 1 peça"),
        (31, "Alavanca de Aterramento 1 peça"),
        (32, "Chave de abertura de painel 1 peça"),
        (33, "Diagrama Unifilar"),
        (34, "Climatização da SE"),
    ]
    add_section(modelo, "Subestação 2 FMM", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_subestacao_1_fmm():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 1 FMM SP09",
        codigo="CL-FMM1-070",
        descricao="Checklist diário de manutenção da Subestação 1 FMM.",
        area_padrao="SP09 - SE-1 FMM",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "UPS Integridade"),
        (5, "UPS Tensão Bateria"),
        (6, "UPS Tensão Entrada"),
        (7, "UPS Tensão Saída"),
        (8, "Baterias Integridade"),
        (9, "TR-1 Integridade"),
        (10, "TR-1 Temperaturas"),
        (11, "TR-1 Ventilação Forçada"),
        (12, "TR-2 Integridade"),
        (13, "TR-2 Temperaturas"),
        (14, "TR-2 Ventilação Forçada"),
        (15, "TR-3 Integridade"),
        (16, "TR-3 Temperaturas"),
        (17, "TR-3 Ventilação Forçada"),
        (18, "TR-4 Integridade"),
        (19, "TR-4 Temperaturas"),
        (20, "TR-4 Ventilação Forçada"),
        (21, "TR-5 Integridade"),
        (22, "TR-5 Temperaturas"),
        (23, "TR-5 Ventilação Forçada"),
        (24, "TR-6 Integridade"),
        (25, "TR-6 Temperaturas"),
        (26, "TR-6 Ventilação Forçada"),
        (27, "TR-AUX Integridade"),
        (28, "TR-AUX Temperaturas"),
        (29, "Painel-QGBT-1-440V Integridade"),
        (30, "Painel-QGBT-1-440V Tensão QG1-TR-1"),
        (31, "Painel-QGBT-1-440V Corrente QG1-TR-1"),
        (32, "Painel-QGBT-440V Tensão QG2-TR2"),
        (33, "Painel-QGBT-440V Corrente QG2-TR2"),
        (34, "Painel-QGBT-440V Tensão QG3-TR3"),
        (35, "Painel-QGBT-440V Corrente QG3-TR3"),
        (36, "Painel-QGBT-2-440V Integridade"),
        (37, "Painel-QGBT-2-440V Tensão QG4-TR4"),
        (38, "Painel-QGBT-2-440V Corrente QG4-TR4"),
        (39, "Painel-QGBT-2-440V Tensão QG5-TR5"),
        (40, "Painel-QGBT-2-440V Corrente QG5-TR5"),
        (41, "Painel-QGBT-2-440V Tensão QG6-TR6"),
        (42, "Painel-QGBT-2-440V Corrente QG6-TR6"),
        (43, "Painel ASP Tensão"),
        (44, "Leitos / Eletrocalhas Integridade"),
        (45, "Cabos Integridade"),
        (46, "Tomadas Integridade e Tensão"),
        (47, "Interruptores Integridade"),
        (48, "Extintores Carregados"),
        (49, "Iluminação da SE Funcionamento"),
        (50, "Iluminação UPS Funcionamento"),
        (51, "Limpeza e organização"),
        (52, "Chave de abertura de painel 1 peça"),
        (53, "Portas integridade"),
        (54, "Portas controle de acesso"),
        (55, "Aterramento Integridade"),
        (56, "Tapete de isolamento para manobra 1 peça"),
        (57, "Alavanca de Aterramento 1 peça"),
        (58, "Ar Condicionado Sala de Baterias"),
        (59, "Climatização - Ventil. e Exaustores"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação 1 FMM", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")


def seed_subestacao_mmh():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação MMH",
        codigo="CL-MMH-072",
        descricao="Checklist diário de manutenção da Subestação MMH.",
        area_padrao="SP03 - SE-MMH",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "UPS Integridade"),
        (5, "UPS Tensão Bateria"),
        (6, "UPS Tensão Entrada"),
        (7, "UPS Tensão Saída"),
        (8, "Baterias Integridade"),
        (9, "TR-1 Integridade"),
        (10, "TR-1 Temperaturas"),
        (11, "TR-1 Ventilação Forçada"),
        (12, "TR-2 Integridade"),
        (13, "TR-2 Temperaturas"),
        (14, "TR-2 Ventilação Forçada"),
        (15, "Painel-QGBT-440V Integridade"),
        (16, "Painel-QGBT-440V Tensão QG1-TR1"),
        (17, "Painel-QGBT-440V Corrente QG1-TR1"),
        (18, "Painel-QGBT-440V Integridade 2"),
        (19, "Painel-QGBT-440V Tensão QG1-TR2"),
        (20, "Painel-QGBT-440V Corrente QG1-TR2"),
        (21, "Painel ASP Integridade"),
        (22, "Painel ASP Tensão"),
        (23, "Leitos / Eletrocalhas Integridade"),
        (24, "Cabos Integridade"),
        (25, "Tomadas Integridade e tensão"),
        (26, "Chave de abertura de painel 1 pç"),
        (27, "Quadro de Iluminação Viária"),
        (28, "Ar Condicionado - Sala de Baterias"),
        (29, "Diagrama Unifilar"),
        (30, "SPDA Integridade"),
        (31, "Climatização - Ventil./Exaustores"),
        (32, "TR-Aux Integridade"),
        (33, "TR-Aux Temperaturas"),
        (34, "Interruptores Integridade"),
        (35, "Extintores Carregados"),
        (36, "Iluminação da SE Funcionamento"),
        (37, "Iluminação UPS Funcionamento"),
        (38, "Limpeza e organização"),
        (39, "Portas integridade"),
        (40, "Portas controle de acesso"),
        (41, "Aterramento Integridade"),
        (42, "Tapete de isolamento para manobra 1 peça"),
        (43, "Alavanca de Aterramento 1 peça"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação MMH", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")


if __name__ == "__main__":
    with app.app_context():
        seed_subestacao_denso()
        seed_subestacao_2_pmc()
        seed_subestacao_1_pmc()
        seed_subestacao_2_fmm()
        seed_subestacao_1_fmm()
        seed_subestacao_mmh()
        db.session.commit()
        print("\\nDécimo segundo lote cadastrado com sucesso.")
