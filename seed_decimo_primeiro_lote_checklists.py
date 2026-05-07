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

def seed_subestacao_1_tiberina():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 1 Tiberina SP04",
        codigo="CL-TIB1-066",
        descricao="Checklist diário de manutenção da Subestação 1 Tiberina / Casa de Bombas.",
        area_padrao="SP04 - SE-1 TIBERINA CASA DE BOMBAS",
    )
    principais = [
        (1, "PMT-1 Integridade"),
        (2, "PMT-2 Integridade"),
        (3, "TR-1 Integridade"),
        (4, "TR-1 Temperaturas"),
        (5, "TR-1 Ventilação Forçada"),
        (6, "TR-2 Integridade"),
        (7, "TR-2 Temperaturas"),
        (8, "TR-2 Ventilação Forçada"),
        (9, "PN-QGBT-440V Integridade"),
        (10, "PN-QGBT-440V Tensão QG1-TR1"),
        (11, "PN-QGBT-440V Corrente QG1-TR1"),
        (12, "PN-QGBT-440V Tensão QG2-TR2"),
        (13, "PN-QGBT-440V Corrente QG2-TR2"),
        (14, "Painel ASP Integridade"),
        (15, "Painel ASP Tensão"),
        (16, "Leitos / Eletrocalhas Integridade"),
        (17, "Cabos Integridade"),
        (18, "Tomadas Integridade e Tensão"),
        (19, "Interruptores Integridade"),
        (20, "Extintores Carregados"),
        (21, "Iluminação da Sala Funcionamento"),
        (22, "Limpeza e organização"),
        (23, "Portas integridade"),
        (24, "Portas controle de acesso"),
        (25, "Aterramento Integridade"),
        (26, "Tapete de isolamento para manobra 1 pç"),
        (27, "Alavanca de Aterramento 1 pç"),
        (28, "Quadro de Iluminação Viária Tensão"),
        (29, "Diagrama Unifilar"),
        (30, "TR-AUXILIAR Integridade"),
        (31, "TR-AUXILIAR Temperaturas"),
        (32, "SPDA Integridade"),
    ]
    add_section(modelo, "Subestação 1", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_revest_coat():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Revest Coat",
        codigo="CL-RVC-064",
        descricao="Checklist diário de manutenção da Subestação Revest Coat.",
        area_padrao="SP02 - SE-REVEST COAT",
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
        (9, "TR-AUX Integridade"),
        (10, "TR-AUX Temperaturas"),
        (11, "TR-1 Integridade"),
        (12, "TR-1 Temperaturas"),
        (13, "TR-1 Ventilação Forçada"),
        (14, "TR-2 Integridade"),
        (15, "TR-2 Temperaturas"),
        (16, "TR-2 Ventilação Forçada"),
        (17, "Painel-QGBT-440V Integridade"),
        (18, "Painel-QGBT-440V Tensão QG1-TR1"),
        (19, "Painel-QGBT-440V Corrente QG1-TR1"),
        (20, "Painel-QGBT-440V Integridade 2"),
        (21, "Painel-QGBT-440V Tensão QG1-TR2"),
        (22, "Painel-QGBT-440V Corrente QG1-TR2"),
        (23, "Painel ASP Integridade"),
        (24, "Painel ASP Tensão"),
        (25, "Leitos / Eletrocalhas Integridade"),
        (26, "Cabos Integridade"),
        (27, "Tomadas Integridade e Tensão"),
        (28, "Chave de abertura de painel 1 peça"),
        (29, "Ar Condicionado - Sala de Baterias"),
        (30, "Diagrama Unifilar"),
        (31, "SPDA Integridade"),
        (32, "Climatização - Ventil./Exaustores"),
        (33, "Interruptores Integridade"),
        (34, "Extintores Carregados"),
        (35, "Iluminação da SE Funcionamento"),
        (36, "Iluminação UPS Funcionamento"),
        (37, "Limpeza e organização"),
        (38, "Portas integridade"),
        (39, "Portas controle de acesso"),
        (40, "Aterramento Integridade"),
        (41, "Tapete de isolamento para manobra 1 peça"),
        (42, "Alavanca de Aterramento 1 peça"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação Revest Coat", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_adler():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação Adler",
        codigo="CL-ADL-063",
        descricao="Checklist diário de manutenção da Subestação Adler.",
        area_padrao="SP13 - SE-ADLER",
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
        (25, "Tomadas Integridade e Tensão"),
        (26, "TRAFO AUXILIAR TEMPERATURA"),
        (27, "TRAFO AUXILIAR INTEGRIDADE"),
        (28, "Chave de abertura de painel 1 pç"),
        (29, "Ar Condicionado - Sala de Baterias"),
        (30, "Diagrama Unifilar"),
        (31, "SPDA Integridade"),
        (32, "Climatização - Ventil./Exaustores"),
        (33, "Interruptores Integridade"),
        (34, "Extintores Carregados"),
        (35, "Iluminação da Sala Funcionamento"),
        (36, "Iluminação Bateria Funcionamento"),
        (37, "Limpeza e organização"),
        (38, "Portas integridade"),
        (39, "Portas controle de acesso"),
        (40, "Aterramento Integridade"),
        (41, "Tapete de isolamento para manobra 1 pç"),
        (42, "Alavanca de Aterramento 1 pç"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação Adler", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_22():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 22",
        codigo="CL-SE22-062",
        descricao="Checklist diário de manutenção da Subestação 22.",
        area_padrao="SP22 - SE-22",
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
        (26, "Interruptores Integridade"),
        (27, "Extintores Carregados"),
        (28, "Iluminação da Sala Funcionamento"),
        (29, "Iluminação Bateria Funcionamento"),
        (30, "Limpeza e organização"),
        (31, "Portas integridade"),
        (32, "Portas controle de acesso"),
        (33, "Aterramento Integridade"),
        (34, "Tapete de isolamento para manobra 1 pç"),
        (35, "Alavanca de Aterramento 1 pç"),
        (36, "Ar Condicionado - Sala de Baterias"),
        (37, "Diagrama Unifilar"),
        (38, "SPDA Integridade"),
        (39, "Climatização - Ventil./Exaustores"),
        (40, "Quadro de Iluminação Viária Tensão"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação 22", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_21():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 21",
        codigo="CL-SE21-061",
        descricao="Checklist diário de manutenção da Subestação 21.",
        area_padrao="SP21 - SE-21",
    )
    principais = [
        (1, 'PMT-Barra "A" Integridade'),
        (2, 'PMT-ENTRADA "A" Tensão'),
        (3, 'PMT-ENTRADA "A" Corrente'),
        (4, 'PMT-Barra "B" Integridade'),
        (5, 'PMT-ENTRADA "B" Tensão'),
        (6, 'PMT-ENTRADA "B" Corrente'),
        (7, 'PMT-Barra "C" Integridade'),
        (8, 'PMT-ENTRADA "C" Tensão'),
        (9, 'PMT-ENTRADA "C" Corrente'),
        (10, "UPS Integridade"),
        (11, "UPS Tensão Bateria"),
        (12, "UPS Tensão Entrada"),
        (13, "UPS Tensão Saída"),
        (14, "Baterias Integridade"),
        (15, "TR-1 Integridade"),
        (16, "TR-1 Temperaturas"),
        (17, "TR-2 Integridade"),
        (18, "TR-2 Temperaturas"),
        (19, "TR-3 Integridade"),
        (20, "TR-3 Temperaturas"),
        (21, "Painel-QGBT-440V Integridade"),
        (22, "Painel-QGBT-440V Tensão QG1-TR1"),
        (23, "Painel-QGBT-440V Corrente QG1-TR1"),
        (24, "Painel-QGBT-440V Tensão QG2-TR2"),
        (25, "Painel-QGBT-440V Corrente QG2-TR2"),
        (26, "Painel-QGBT-380V Integridade"),
        (27, "Painel-QGBT-380V Tensão QG1-TR3"),
        (28, "Painel-QGBT-380V Corrente QG1-TR3"),
        (29, "Painel ASP Integridade"),
        (30, "Painel ASP Tensão"),
        (31, "Leitos / Eletrocalhas Integridade"),
        (32, "Cabos Integridade"),
        (33, "Tomadas Integridade e Tensão"),
        (34, "Interruptores Integridade"),
        (35, "Extintores Carregados"),
        (36, "Chave de abertura de painel 3 peça"),
        (37, "Quadro de Iluminação Viária"),
        (38, "TR1-Ventilação Forçada"),
        (39, "TR2-Ventilação Forçada"),
        (40, "TR3-Ventilação Forçada"),
        (41, "Diagrama Unifilar"),
        (42, "SPDA Integridade"),
        (43, "Climatização - Ventil./Exaustores"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta de Baterias")]
    add_section(modelo, "Subestação 21", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

def seed_subestacao_2_tiberina():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Subestação 2 Tiberina SP04",
        codigo="CL-TIB2-065",
        descricao="Checklist diário de manutenção da Subestação 2 Tiberina / CMA / MMH.",
        area_padrao="SP04 - SE 2 TIBERINA / CMA / MMH",
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
        (9, "TR-3 Integridade"),
        (10, "TR-3 Temperaturas"),
        (11, "TR-3 Ventilação Forçada"),
        (12, "TR-4 Integridade"),
        (13, "TR-4 Temperaturas"),
        (14, "TR-4 Ventilação Forçada"),
        (15, "TR-5 Integridade"),
        (16, "TR-5 Temperaturas"),
        (17, "TR-5 Ventilação Forçada"),
        (18, "TR-6 Integridade"),
        (19, "TR-6 Temperaturas"),
        (20, "TR-6 Ventilação Forçada"),
        (21, "TR-7 Integridade"),
        (22, "TR-7 Temperaturas"),
        (23, "TR-7 Ventilação Forçada"),
        (24, "PN-QGBT-440V Integridade"),
        (25, "PN-QGBT-440V Tensão QG1-TR3"),
        (26, "PN-QGBT-440V Corrente QG1-TR3"),
        (27, "Painel ASP Integridade"),
        (28, "Painel ASP Tensão"),
        (29, "Leitos / Eletrocalhas Integridade"),
        (30, "Cabos Integridade"),
        (31, "Tomadas Integridade e Tensão"),
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
        (42, "Chave de abertura de painel 1 pç"),
        (43, "Iluminação Externa do prédio Q-ASP"),
        (44, "Ar Condicionado - Sala de Baterias"),
        (45, "Diagrama Unifilar"),
        (46, "SPDA Integridade"),
        (47, "PN-QGBT-440V Integridade TR7"),
        (48, "PN-QGBT-440V Tensão QG1-TR7"),
        (49, "PN-QGBT-440V Corrente QG1-TR7"),
        (50, "TR-AUXILIO 01 Integridade"),
        (51, "TR-AUXILIO 02 Temperatura"),
        (52, "TR-AUXILIAR 2 Integridade"),
        (53, "PN-QGBT-440V Integridade TR6"),
        (54, "PN-QGBT-440V Tensão QG1-TR6"),
        (55, "PN-QGBT-440V Corrente QG1-TR6"),
        (56, "PN-QGBT-440V Integridade TR5"),
        (57, "PN-QGBT-440V Tensão QG1-TR5"),
        (58, "PN-QGBT-440V Corrente QG1-TR5"),
        (59, "PN-QGBT-440V Integridade TR4"),
        (60, "PN-QGBT-440V Tensão QG1-TR4"),
        (61, "PN-QGBT-440V Corrente QG1-TR4"),
        (62, "Climatização - Ventil./Exaustores"),
    ]
    sala_ups_ar = [(1, "Integridade"), (2, "Funcionamento")]
    sala_ups_status = [(3, "Alarme"), (4, "Baterias"), (5, "Etiqueta baterias")]
    add_section(modelo, "Subestação 2", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Sala UPS - Ar Condicionado", 2, sala_ups_ar, usa_rst=False, usa_obs=True)
    add_section(modelo, "Sala UPS - Status", 3, sala_ups_status, usa_rst=False, usa_obs=True)
    add_section(modelo, "Observações gerais", 4, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_subestacao_1_tiberina()
        seed_subestacao_revest_coat()
        seed_subestacao_adler()
        seed_subestacao_22()
        seed_subestacao_21()
        seed_subestacao_2_tiberina()
        db.session.commit()
        print("\\nDécimo primeiro lote cadastrado com sucesso.")
