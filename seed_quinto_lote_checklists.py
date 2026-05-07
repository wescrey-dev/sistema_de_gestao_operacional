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

    modelo = ChecklistModelo(nome=nome, codigo=codigo, descricao=descricao, area_padrao=area_padrao, ativo=True)
    db.session.add(modelo)
    db.session.flush()

    for ordem, (nome_campo, label_campo, tipo_campo, obrigatorio) in enumerate(COMMON_HEADER, start=1):
        db.session.add(ChecklistCampoCabecalho(checklist_modelo_id=modelo.id, nome_campo=nome_campo, label_campo=label_campo, tipo_campo=tipo_campo, obrigatorio=obrigatorio, ordem=ordem))
    return modelo

def add_item(secao, numero_item, descricao, ordem, usa_rst=True, usa_obs=True):
    db.session.add(ChecklistItemModelo(checklist_secao_id=secao.id, numero_item=str(numero_item) if numero_item is not None else "", descricao=descricao, tipo_resposta="padrao", usa_normal_anormal=True, usa_valores_rst=usa_rst, usa_observacao=usa_obs, usa_resolvido=False, ordem=ordem))

def add_section(modelo, titulo, ordem, itens, tipo_secao="itens", usa_rst=True, usa_obs=True):
    secao = ChecklistSecao(checklist_modelo_id=modelo.id, titulo=titulo, tipo_secao=tipo_secao, ordem=ordem)
    db.session.add(secao)
    db.session.flush()
    if tipo_secao == "observacoes_gerais":
        for i in range(1, itens + 1):
            db.session.add(ChecklistItemModelo(checklist_secao_id=secao.id, numero_item=str(i), descricao=f"Ocorrência {i}", tipo_resposta="observacao_geral", usa_normal_anormal=False, usa_valores_rst=False, usa_observacao=False, usa_resolvido=True, ordem=i))
        return
    for ordem_item, (numero_item, descricao) in enumerate(itens, start=1):
        add_item(secao, numero_item, descricao, ordem_item, usa_rst=usa_rst, usa_obs=usa_obs)

def seed_iluminacao_emergencia_pintura():
    modelo = get_or_create_model("Check List de Manutenção - Iluminação de Emergência Pintura", "CL-ILP-022", "Checklist de manutenção da iluminação de emergência do prédio Pintura.", "MP - Iluminação de Emergência Pintura")
    principais = [
        (1, "PN-LP-1 Col.CZ-110 Integridade"), (2, "PN-LP-1 Col.CZ-110 Tensão"), (3, "Funcionamento da Iluminação Emerg. 1"),
        (4, "PN-LP-2 Col.CR-110 Integridade"), (5, "PN-LP-2 Col.CR-110 Tensão"), (6, "Funcionamento da Iluminação Emerg. 2"),
        (7, "PN-LP-3 Col.CL-110 Integridade"), (8, "PN-LP-3 Col.CL-110 Tensão"), (9, "Funcionamento da Iluminação Emerg. 3"),
        (10, "PN-LP-4 Col.CB-110 Integridade"), (11, "PN-LP-4 Col.CB-110 Tensão"), (12, "Funcionamento da Iluminação Emerg. 4"),
        (13, "PN-LP-5 Col.BY-108 Integridade"), (14, "PN-LP-5 Col.BY-108 Tensão"), (15, "Funcionamento da Iluminação Emerg. 5"),
        (16, "PN-LP-6 Col.CP-112 Integridade"), (17, "PN-LP-6 Col.CP-112 Tensão"), (18, "Funcionamento da Iluminação Emerg. 6"),
    ]
    add_section(modelo, "Prédio Pintura", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_cdc_iluminacao_interna_externa():
    modelo = get_or_create_model("Check List de Manutenção - CDC Iluminação Interna / Externa", "CL-CDI-023", "Checklist de manutenção da iluminação interna e externa do prédio CDC.", "MP - CDC Iluminação Interna / Externa")
    principais = [
        (1, "LP1 - Integridade"), (2, "LP1 - Tensão"), (3, "LP1 - Corrente"), (4, "RP1 - Integridade"), (5, "RP1 - Tensão"), (6, "RP1 - Corrente"),
        (7, "RP2 - Integridade"), (8, "RP2 - Tensão"), (9, "RP2 - Corrente"), (10, "LP2 - Integridade"), (11, "LP2 - Tensão"), (12, "LP2 - Corrente"),
        (13, "QXLP3 - Integridade"), (14, "QXLP3 - Tensão"), (15, "QXLP3 - Corrente"), (16, "LP3 - Integridade"), (17, "LP3 - Tensão"), (18, "LP3 - Corrente"),
        (19, "RP3 - Integridade"), (20, "RP3 - Tensão"), (21, "RP3 - Corrente"), (22, "LP4 - Integridade"), (23, "LP4 - Tensão"), (24, "LP4 - Corrente"),
        (25, "RP5 - Integridade"), (26, "RP5 - Tensão"), (27, "RP5 - Corrente"), (28, "LP5 - Integridade"), (29, "LP5 - Tensão"), (30, "LP5 - Corrente"),
        (31, "RP4 - Integridade"), (32, "RP4 - Tensão"), (33, "RP4 - Corrente"), (34, "QXLP1 - Integridade"), (35, "QXLP1 - Tensão"), (36, "QXLP1 - Corrente"),
        (37, "QXLP2 - Integridade"), (38, "QXLP2 - Tensão"), (39, "QXLP2 - Corrente"),
    ]
    add_section(modelo, "Prédio CDC", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 10, tipo_secao="observacoes_gerais")

def seed_iluminacao_emergencia_montagem():
    modelo = get_or_create_model("Check List de Manutenção - Iluminação de Emergência Montagem", "CL-ILM-021", "Checklist de manutenção da iluminação de emergência do prédio Montagem.", "MP - Iluminação de Emergência Montagem")
    principais = [
        (1, "PN-LP-1 Col.DB-144 Integridade"), (2, "PN-LP-1 Col.DB-144 Tensão"), (3, "Funcionamento da Iluminação Emerg. 1"),
        (4, "PN-LP-2 Col.DN-144 Integridade"), (5, "PN-LP-2 Col.DN-144 Tensão"), (6, "Funcionamento da Iluminação Emerg. 2"),
        (7, "PN-LP-3 Col.DV-146 Integridade"), (8, "PN-LP-3 Col.DV-146 Tensão"), (9, "Funcionamento da Iluminação Emerg. 3"),
        (10, "PN-LP-4 Col.DD-134 Integridade"), (11, "PN-LP-4 Col.DD-134 Tensão"), (12, "Funcionamento da Iluminação Emerg. 4"),
        (13, "PN-LP-5 Col.DN-134 Integridade"), (14, "PN-LP-5 Col.DN-134 Tensão"), (15, "Funcionamento da Iluminação Emerg. 5"),
        (16, "PN-LP-6 Col.DR-134 Integridade"), (17, "PN-LP-6 Col.DR-134 Tensão"), (18, "Funcionamento da Iluminação Emerg. 6"),
        (19, "PN-LP-7 Col.DL-130 Integridade"), (20, "PN-LP-7 Col.DL-130 Tensão"), (21, "Funcionamento da Iluminação Emerg. 7"),
    ]
    add_section(modelo, "Prédio Montagem", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_iluminacao_emergencia_pintura()
        seed_cdc_iluminacao_interna_externa()
        seed_iluminacao_emergencia_montagem()
        db.session.commit()
        print("\nQuinto lote cadastrado com sucesso.")
