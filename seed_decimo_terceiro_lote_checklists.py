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

def seed_subestacao_2_prima_sole():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 2 Prima Sole SP12",
        codigo="CL-PS2-075",
        descricao="Checklist diário de manutenção da Subestação 2 Prima Sole / Casa de Bombas.",
        area_padrao="SP12 - SE2 BROSE PS / CASA DE BOMBAS",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "PMT Tensão"),
        (3, "PMT Corrente"),
        (4, "TR-5 Integridade"),
        (5, "TR-5 Temperaturas"),
        (6, "TR-5 Ventilação Forçada"),
        (7, "TR-6 Integridade"),
        (8, "TR-6 Temperaturas"),
        (9, "TR-6 Ventilação Forçada"),
        (10, "TR-AUX Integridade"),
        (11, "TR-AUX Temperaturas"),
        (12, "Painel-QGBT-440V Integridade"),
        (13, "Painel-QGBT-440V Tensão QG1-TR6"),
        (14, "Painel-QGBT-440V Corrente QG1-TR6"),
        (15, "Painel-QGBT-440V Tensão QG2-TR5"),
        (16, "Painel-QGBT-440V Corrente QG2-TR5"),
        (17, "Leitos / Eletrocalhas Integridade"),
        (18, "Cabos Integridade"),
        (19, "Tomadas Integridade e Tensão"),
        (20, "Interruptores Integridade"),
        (21, "Extintores Carregados"),
        (22, "Iluminação da SE Funcionamento"),
        (23, "Limpeza e organização"),
        (24, "Portas integridade"),
        (25, "Portas controle de acesso"),
        (26, "Aterramento Integridade"),
        (27, "Tapete de isolamento para manobra 1 peça"),
        (28, "Alavanca de Aterramento 1 peça"),
        (29, "Chave de abertura de painel 1 peça"),
        (30, "Diagrama Unifilar"),
        (31, "CCM-1 Tensão"),
        (32, "CCM-1 Corrente"),
        (33, "CCM-2 Tensão"),
        (34, "CCM-2 Corrente"),
    ]
    add_section(modelo, "Subestação 2 - Casa de Bombas", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_lear():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Lear",
        codigo="CL-LER-074",
        descricao="Checklist diário de manutenção da Subestação Lear.",
        area_padrao="SP15 - LEAR",
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
        (15, "Painel-QGBT-380V Integridade"),
        (16, "Painel-QGBT-380V Tensão QG1-TR1"),
        (17, "PN-QGBT-380V Corrente QG1-TR1"),
        (18, "Painel-QGBT-380V Integridade 2"),
        (19, "Painel-QGBT-380V Tensão QG1-TR2"),
        (20, "Painel-QGBT-380V Corrente QG1-TR2"),
        (21, "Painel ASP Integridade"),
        (22, "Painel ASP Tensão"),
        (23, "Leitos / Eletrocalhas Integridade"),
        (24, "Cabos Integridade"),
        (25, "Tomadas Integridade e Tensão"),
        (26, "Interruptores Integridade e Tensão"),
        (27, "Extintores Carregados"),
        (28, "Iluminação da Sala Funcionamento"),
        (29, "Iluminação Bateria Funcionamento"),
        (30, "Limpeza e organização"),
        (31, "Portas Integridade"),
        (32, "Portas controle de acesso"),
        (33, "Aterramento Integridade"),
        (34, "Tapete de isolamento para manobra 1 peça"),
        (35, "Alavanca de Aterramento 1 peça"),
        (36, "Chave de abertura de painel 1 peça"),
        (37, "SPDA Integridade"),
        (38, "Climatização - Ventil./Exaustores"),
        (39, "Diagrama Unifilar"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação Lear", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_1_prima_sole():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 1 Prima Sole SP12",
        codigo="CL-PS1-073",
        descricao="Checklist diário de manutenção da Subestação 1 Brose / Prima Sole e Galpão.",
        area_padrao="SP12 - SE-1 BROSE / PRIMA SOLE E GALPÃO",
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
        (21, "TR-AUX Integridade"),
        (22, "TR-AUX Temperaturas"),
        (23, "PN-QGBT-1-440V Integridade"),
        (24, "Painel-QGBT-1-440V Tensão QG1-TR-1"),
        (25, "Painel-QGBT-1-440V Corrente QG1-TR-1"),
        (26, "Painel-QGBT-440V Tensão QG2-TR2"),
        (27, "Painel-QGBT-440V Corrente QG2-TR2"),
        (28, "Painel-QGBT-1-440V Tensão QG1-TR-3"),
        (29, "Painel-QGBT-1-440V Corrente QG1-TR-3"),
        (30, "Painel-QGBT-440V Tensão QG2-TR4"),
        (31, "Painel-QGBT-440V Corrente QG2-TR4"),
        (32, "Iluminação da SE Funcionamento"),
        (33, "Iluminação UPS Funcionamento"),
        (34, "Limpeza e organização"),
        (35, "Portas integridade"),
        (36, "Portas controle de acesso"),
        (37, "Aterramento Integridade"),
        (38, "Tapete de isolamento para manobra 1 peça"),
        (39, "Alavanca de Aterramento 1 peça"),
        (40, "Chave de abertura de painel 1 peça"),
        (41, "Climatização - Ventil./Exaustores"),
        (42, "Diagrama Unifilar"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação 1 - Brose Prima Sole", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_pirelli():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Pirelli",
        codigo="CL-PIR-077",
        descricao="Checklist diário de manutenção da Subestação Pirelli.",
        area_padrao="SP14 - SE-PIRELLI",
    )
    principais = [
        (1, "PMT Integridade"),
        (2, "UPS Integridade"),
        (3, "UPS Tensão Bateria"),
        (4, "UPS Tensão Entrada"),
        (5, "UPS Tensão Saída"),
        (6, "Baterias Integridade"),
        (7, "TR-1 Integridade"),
        (8, "TR-1 Temperaturas"),
        (9, "TR-1 Ventilação Forçada"),
        (10, "TR-2 Integridade"),
        (11, "TR-2 Temperaturas"),
        (12, "TR-2 Ventilação Forçada"),
        (13, "TR-Aux Integridade"),
        (14, "TR-Aux Temperaturas"),
        (15, "Painel-QGBT-440V Integridade"),
        (16, "Painel-QGBT-440V Tensão QG1-TR1"),
        (17, "Painel-QGBT-440V Corrente QG1-TR1"),
        (18, "Painel-QGBT-440V Tensão QG2-TR2"),
        (19, "Painel-QGBT-440V Corrente QG2-TR2"),
        (20, "Painel ASP Integridade"),
        (21, "Painel ASP Tensão"),
        (22, "Leitos / Eletrocalhas Integridade"),
        (23, "Cabos Integridade"),
        (24, "Tomadas Integridade e Tensão"),
        (25, "Interruptores Integridade"),
        (26, "Aterramento Integridade"),
        (27, "Climatização - Ventil./Exaustores"),
        (28, "Extintores Carregados"),
        (29, "Circuito Iluminação da SE"),
        (30, "Iluminação UPS Funcionamento"),
        (31, "Limpeza e organização"),
        (32, "Portas integridade"),
        (33, "Portas controle de acesso"),
        (34, "Diagrama Unifilar"),
        (35, "Tapete de isolamento para manobra 1 peça"),
        (36, "Alavanca de Aterramento 1 peça"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação Pirelli", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_saint_gobain():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Saint Gobain",
        codigo="CL-SGB-076",
        descricao="Checklist diário de manutenção da Subestação Saint Gobain.",
        area_padrao="SP05 - SE-SAINT GOBAIN",
    )
    principais = [
        (1, "QGBT Integridade"),
        (2, "QGBT Tensão"),
        (3, "QGBT Corrente"),
        (4, "Leitos / Eletrocalhas Integridade"),
        (5, "Cabos Integridade"),
    ]
    add_section(modelo, "Subestação Saint Gobain", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_subestacao_2_prima_sole()
        seed_subestacao_lear()
        seed_subestacao_1_prima_sole()
        seed_subestacao_pirelli()
        seed_subestacao_saint_gobain()
        db.session.commit()
        print("\nDécimo terceiro lote cadastrado com sucesso.")
