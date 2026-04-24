
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "seguranca-secret-key")

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD", "SUA_SENHA_AQUI"))
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DB", "sistema_seguranca")

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# listas
OPAI_CLASSES = ["CC - Conscientizado o colaborador","CCI - Corrigida a condição insegura","CM - Comunicado ao supervisor","IS - Interrompido o serviço","SC - Solicitado a correção da condição insegura"]
OPAI_CRITICIDADES = ["Desprezível","Moderado","Crítico","Não aplicável"]
OPAI_SUBCLASSES = ["Adequados e não seguidos","Inadequados","Não existente","Impróprios para o serviço","Usados incorretamente","Em condições inseguras","Local sujo","Local desorganizado","Local com vazamentos / poluição ambiental","Ingerir contaminantes","Postura inadequada","Esforço inadequado","Risco de choque elétrico","Inalar contaminantes","Absorver contaminantes","Ficar preso entre","Risco de queda","Risco de queimadura","Ajustando o EPI","Adequando ao serviço","Bater contra / ser atingido","Mudança de posição","Parando o serviço"]
OPAI_CATEGORIAS = ["Pés e pernas","Reação das pessoas","Posição das pessoas","Ordem, limpeza e organização","Ferramenta / equipamento","Procedimentos","EPI","Ouvidos","Mãos e braços","Tronco","Cabeça","Sistema respiratório","Olhos e faces"]
AP_AREAS = ["Equipamento obstruído","Saída de emergência obstruída","Piso desnivelado / escorregadio"]
AP_EQUIPAMENTOS = ["Falta de proteção na máquina","Botoeira / sensor danificados","Partes móveis / cortantes desprotegidas"]
AP_PROCEDIMENTOS = ["Inexistentes","Existentes e não seguidos","Não contempla todos os riscos","Não execução / inadequado de LIBRA"]
AP_FERRAMENTAS = ["Falha no isolamento elétrico","Ferramenta com avaria / improvisada","Ferramentas com excesso de sujeira","Transporte inadequado"]
AP_COMPORTAMENTOS = ["Uso indevido de celular","Comportamento inseguro","Uso incorreto de ferramentas","APR e PT preenchidos incorretamente","Ausência / mau uso do EPI","Armazenamento inadequado de resíduos","Crenças de segurança não seguidas","Não praticado direção segura","Postura inadequada"]
AP_OUTROS = ["Local desorganizado / sujo","Estrutura sem contenção de vazamento","Risco de poluição ambiental","Equipamento / máquina sem manutenção","Instalação com rachadura","Checklist não preenchido","Instalação com infiltração","Extintores sem inspeção","Atividade toda sinalizada"]
AP_ACOES = ["Paralisação da atividade","Notificação do superior imediato ou cipeiro / representante","Orientação da equipe ou colega de trabalho","Sinalização e/ou isolamento da área","Acionamento da brigada de emergência","Evacuação da área","Adoção de medidas de contenção","Outro"]
AP_CRITICIDADES = ["Desprezível","Moderado","Crítico"]
IPS_CRITICIDADES = ["Leve","Moderado","Crítico"]
IPS_STATUS = ["OK","Pendente"]
IPS_ELEMENTOS = ["Engrenagens mecânicas","Carcaça","Manopla","Pintura","Lâminas","Componentes","Botões e parafusos","Mangueiras e mangotes","Manômetros e mostradores","Tampas e hastes","Suportes e travas","Luzes e faróis","Cabo","Escovas e fibras","Limpeza","Estado geral","Circuitos elétricos","Check-list de pré-uso"]

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(50), nullable=False, default="usuario")
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class OPAI(db.Model):
    __tablename__ = "opai"
    id = db.Column(db.Integer, primary_key=True)
    local_observado = db.Column(db.String(255), nullable=False)
    data_opai = db.Column(db.Date, nullable=False)
    nome_ut = db.Column(db.String(150))
    numero_ut = db.Column(db.String(100))
    auditor = db.Column(db.String(150), nullable=False)
    re = db.Column(db.String(50))
    equipe_observada = db.Column(db.String(150))
    numero_pessoas = db.Column(db.Integer)
    status_opai = db.Column(db.String(50))
    comportamentos_positivos = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    desvios = db.relationship("OPAIDesvio", backref="opai", cascade="all, delete-orphan", lazy=True)

class OPAIDesvio(db.Model):
    __tablename__ = "opai_desvios"
    id = db.Column(db.Integer, primary_key=True)
    opai_id = db.Column(db.Integer, db.ForeignKey("opai.id", ondelete="CASCADE"), nullable=False)
    sequencia = db.Column(db.Integer)
    descricao = db.Column(db.Text, nullable=False)
    categoria = db.Column(db.String(150))
    subclasse = db.Column(db.String(150))
    classe = db.Column(db.String(150))
    criticidade = db.Column(db.String(50))
    acao_imediata = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class AP(db.Model):
    __tablename__ = "ap"
    id = db.Column(db.Integer, primary_key=True)
    numero_nome_ut = db.Column(db.String(150), nullable=False)
    data_ocorrencia = db.Column(db.Date, nullable=False)
    hora_ocorrencia = db.Column(db.Time)
    emitido_por = db.Column(db.String(150), nullable=False)
    recebido_por = db.Column(db.String(150))
    descricao_local = db.Column(db.Text)
    criticidade = db.Column(db.String(50), nullable=False)
    desvio_tratado = db.Column(db.String(10))
    outros_texto = db.Column(db.Text)
    acao_outro_texto = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itens = db.relationship("APItem", backref="ap", cascade="all, delete-orphan", lazy=True)

class APItem(db.Model):
    __tablename__ = "ap_itens"
    id = db.Column(db.Integer, primary_key=True)
    ap_id = db.Column(db.Integer, db.ForeignKey("ap.id", ondelete="CASCADE"), nullable=False)
    tipo_item = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class IPS(db.Model):
    __tablename__ = "ips"
    id = db.Column(db.Integer, primary_key=True)
    data_inspecao = db.Column(db.Date, nullable=False)
    re = db.Column(db.String(50))
    inspetor = db.Column(db.String(150), nullable=False)
    nome_ut = db.Column(db.String(150))
    numero_ut = db.Column(db.String(100))
    identificacao_tag = db.Column(db.String(150), nullable=False)
    funcao = db.Column(db.String(100))
    cipeiro = db.Column(db.String(150))
    funcao_cipeiro = db.Column(db.String(100))
    quantidade_desvios = db.Column(db.Integer, nullable=False, default=0)
    quantidade_acoes_propostas = db.Column(db.Integer, nullable=False, default=0)
    quantidade_acoes_concluidas = db.Column(db.Integer, nullable=False, default=0)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itens = db.relationship("IPSItem", backref="ips", cascade="all, delete-orphan", lazy=True)

class IPSItem(db.Model):
    __tablename__ = "ips_itens"
    id = db.Column(db.Integer, primary_key=True)
    ips_id = db.Column(db.Integer, db.ForeignKey("ips.id", ondelete="CASCADE"), nullable=False)
    elemento = db.Column(db.String(150), nullable=False)
    desvio = db.Column(db.Enum("Sim","Não"), nullable=False, default="Não")
    criticidade = db.Column(db.String(50))
    acao_corretiva = db.Column(db.String(255))
    prazo = db.Column(db.Date)
    status_item = db.Column(db.String(50))
    responsavel = db.Column(db.String(150))
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# checklist
class ChecklistModelo(db.Model):
    __tablename__ = "checklist_modelos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(50))
    descricao = db.Column(db.Text)
    area_padrao = db.Column(db.String(150))
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    campos_cabecalho = db.relationship("ChecklistCampoCabecalho", backref="modelo", cascade="all, delete-orphan", lazy=True)
    secoes = db.relationship("ChecklistSecao", backref="modelo", cascade="all, delete-orphan", lazy=True)


class ChecklistCampoCabecalho(db.Model):
    __tablename__ = "checklist_campos_cabecalho"

    id = db.Column(db.Integer, primary_key=True)
    checklist_modelo_id = db.Column(db.Integer, db.ForeignKey("checklist_modelos.id", ondelete="CASCADE"), nullable=False)
    nome_campo = db.Column(db.String(100), nullable=False)
    label_campo = db.Column(db.String(150), nullable=False)
    tipo_campo = db.Column(db.String(50), nullable=False)
    obrigatorio = db.Column(db.Boolean, nullable=False, default=False)
    ordem = db.Column(db.Integer, nullable=False, default=0)


class ChecklistSecao(db.Model):
    __tablename__ = "checklist_secoes"

    id = db.Column(db.Integer, primary_key=True)
    checklist_modelo_id = db.Column(db.Integer, db.ForeignKey("checklist_modelos.id", ondelete="CASCADE"), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    tipo_secao = db.Column(db.String(50), nullable=False, default="itens")
    ordem = db.Column(db.Integer, nullable=False, default=0)

    itens = db.relationship("ChecklistItemModelo", backref="secao", cascade="all, delete-orphan", lazy=True)


class ChecklistItemModelo(db.Model):
    __tablename__ = "checklist_itens_modelo"

    id = db.Column(db.Integer, primary_key=True)
    checklist_secao_id = db.Column(db.Integer, db.ForeignKey("checklist_secoes.id", ondelete="CASCADE"), nullable=False)
    numero_item = db.Column(db.String(20))
    descricao = db.Column(db.String(255), nullable=False)
    tipo_resposta = db.Column(db.String(50), nullable=False)
    usa_normal_anormal = db.Column(db.Boolean, nullable=False, default=False)
    usa_valores_rst = db.Column(db.Boolean, nullable=False, default=False)
    usa_observacao = db.Column(db.Boolean, nullable=False, default=False)
    usa_resolvido = db.Column(db.Boolean, nullable=False, default=False)
    ordem = db.Column(db.Integer, nullable=False, default=0)

def to_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None

def to_time(value):
    return datetime.strptime(value, "%H:%M").time() if value else None

def selected_list(name):
    return request.form.getlist(name)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Faça login para acessar o sistema.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def perfil_required(*perfis):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if "usuario_id" not in session:
                flash("Faça login para acessar o sistema.", "warning")
                return redirect(url_for("login"))

            if session.get("usuario_perfil") not in perfis:
                flash("Você não tem permissão para acessar esta área.", "danger")
                return redirect(url_for("registros"))

            return f(*args, **kwargs)
        return decorated
    return decorator

@app.context_processor
def inject_globals():
    return {"usuario_logado": "usuario_id" in session, "usuario_nome": session.get("usuario_nome")}

@app.route("/register", methods=["GET", "POST"])
def register():
    total_usuarios = Usuario.query.count()

    # Se já existe usuário no sistema, só admin pode cadastrar outro
    if total_usuarios > 0:
        if "usuario_id" not in session:
            flash("Somente administradores podem cadastrar novos usuários.", "danger")
            return redirect(url_for("login"))

        if session.get("usuario_perfil") != "admin":
            flash("Somente administradores podem cadastrar novos usuários.", "danger")
            return redirect(url_for("registros"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")

        if not nome or not email or not senha:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("register"))

        if senha != confirmar:
            flash("As senhas não conferem.", "danger")
            return redirect(url_for("register"))

        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            flash("Já existe um usuário com este email.", "danger")
            return redirect(url_for("register"))

        perfil_inicial = "admin" if total_usuarios == 0 else "usuario"

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha),
            perfil=perfil_inicial,
            ativo=True
        )

        db.session.add(usuario)
        db.session.commit()

        flash("Usuário criado com sucesso.", "success")

        if total_usuarios == 0:
            return redirect(url_for("login"))

        return redirect(url_for("usuarios"))

    return render_template("register.html")

@app.route("/usuarios")
@perfil_required("admin")
def usuarios():
    lista_usuarios = Usuario.query.order_by(Usuario.nome.asc()).all()
    return render_template("usuarios.html", usuarios=lista_usuarios)


@app.route("/usuarios/<int:usuario_id>/perfil", methods=["POST"])
@perfil_required("admin")
def alterar_perfil(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    novo_perfil = request.form.get("perfil")

    if novo_perfil not in ["admin", "supervisor", "usuario"]:
        flash("Perfil inválido.", "danger")
        return redirect(url_for("usuarios"))

    # evita remover o próprio admin sem querer
    if usuario.id == session.get("usuario_id") and novo_perfil != "admin":
        flash("Você não pode remover seu próprio perfil de admin.", "danger")
        return redirect(url_for("usuarios"))

    usuario.perfil = novo_perfil
    db.session.commit()

    flash("Perfil atualizado com sucesso.", "success")
    return redirect(url_for("usuarios"))


@app.route("/usuarios/<int:usuario_id>/toggle", methods=["POST"])
@perfil_required("admin")
def toggle_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)

    if usuario.id == session.get("usuario_id"):
        flash("Você não pode desativar seu próprio usuário.", "danger")
        return redirect(url_for("usuarios"))

    usuario.ativo = not usuario.ativo
    db.session.commit()

    flash("Status do usuário atualizado com sucesso.", "success")
    return redirect(url_for("usuarios"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario_id" in session:
        perfil = session.get("usuario_perfil")
        if perfil in ["admin", "supervisor"]:
            return redirect(url_for("index"))
        return redirect(url_for("registros"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if usuario and check_password_hash(usuario.senha_hash, senha):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_perfil"] = usuario.perfil

            flash("Login realizado com sucesso.", "success")

            if usuario.perfil in ["admin", "supervisor"]:
                return redirect(url_for("index"))
            else:
                return redirect(url_for("registros"))

        flash("Email ou senha inválidos.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu do sistema.", "success")
    return redirect(url_for("login"))

@app.route("/")
@perfil_required("admin", "supervisor")
def index():
    total = OPAI.query.count() + AP.query.count() + IPS.query.count()
    opai = OPAI.query.count()
    ap = AP.query.count()
    ips = IPS.query.count()
    criticos = (
        OPAIDesvio.query.filter_by(criticidade="Crítico").count()
        + AP.query.filter_by(criticidade="Crítico").count()
        + IPSItem.query.filter_by(criticidade="Crítico").count()
    )

    registros = []
    for item in OPAI.query.order_by(OPAI.criado_em.desc()).limit(5).all():
        registros.append({
            "tipo": "OPAI",
            "id": item.id,
            "created_at": item.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            "titulo": item.local_observado
        })

    for item in AP.query.order_by(AP.criado_em.desc()).limit(5).all():
        registros.append({
            "tipo": "AP",
            "id": item.id,
            "created_at": item.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            "titulo": item.numero_nome_ut
        })

    for item in IPS.query.order_by(IPS.criado_em.desc()).limit(5).all():
        registros.append({
            "tipo": "IPS",
            "id": item.id,
            "created_at": item.criado_em.strftime("%d/%m/%Y %H:%M:%S"),
            "titulo": item.identificacao_tag
        })

    registros = sorted(registros, key=lambda x: x["created_at"], reverse=True)[:5]

    return render_template(
        "index.html",
        total=total,
        opai=opai,
        ap=ap,
        ips=ips,
        criticos=criticos,
        registros=registros
    )

@app.route("/registros")
@login_required
def registros():
    busca = request.args.get("busca", "").strip()
    tipo = request.args.get("tipo", "").strip()
    criticidade = request.args.get("criticidade", "").strip()
    usuario_id = request.args.get("usuario_id", "").strip()
    data_inicio = request.args.get("data_inicio", "").strip()
    data_fim = request.args.get("data_fim", "").strip()

    opais = OPAI.query
    aps = AP.query
    ips_list = IPS.query

    if usuario_id:
        try:
            usuario_id_int = int(usuario_id)
            opais = opais.filter(OPAI.usuario_id == usuario_id_int)
            aps = aps.filter(AP.usuario_id == usuario_id_int)
            ips_list = ips_list.filter(IPS.usuario_id == usuario_id_int)
        except ValueError:
            pass

    if data_inicio:
        inicio = to_date(data_inicio)
        if inicio:
            opais = opais.filter(OPAI.criado_em >= datetime.combine(inicio, datetime.min.time()))
            aps = aps.filter(AP.criado_em >= datetime.combine(inicio, datetime.min.time()))
            ips_list = ips_list.filter(IPS.criado_em >= datetime.combine(inicio, datetime.min.time()))

    if data_fim:
        fim = to_date(data_fim)
        if fim:
            opais = opais.filter(OPAI.criado_em <= datetime.combine(fim, datetime.max.time()))
            aps = aps.filter(AP.criado_em <= datetime.combine(fim, datetime.max.time()))
            ips_list = ips_list.filter(IPS.criado_em <= datetime.combine(fim, datetime.max.time()))

    if busca:
        termo = f"%{busca}%"
        opais = opais.filter(
            db.or_(
                OPAI.local_observado.ilike(termo),
                OPAI.auditor.ilike(termo),
                OPAI.equipe_observada.ilike(termo),
                OPAI.nome_ut.ilike(termo),
                OPAI.numero_ut.ilike(termo),
            )
        )
        aps = aps.filter(
            db.or_(
                AP.numero_nome_ut.ilike(termo),
                AP.emitido_por.ilike(termo),
                AP.recebido_por.ilike(termo),
                AP.descricao_local.ilike(termo),
            )
        )
        ips_list = ips_list.filter(
            db.or_(
                IPS.identificacao_tag.ilike(termo),
                IPS.inspetor.ilike(termo),
                IPS.nome_ut.ilike(termo),
                IPS.numero_ut.ilike(termo),
                IPS.funcao.ilike(termo),
            )
        )

    opais = opais.order_by(OPAI.criado_em.desc()).all()
    aps = aps.order_by(AP.criado_em.desc()).all()
    ips_list = ips_list.order_by(IPS.criado_em.desc()).all()

    def criticidade_opai(opai):
        if not opai.desvios:
            return "Não informada"
        prioridades = {"Crítico": 3, "Moderado": 2, "Desprezível": 1, "Não aplicável": 0}
        maior = max(opai.desvios, key=lambda d: prioridades.get(d.criticidade, -1))
        return maior.criticidade or "Não informada"

    def criticidade_ips(ips):
        if not ips.itens:
            return "Não informada"
        prioridades = {"Crítico": 3, "Moderado": 2, "Leve": 1}
        maior = max(ips.itens, key=lambda i: prioridades.get(i.criticidade, -1))
        return maior.criticidade or "Não informada"

    if criticidade:
        if tipo in ["", "opai"]:
            opais = [r for r in opais if criticidade_opai(r) == criticidade]
        if tipo in ["", "ap"]:
            aps = [r for r in aps if (r.criticidade or "Não informada") == criticidade]
        if tipo in ["", "ips"]:
            ips_list = [r for r in ips_list if criticidade_ips(r) == criticidade]

    if tipo == "opai":
        aps = []
        ips_list = []
    elif tipo == "ap":
        opais = []
        ips_list = []
    elif tipo == "ips":
        opais = []
        aps = []

    lista_usuarios = Usuario.query.order_by(Usuario.nome.asc()).all()

    return render_template(
        "records.html",
        opais=opais,
        aps=aps,
        ips_list=ips_list,
        criticidade_opai=criticidade_opai,
        criticidade_ips=criticidade_ips,
        lista_usuarios=lista_usuarios,
        filtros={
            "busca": busca,
            "tipo": tipo,
            "criticidade": criticidade,
            "usuario_id": usuario_id,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
        }
    )

@app.route("/opai", methods=["GET","POST"])
@login_required
def opai():
    if request.method == "POST":
        registro = OPAI(local_observado=request.form.get("local_observado",""), data_opai=to_date(request.form.get("data")), nome_ut=request.form.get("nome_ut",""), numero_ut=request.form.get("numero_ut",""), auditor=request.form.get("auditor",""), re=request.form.get("re",""), equipe_observada=request.form.get("equipe_observada",""), numero_pessoas=int(request.form.get("numero_pessoas")) if request.form.get("numero_pessoas") else None, status_opai=request.form.get("status_opai",""), comportamentos_positivos=request.form.get("comportamentos_positivos",""))
        seqs = request.form.getlist("desvio_seq[]"); descricoes = request.form.getlist("desvio_descricao[]"); categorias = request.form.getlist("desvio_categoria[]"); subclasses = request.form.getlist("desvio_subclasse[]"); classes = request.form.getlist("desvio_classe[]"); criticidades = request.form.getlist("desvio_criticidade[]"); acoes = request.form.getlist("desvio_acao[]")
        for i in range(len(descricoes)):
            if descricoes[i].strip():
                registro.desvios.append(OPAIDesvio(sequencia=int(seqs[i]) if seqs[i].isdigit() else i+1, descricao=descricoes[i], categoria=categorias[i], subclasse=subclasses[i], classe=classes[i], criticidade=criticidades[i], acao_imediata=acoes[i]))
        db.session.add(registro); db.session.commit(); flash("OPAI salva com sucesso.", "success"); return redirect(url_for("registros"))
    return render_template("form_opai.html", classes=OPAI_CLASSES, criticidades=OPAI_CRITICIDADES, subclasses=OPAI_SUBCLASSES, categorias=OPAI_CATEGORIAS)

@app.route("/ap", methods=["GET","POST"])
@login_required
def ap():
    if request.method == "POST":
        registro = AP(numero_nome_ut=request.form.get("numero_nome_ut",""), data_ocorrencia=to_date(request.form.get("data_ocorrencia")), hora_ocorrencia=to_time(request.form.get("hora_ocorrencia")), emitido_por=request.form.get("emitido_por",""), recebido_por=request.form.get("recebido_por",""), descricao_local=request.form.get("descricao_local",""), criticidade=request.form.get("criticidade",""), desvio_tratado=request.form.get("desvio_tratado",""), outros_texto=request.form.get("outros_texto",""), acao_outro_texto=request.form.get("acao_outro_texto",""))
        grupos = {"area": selected_list("areas"), "equipamento": selected_list("equipamentos"), "procedimento": selected_list("procedimentos"), "ferramenta": selected_list("ferramentas"), "comportamento": selected_list("comportamentos"), "outro": selected_list("outros_marcados"), "acao_imediata": selected_list("acoes_imediatas")}
        for tipo_item, valores in grupos.items():
            for valor in valores:
                registro.itens.append(APItem(tipo_item=tipo_item, valor=valor))
        db.session.add(registro); db.session.commit(); flash("Alerta preventivo salvo com sucesso.", "success"); return redirect(url_for("registros"))
    return render_template("form_ap.html", areas=AP_AREAS, equipamentos=AP_EQUIPAMENTOS, procedimentos=AP_PROCEDIMENTOS, ferramentas=AP_FERRAMENTAS, comportamentos=AP_COMPORTAMENTOS, outros=AP_OUTROS, acoes=AP_ACOES, criticidades=AP_CRITICIDADES)

@app.route("/ips", methods=["GET","POST"])
@login_required
def ips():
    if request.method == "POST":
        registro = IPS(data_inspecao=to_date(request.form.get("data")), re=request.form.get("re",""), inspetor=request.form.get("inspetor",""), nome_ut=request.form.get("nome_ut",""), numero_ut=request.form.get("numero_ut",""), identificacao_tag=request.form.get("identificacao_tag",""), funcao=request.form.get("funcao",""), cipeiro=request.form.get("cipeiro",""), funcao_cipeiro=request.form.get("funcao_cipeiro",""))
        elementos = request.form.getlist("item_elemento[]"); desvios = request.form.getlist("item_desvio[]"); criticidades = request.form.getlist("item_criticidade[]"); acoes = request.form.getlist("item_acao[]"); prazos = request.form.getlist("item_prazo[]"); status = request.form.getlist("item_status[]"); responsaveis = request.form.getlist("item_responsavel[]")
        qtd_desvios=qtd_acoes=qtd_concluidas=0
        for i in range(len(elementos)):
            desvio = desvios[i]; acao = acoes[i]; status_item = status[i]
            if desvio == "Sim": qtd_desvios += 1
            if acao.strip(): qtd_acoes += 1
            if status_item == "OK": qtd_concluidas += 1
            registro.itens.append(IPSItem(elemento=elementos[i], desvio=desvio, criticidade=criticidades[i], acao_corretiva=acao, prazo=to_date(prazos[i]) if prazos[i] else None, status_item=status_item, responsavel=responsaveis[i]))
        registro.quantidade_desvios=qtd_desvios; registro.quantidade_acoes_propostas=qtd_acoes; registro.quantidade_acoes_concluidas=qtd_concluidas
        db.session.add(registro); db.session.commit(); flash("IPS salva com sucesso.", "success"); return redirect(url_for("registros"))
    return render_template("form_ips.html", elementos=IPS_ELEMENTOS, criticidades=IPS_CRITICIDADES, status_options=IPS_STATUS)

# Rota do checklist
@app.route("/checklists")
@login_required
def checklist_modelos():
    modelos = ChecklistModelo.query.filter_by(ativo=True).order_by(ChecklistModelo.nome.asc()).all()
    return render_template("checklist_modelos.html", modelos=modelos)


@app.route("/checklists/<int:modelo_id>")
@login_required
def checklist_preencher(modelo_id):
    modelo = ChecklistModelo.query.get_or_404(modelo_id)

    campos_cabecalho = ChecklistCampoCabecalho.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistCampoCabecalho.ordem.asc()).all()

    secoes = ChecklistSecao.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistSecao.ordem.asc()).all()

    return render_template(
        "checklist_preencher.html",
        modelo=modelo,
        campos_cabecalho=campos_cabecalho,
        secoes=secoes
    )



@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status":"ok","database":"connected"}
    except Exception as e:
        return {"status":"error","message":str(e)}, 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
