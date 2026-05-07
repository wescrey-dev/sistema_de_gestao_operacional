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

def seed_restaurante_2_supplier_park():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Restaurante 2 Supplier Park",
        codigo="CL-RSP2-079",
        descricao="Checklist diário de manutenção do Refeitório 2 Supplier Park.",
        area_padrao="SP - REFEITÓRIO 2 SUPPLY PARK",
    )
    principais = [
        (1, "GPR2 Integridade"),
        (2, "GPR2 Tensão"),
        (3, "GPR2 Corrente"),
        (4, "GPR3 Integridade"),
        (5, "GPR3 Tensão"),
        (6, "GPR3 Corrente"),
        (7, "GPR1-B.Capacitores Integridade"),
        (8, "GPR1-B.Capacitores Tensão"),
        (9, "GPEM - Emergência Rest.1 Integridade"),
        (10, "GPEM - Emergência Rest.1 Tensão"),
        (11, "GPR1 - Restaurante Integridade"),
        (12, "GPR1 - Restaurante Tensão"),
        (13, "GPR1 - Restaurante Corrente"),
        (14, "Iluminação Interna"),
        (15, "Iluminação Emergência"),
        (16, "Eletrocalhas"),
        (17, "WC Masculino - Iluminação"),
        (18, "WC Masculino - Tomadas"),
        (19, "WC Masculino - Iluminação de Emergência"),
        (20, "WC Feminino - Iluminação"),
        (21, "WC Feminino - Tomadas"),
        (22, "WC Feminino - Iluminação de Emergência"),
        (23, "Iluminação Cozinha"),
        (24, "Climatização Funcionamento"),
        (25, "WC Masculino Externo - Iluminação"),
        (26, "QHUAC-1 Integridade"),
        (27, "QHUAC-1 Tensão"),
        (28, "QHUAC-1 Corrente"),
        (29, "QHUAC-2 Integridade"),
        (30, "QHUAC-2 Tensão"),
        (31, "QHUAC-2 Corrente"),
        (32, "Limpeza da sala elétrica / Organização"),
        (33, "Câmara Frigorífica"),
    ]
    add_section(modelo, "Refeitório 2 Supply Park", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_restaurante_1_supplier_park():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Restaurante 1 Supplier Park",
        codigo="CL-RSP1-078",
        descricao="Checklist diário de manutenção do Refeitório 1 Supplier Park.",
        area_padrao="SP - REFEITÓRIO 1 SUPPLY PARK",
    )
    principais = [
        (1, "GPR2 Integridade"),
        (2, "GPR2 Tensão"),
        (3, "GPR2 Corrente"),
        (4, "GPR3 Integridade"),
        (5, "GPR3 Tensão"),
        (6, "GPR3 Corrente"),
        (7, "GPR1-B.Capacitores Integridade"),
        (8, "GPR1-B.Capacitores Tensão"),
        (9, "GPEM - Emergência Rest.1 Integridade"),
        (10, "GPEM - Emergência Rest.1 Tensão"),
        (11, "GPR1 - Restaurante Integridade"),
        (12, "GPR1 - Restaurante Tensão"),
        (13, "GPR1 - Restaurante Corrente"),
        (14, "QHVAC Integridade"),
        (15, "QHVAC Tensão"),
        (16, "QHVAC Corrente"),
        (17, "QHVAC Casa de Bomba Integridade"),
        (18, "QHVAC Casa de Bomba Tensão"),
        (19, "QHVAC Casa de Bomba Corrente"),
        (20, "Circuito Iluminação Interna"),
        (21, "Circuito Iluminação Emergência"),
        (22, "Eletrocalhas"),
        (23, "WC Masculino - Iluminação"),
        (24, "WC Masculino - Tomadas"),
        (25, "WC Masculino - Iluminação de Emergência"),
        (26, "WC Feminino - Iluminação"),
        (27, "WC Feminino - Tomadas"),
        (28, "WC Feminino - Iluminação de Emergência"),
        (29, "Iluminação Cozinha"),
        (30, "Porta - Integridade"),
        (31, "Limpeza e Organização"),
        (32, "Câmara Frigorífica"),
    ]
    add_section(modelo, "Refeitório 1 Supply Park", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

def seed_medical_center_supplier_park():
    modelo = get_or_create_model(
        nome="Check List de Manutenção - Medical Center Supplier Park",
        codigo="CL-MCSP-080",
        descricao="Checklist diário de manutenção do Medical Center Supplier Park.",
        area_padrao="SP - MEDICAL CENTER SUPPLY PARK",
    )
    principais = [
        (1, "Painel-GPMC-1 380V Integridade"),
        (2, "Painel-GPMC-1 380V Tensão"),
        (3, "Painel-GPMC-1 380V Corrente"),
        (4, "WC-MASC. Tomadas Tensão"),
        (5, "WC-MASC. Interruptores"),
        (6, "WC-MASC. Circuito de Iluminação"),
        (7, "WC-FEM. Tomadas Tensão"),
        (8, "WC-FEM. Interruptores"),
        (9, "WC-FEM. Circuito de Iluminação"),
        (10, "Circuito de Iluminação Corredor"),
        (11, "Circuito de Tomadas Corredor"),
        (12, "Climatização Funcionamento"),
        (13, "Amb. PML - Circuito Iluminação Interna"),
        (14, "Amb. PML - Circuito de Tomadas"),
        (15, "Sala de Coletas - Circuito Iluminação"),
        (16, "Sala de Coletas - Circuito Tomadas"),
        (17, "Sala de Repouso - Circuito Iluminação"),
        (18, "Sala de Repouso - Circuito Tomadas"),
        (19, "Sala de Triagem - Circuito Iluminação"),
        (20, "Sala de Triagem - Circuito Tomadas"),
        (21, "Copa - Circuito de Iluminação"),
        (22, "Copa - Circuito de Tomadas"),
        (23, "Sala de ADM - Circuito Iluminação"),
        (24, "Sala de ADM - Circuito Tomadas"),
        (25, "Consultório Médico - Iluminação"),
        (26, "Consultório Médico - Tomadas Integridade e Tensão"),
        (27, "Iluminação Externa"),
    ]
    add_section(modelo, "Prédio Medical Center", 1, principais, usa_rst=True, usa_obs=True)
    add_section(modelo, "Observações gerais", 2, 8, tipo_secao="observacoes_gerais")

if __name__ == "__main__":
    with app.app_context():
        seed_restaurante_2_supplier_park()
        seed_restaurante_1_supplier_park()
        seed_medical_center_supplier_park()
        db.session.commit()
        print("\\nDécimo quarto lote cadastrado com sucesso.")
