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


def seed_casa_bombas_adler():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas Adler",
        codigo="CL-CBAD-081",
        descricao="Checklist diário de manutenção da Casa de Bombas Adler.",
        area_padrao="SP - CASA DE BOMBAS ADLER",
    )
    principais = [
        (1, "QD-1.2KV-13MCC01 Integridade"),
        (2, "QD-1.2KV-13MCC01 Tensão"),
        (3, "QM8 - Chiller 1 Integridade"),
        (4, "QM8 - Chiller 1 Tensão"),
        (5, "QM9 - Chiller 2 Integridade"),
        (6, "QM9 - Chiller 2 Tensão"),
        (7, "Circuito de Iluminação Interna"),
        (8, "Circuito Iluminação Emergência"),
        (9, "Tomadas Integridade e Tensão"),
        (10, "Aterramento Integridade"),
        (11, "Portas de acesso"),
        (12, "EP01A - Bomba do Chiller 1 Integridade"),
        (13, "EP01A - Bomba do Chiller 1 Tensão"),
        (14, "EP01B - Bomba do Chiller 1 Integridade"),
        (15, "EP01B - Bomba do Chiller 1 Tensão"),
        (16, "EP01C - Bomba do Chiller 1 Integridade"),
        (17, "EP01C - Bomba do Chiller 1 Tensão"),
        (18, "EP02A - Bomba do Processo Integridade"),
        (19, "EP02A - Bomba do Processo Tensão"),
        (20, "EP02B - Bomba do Processo Integridade"),
        (21, "EP02B - Bomba do Processo Tensão"),
    ]
    add_section(modelo, "Casa de Bombas Adler", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_revest_coat():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas Revest Coat",
        codigo="CL-CBRC-082",
        descricao="Checklist diário de manutenção da Casa de Bombas Revest Coat.",
        area_padrao="SP - CASA DE BOMBAS REVEST COAT",
    )
    principais = [
        (1, "QECP-440V Integridade"),
        (2, "QECP-440V Tensão"),
        (3, "9QF1 - FM-5 Integridade"),
        (4, "9QF1 - FM-5 Tensão"),
        (5, "9QF2 - FM-6 Integridade"),
        (6, "9QF2 - FM-6 Tensão"),
        (7, "9QF3 - FM-7 Integridade"),
        (8, "9QF3 - FM-7 Tensão"),
        (9, "10QF1 - FM-1 Integridade"),
        (10, "10QF1 - FM-1 Tensão"),
        (11, "10QF2 - FM-2 Integridade"),
        (12, "10QF2 - FM-2 Tensão"),
        (13, "10QF3 - FM-3 Integridade"),
        (14, "10QF3 - FM-3 Tensão"),
        (15, "11QF1 - FM-9 Integridade"),
        (16, "11QF1 - FM-9 Tensão"),
        (17, "Circuito Iluminação Interna"),
        (18, "Circuito Iluminação Externa"),
        (19, "Circuito Iluminação de Emergência"),
        (20, "Interruptores Integridade"),
        (21, "Limpeza / Organização"),
        (22, "Aterramento Integridade"),
    ]
    add_section(modelo, "Casa de Bombas Revest Coat", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_tiberina():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas Tiberina SP04",
        codigo="CL-CBTIB-083",
        descricao="Checklist diário de manutenção da Casa de Bombas Tiberina.",
        area_padrao="SP04 - CASA DE BOMBAS TIBERINA",
    )
    principais = [
        (1, "CCM Integridade"),
        (2, "CCM Tensão"),
        (3, "CCM Corrente"),
        (4, "QF1 - Pump EP01A Integridade"),
        (5, "QF1 - Pump EP01A Tensão"),
        (6, "QF2 - Pump EP02 Integridade"),
        (7, "QF2 - Pump EP02 Tensão"),
        (8, "QF3 - Pump EP03 Integridade"),
        (9, "QF3 - Pump EP03 Tensão"),
        (10, "QF4 - Pump EP04 Integridade"),
        (11, "QF4 - Pump EP04 Tensão"),
        (12, "QF5 - Pump EP05 Integridade"),
        (13, "QF5 - Pump EP05 Tensão"),
        (14, "QF6 - Pump EP06 Integridade"),
        (15, "QF6 - Pump EP06 Tensão"),
        (16, "QF7 - Pump EP07 Integridade"),
        (17, "QF7 - Pump EP07 Tensão"),
        (18, "QF8 - Pump EP08 Integridade"),
        (19, "QF8 - Pump EP08 Tensão"),
        (20, "QF9 - Pump EP09 Integridade"),
        (21, "QF9 - Pump EP09 Tensão"),
        (22, "QF10 - Pump EP10 Integridade"),
        (23, "QF10 - Pump EP10 Tensão"),
        (24, "QF11 - Pump EP11 Integridade"),
        (25, "QF11 - Pump EP11 Tensão"),
        (26, "QF12 - Pump EP12 Integridade"),
        (27, "QF12 - Pump EP12 Tensão"),
        (28, "QF13 - Pump EP13 Integridade"),
        (29, "QF13 - Pump EP13 Tensão"),
        (30, "QF14 - Pump EP14 Integridade"),
        (31, "QF14 - Pump EP14 Tensão"),
        (32, "QF15 - Pump EP15 Integridade"),
        (33, "QF15 - Pump EP15 Tensão"),
        (34, "QF16 - Pump EP16 Integridade"),
        (35, "QF16 - Pump EP16 Tensão"),
        (36, "QF17 - Pump EP17 Integridade"),
        (37, "QF17 - Pump EP17 Tensão"),
        (38, "QF18 - Pump EP18 Integridade"),
        (39, "QF18 - Pump EP18 Tensão"),
        (40, "QF19 - Pump EP19 Integridade"),
        (41, "QF19 - Pump EP19 Tensão"),
        (42, "QF20 - Pump EP20 Integridade"),
        (43, "QF20 - Pump EP20 Tensão"),
        (44, "Circuito Iluminação Interna"),
        (45, "Aterramento Integridade"),
        (46, "Limpeza e Organização"),
    ]
    add_section(modelo, "Casa de Bombas Tiberina", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_pmc():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas PMC",
        codigo="CL-CBPMC-084",
        descricao="Checklist diário de manutenção da Casa de Bombas PMC.",
        area_padrao="SP01 - CASA DE BOMBAS PMC",
    )
    principais = [
        (1, "CCM-440V Integridade"),
        (2, "CCM-440V Tensão"),
        (3, "CCM-440V Corrente"),
        (4, "16QG1-FM17 Integridade"),
        (5, "16QG1-FM17 Tensão"),
        (6, "18QG1-FM18 Integridade"),
        (7, "18QG1-FM18 Tensão"),
        (8, "20QG1-FM22 Integridade"),
        (9, "20QG1-FM22 Tensão"),
        (10, "22QG1-FM23 Integridade"),
        (11, "22QG1-FM23 Tensão"),
        (12, "24QG1-FM14 Integridade"),
        (13, "24QG1-FM14 Tensão"),
        (14, "26QG1-FM15 Integridade"),
        (15, "26QG1-FM15 Tensão"),
        (16, "28QG1-FM16 Integridade"),
        (17, "28QG1-FM16 Tensão"),
        (18, "30QG1-FM19 Integridade"),
        (19, "30QG1-FM19 Tensão"),
        (20, "32QG1-FM20 Integridade"),
        (21, "32QG1-FM20 Tensão"),
        (22, "34QG1-FM21 Integridade"),
        (23, "34QG1-FM21 Tensão"),
        (24, "39QG1-FM27 Integridade"),
        (25, "39QG1-FM27 Tensão"),
        (26, "Circuito Iluminação Interna"),
        (27, "Circuito Iluminação Emergência"),
        (28, "Circuito Tomadas Integridade / Tensão"),
        (29, "Aterramento Integridade"),
        (30, "Portas de acesso"),
        (31, "Extintores carregados"),
    ]
    add_section(modelo, "Casa de Bombas PMC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_mmh():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas MMH",
        codigo="CL-CBMMH-085",
        descricao="Checklist diário de manutenção da Casa de Bombas MMH.",
        area_padrao="SP03 - CASA DE BOMBAS MMH",
    )
    principais = [
        (1, "03MCC01 Integridade"),
        (2, "03MCC01 Tensão"),
        (3, "7Q1 - Chiller-1 Integridade"),
        (4, "7Q1 - Chiller-1 Tensão"),
        (5, "8Q1 - Chiller-2 Integridade"),
        (6, "8Q1 - Chiller-2 Tensão"),
        (7, "9Q1 - Chiller-3 Integridade"),
        (8, "9Q1 - Chiller-3 Tensão"),
        (9, "10Q1 - Chiller-4 Integridade"),
        (10, "10Q1 - Chiller-4 Tensão"),
        (11, "11Q1 - Pump HVAC-1 Integridade"),
        (12, "11Q1 - Pump HVAC-1 Tensão"),
        (13, "11Q2 - Pump HVAC-2 Integridade"),
        (14, "11Q2 - Pump HVAC-2 Tensão"),
        (15, "11Q3 - Pump HVAC-3 Integridade"),
        (16, "11Q3 - Pump HVAC-3 Tensão"),
        (17, "11Q4 - Pump HVAC-4 Integridade"),
        (18, "11Q4 - Pump HVAC-4 Tensão"),
        (19, "11Q5 - Pump HVAC-5 Integridade"),
        (20, "11Q5 - Pump HVAC-5 Tensão"),
        (21, "12Q1 - Pump Syst EP01A Integridade"),
        (22, "12Q1 - Pump Syst EP01A Tensão"),
        (23, "12Q2 - Pump Syst EP01B Integridade"),
        (24, "12Q2 - Pump Syst EP01B Tensão"),
        (25, "12Q3 - Pump Syst EP01C Integridade"),
        (26, "12Q3 - Pump Syst EP01C Tensão"),
        (27, "12Q4 - Pump Syst EP01D Integridade"),
        (28, "12Q4 - Pump Syst EP01D Tensão"),
        (29, "Pump Syst EP01E Integridade"),
        (30, "Pump Syst EP01E Tensão"),
        (31, "Circuito de Iluminação Interna"),
        (32, "Tomadas Integridade / Tensão"),
        (33, "Aterramento Integridade"),
        (34, "Portas de acesso"),
    ]
    add_section(modelo, "Casa de Bombas MMH", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_denso():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas Denso",
        codigo="CL-CBDEN-086",
        descricao="Checklist diário de manutenção da Casa de Bombas Denso.",
        area_padrao="SP06 - CASA DE BOMBAS DENSO",
    )
    principais = [
        (1, "07MCC-PE Integridade"),
        (2, "07MCC-PE Tensão"),
        (3, "07MCC-PE Corrente"),
        (4, "QM1 - BP1 Integridade"),
        (5, "QM1 - BP1 Tensão"),
        (6, "QM2 - BP2 Integridade"),
        (7, "QM2 - BP2 Tensão"),
        (8, "QM3 - BP3 Integridade"),
        (9, "QM3 - BP3 Tensão"),
        (10, "QM4 - Bomba 4 BS1 Integridade"),
        (11, "QM4 - Bomba 4 BS1 Tensão"),
        (12, "QM5 - Bomba 5 Integridade"),
        (13, "QM5 - Bomba 5 Tensão"),
        (14, "Circuito Iluminação Interna"),
        (15, "Circuito Iluminação Externa"),
        (16, "Circuito Iluminação de Emergência"),
        (17, "Aterramento Integridade"),
        (18, "Tomadas Integridade e Tensão"),
        (19, "Limpeza e Organização"),
    ]
    add_section(modelo, "Casa de Bombas Denso", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


def seed_casa_bombas_fmm():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas FMM",
        codigo="CL-CBFMM-087",
        descricao="Checklist diário de manutenção da Casa de Bombas FMM.",
        area_padrao="SP09 - CASA DE BOMBAS FMM",
    )
    principais = [
        (1, "09MPC01-MCC Integridade"),
        (2, "09MPC01-MCC Tensão"),
        (3, "Q1 - Chiller-1 Integridade"),
        (4, "Q1 - Chiller-1 Tensão"),
        (5, "Q2 - Chiller-2 Integridade"),
        (6, "Q2 - Chiller-2 Tensão"),
        (7, "Q3 - Chiller-3 Integridade"),
        (8, "Q3 - Chiller-3 Tensão"),
        (9, "Q7 - Chiller-4 Integridade"),
        (10, "Q7 - Chiller-4 Tensão"),
        (11, "Q8 - Chiller-5 Integridade"),
        (12, "Q8 - Chiller-5 Tensão"),
        (13, "Q9 - Chiller-6 Integridade"),
        (14, "Q9 - Chiller-6 Tensão"),
        (15, "Bomba-EP01A Integridade"),
        (16, "Bomba-EP01A Tensão"),
        (17, "Bomba-EP01B Integridade"),
        (18, "Bomba-EP01B Tensão"),
        (19, "Bomba-EP01C Integridade"),
        (20, "Bomba-EP01C Tensão"),
        (21, "Bomba-EP02A Integridade"),
        (22, "Bomba-EP02A Tensão"),
        (23, "Bomba-EP02B Integridade"),
        (24, "Bomba-EP02B Tensão"),
        (25, "Bomba-EP03A Integridade"),
        (26, "Bomba-EP03A Tensão"),
        (27, "Bomba-EP03B Integridade"),
        (28, "Bomba-EP03B Tensão"),
        (29, "Bomba-EP03C Integridade"),
        (30, "Bomba-EP03C Tensão"),
        (31, "Bomba-EP03D Integridade"),
        (32, "Bomba-EP03D Tensão"),
        (33, "Bomba-EP03E Integridade"),
        (34, "Bomba-EP03E Tensão"),
        (35, "Bomba-EP03F Integridade"),
        (36, "Bomba-EP03F Tensão"),
        (37, "Bomba-EP03G Integridade"),
        (38, "Bomba-EP03G Tensão"),
        (39, "Circuito de Iluminação Interna"),
        (40, "Tomadas Integridade e Tensão"),
        (41, "Aterramento Integridade"),
        (42, "Portas de acesso"),
        (43, "Sistema de Ventilação"),
    ]
    add_section(modelo, "Casa de Bombas FMM", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")


if __name__ == "__main__":
    with app.app_context():
        seed_casa_bombas_adler()
        seed_casa_bombas_revest_coat()
        seed_casa_bombas_tiberina()
        seed_casa_bombas_pmc()
        seed_casa_bombas_mmh()
        seed_casa_bombas_denso()
        seed_casa_bombas_fmm()
        db.session.commit()
        print("\\nDécimo quinto lote cadastrado com sucesso.")
