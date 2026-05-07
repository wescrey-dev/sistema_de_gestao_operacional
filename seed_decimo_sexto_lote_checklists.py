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

def seed_chiller_restaurante_1():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Chiller Restaurante 1",
        codigo="CL-CHR1-088",
        descricao="Checklist diário de manutenção do chiller do Restaurante 1.",
        area_padrao="SP - CHILLER REST.1 - P4 SUPPLY PARK",
    )
    principais = [
        (1, "CHILLER 1 vem Q15 SE-22 Integridade"),
        (2, "CHILLER 1 Tensão"),
        (3, "CHILLER 2 vem Q16 SE-22 Integridade"),
        (4, "CHILLER 2 Tensão"),
    ]
    add_section(modelo, "Restaurante 01", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_chiller_restaurante_2():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Chiller Restaurante 2",
        codigo="CL-CHR2-089",
        descricao="Checklist diário de manutenção do chiller do Restaurante 2.",
        area_padrao="SP - CHILLER REST.2 - REVEST C. SUPPLY PARK",
    )
    principais = [
        (1, "CHILLER-1 vem Q7 SE-21 Integridade"),
        (2, "CHILLER-1 vem Q7 SE-21 Tensão"),
    ]
    add_section(modelo, "Restaurante 02", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_iluminacao_viaria_interna_main_plant():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Iluminação Viária Interna Main Plant",
        codigo="CL-IVIMP-090",
        descricao="Checklist diário de manutenção da iluminação viária interna da Main Plant.",
        area_padrao="MP - ILUMINAÇÃO VIÁRIA INTERNA MAIN PLANT",
    )
    principais = [
        (1, "Funil. RP-03 Coluna EF-102 Integridade"),
        (2, "Funil. RP-03 Coluna EF-102 Tensão"),
        (3, "Pintura Coluna CB-112"),
        (4, "RP-07 - Rua da SE Pintura 02 à SE P7 / Frente Pintura 01 / da P7 à PP"),
        (5, "RP-03 rua do Portão A3 da Prensas Integridade"),
        (6, "RP-03 rua da SE-Treinamento Tagueamento dos disjuntores"),
        (7, "RP-03 rua A e B do Galpão Sucata Tensão"),
        (8, "RP-03 rua da SE-Funilaria"),
        (9, "Circuito Q1 RP-03 rua ao lado da Funilaria"),
        (10, "Circuito Q2 RP-03 rua Heliponto ao Galpão Construcap"),
        (11, "Circuito Q3 Montagem RP6 Col.134 Integridade"),
        (12, "Montagem RP6 Col.134 Tensão"),
        (13, "Pintura 2 Coluna DD-110"),
        (14, "RP-02 - Rua da Montagem à Pensilina"),
        (15, "RP6 - vai da PS1 até PS3 Integridade"),
        (16, "RP6 - vai da PS1 a P2 Tagueamento dos disjuntores"),
        (17, "RP6 - toda a pista de teste do E.Center Tensão"),
        (18, "ETE-QLT056-02 Rua ETE / SE-0"),
        (19, "Prensas Coluna DW-76"),
        (20, "ETE-QUPS em frente a SE-ETE (LED)"),
        (21, "RP-01 - Rua da PP ao Heliponto Integridade"),
        (22, "RP-01 - Rua da PP ao Heliponto Tagueamento dos disjuntores"),
        (23, "RP-01 - Rua da PP ao Heliponto Tensão"),
        (24, "Ilha Ecol. PN Integridade"),
        (25, "Ilha Ecol. PN Tensão"),
        (26, "Da Pista A e B do E. Center à Balança P1"),
        (27, "Da Ilha Ecol. à PS1"),
        (28, "CDC-QXLP-1 Col.A-09 Integridade - Rua da SE-CDC à PS3"),
        (29, "CDC-QXLP-1 Col.A-09 Tensão - Rua da SE-CDC à PS3"),
        (30, "CDC-QXLP-2 Col.H-12 Integridade - Rua em frente ao CDC"),
        (31, "CDC-QXLP-1 Col.H-12 Tensão"),
        (32, "Postes Integridade"),
        (33, "Temporizadores Integridade"),
    ]
    add_section(modelo, "Iluminação Viária Interna Main Plant", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 10, tipo_secao="observacoes_gerais")

def seed_iluminacao_viaria_externa_main_plant():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Iluminação Viária Externa Main Plant",
        codigo="CL-IVEMP-091",
        descricao="Checklist diário de manutenção da iluminação viária externa da Main Plant.",
        area_padrao="MP - ILUMINAÇÃO VIÁRIA EXTERNA MAIN PLANT",
    )
    principais = [
        (1, "QS-P1 Port.1 Tensão - vai da convivência da PR01 à retorno da PR7"),
        (2, "Circuito de Iluminação Viária"),
        (3, "PN-Treinamento - rua da convivência PR01 à giradouro PP"),
        (4, "QS-P1 Port.1 Integridade - vai da convivência da PR01 à retorno da PR7"),
    ]
    add_section(modelo, "Iluminação Viária Externa Main Plant", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_iluminacao_viaria_supplier_park():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Iluminação Viária Supplier Park",
        codigo="CL-IVSP-092",
        descricao="Checklist diário de manutenção da iluminação viária do Supplier Park.",
        area_padrao="SP - ILUMIN. VIÁRIA SUPPLY PARK",
    )
    principais = [
        (1, "SE-22 PN-SRL-2 Integridade"),
        (2, "SE-22 PN-SRL-2 Tensão"),
        (3, "SE-22 SR1-2 C1 Brose / P.CDC Tensão"),
        (4, "SE-22 SR1-2 C2 Ambul. / PS3 Tensão"),
        (5, "SE-21 PN-SRL-1 Integridade"),
        (6, "SE-21 PN-SRL-1 Tensão"),
        (7, "SE-21 SRL1-C1 Denso / SE-21 Tensão"),
        (8, "SE-21 SRL1-C2 Adler / P5 Tensão"),
        (9, "SE-21 SRL1-C3 P5 / SE-22 Tensão"),
        (10, "SE-21 SRL1-C4 Port CMA / Revest Tensão"),
        (11, "Postes Integridade"),
        (12, "Temporizadores Integridade"),
        (13, "Postes Aterramento"),
    ]
    add_section(modelo, "Iluminação Viária Supply Park", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_casa_bombas_ete():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Casa de Bombas ETE",
        codigo="CL-CBETE-093",
        descricao="Checklist diário de manutenção da Central de Bombas ETE.",
        area_padrao="MP - CENTRAL DE BOMBAS ETE",
    )
    principais = [
        (1, "QCPS-440V Integridade"),
        (2, "QCPS-440V Tensão"),
        (3, "QCPS-440V Corrente"),
        (4, "PN-MB-01 CCM 440V Integridade"),
        (5, "PN-MB-01 CCM 440V Tensão"),
        (6, "PN-MB-01 CCM 440V Corrente"),
        (7, "PN-MB-02 CCM 440V Integridade"),
        (8, "PN-MB-02 CCM 440V Tensão"),
        (9, "PN-MB-02 CCM 440V Corrente"),
        (10, "QAP-1 440V Integridade"),
        (11, "QAP-1 440V Tensão"),
        (12, "PN-QAP-01 Corrente"),
        (13, "PN-Quadro de Distribuição Integridade"),
        (14, "PN-Quadro de Distribuição Tensão"),
        (15, "Portas de acesso"),
        (16, "Circuito de Iluminação Interna"),
        (17, "Circuito de iluminação de emergência"),
        (18, "Tomadas Integridade e Tensão"),
        (19, "Aterramento Integridade"),
    ]
    add_section(modelo, "Central de Bombas - ETE", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_chiller_restaurante_1()
        seed_chiller_restaurante_2()
        seed_iluminacao_viaria_interna_main_plant()
        seed_iluminacao_viaria_externa_main_plant()
        seed_iluminacao_viaria_supplier_park()
        seed_casa_bombas_ete()
        db.session.commit()
        print("\\nDécimo sexto lote cadastrado com sucesso.")
