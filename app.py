
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
_secret_key = os.getenv("SECRET_KEY")
if not _secret_key:
    print("AVISO: SECRET_KEY não configurada. Usando valor de desenvolvimento — configure SECRET_KEY antes de ir para produção.")
    _secret_key = "seguranca-secret-key-dev-apenas"
app.secret_key = _secret_key

DB_MODE = os.getenv("DB_MODE", "mysql").lower()

if DB_MODE == "sqlite":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banco_local.db"
elif os.getenv("MYSQL_URL"):
    # Railway expõe a connection string pronta em MYSQL_URL.
    # SQLAlchemy precisa do driver pymysql explícito no scheme.
    db_url = os.getenv("MYSQL_URL")
    if db_url.startswith("mysql://"):
        db_url = db_url.replace("mysql://", "mysql+pymysql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    # Aceita tanto o padrão local (.env com underscore) quanto o padrão
    # que o Railway usa nas variáveis do serviço MySQL (sem underscore).
    DB_USER = os.getenv("MYSQL_USER") or os.getenv("MYSQLUSER", "root")
    DB_PASSWORD = quote_plus(os.getenv("MYSQL_PASSWORD") or os.getenv("MYSQLPASSWORD", "SUA_SENHA_AQUI"))
    DB_HOST = os.getenv("MYSQL_HOST") or os.getenv("MYSQLHOST", "localhost")
    DB_PORT = os.getenv("MYSQL_PORT") or os.getenv("MYSQLPORT", "3306")
    DB_NAME = os.getenv("MYSQL_DB") or os.getenv("MYSQLDATABASE", "sistema_seguranca")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

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
MATERIAL_UNIDADES = ["UN","PC","KG","M","M²","M³","L","CX","RL","PAR","KIT","SC","GL"]
MATERIAL_STATUS = ["Pendente","Aprovado","Rejeitado","Cancelado"]

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
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    desvios = db.relationship("OPAIDesvio", backref="opai", cascade="all, delete-orphan", lazy=True)
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id])

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
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itens = db.relationship("APItem", backref="ap", cascade="all, delete-orphan", lazy=True)
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id])

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
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    itens = db.relationship("IPSItem", backref="ips", cascade="all, delete-orphan", lazy=True)
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id])

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

# materiais
class LevantamentoMaterial(db.Model):
    __tablename__ = "levantamentos_material"

    id = db.Column(db.Integer, primary_key=True)
    atividade = db.Column(db.String(255), nullable=False)
    numero_om = db.Column(db.String(100))
    solicitante = db.Column(db.String(150), nullable=False)
    observacao = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default="Pendente")
    observacao_analise = db.Column(db.Text)
    numero_reserva = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    analisado_por_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    analisado_em = db.Column(db.DateTime)

    itens = db.relationship(
        "LevantamentoMaterialItem",
        backref="levantamento",
        cascade="all, delete-orphan",
        lazy=True
    )
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id])
    analisado_por = db.relationship("Usuario", foreign_keys=[analisado_por_id])


class LevantamentoMaterialItem(db.Model):
    __tablename__ = "levantamentos_material_itens"

    id = db.Column(db.Integer, primary_key=True)
    levantamento_id = db.Column(
        db.Integer,
        db.ForeignKey("levantamentos_material.id", ondelete="CASCADE"),
        nullable=False
    )
    material = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Numeric(10, 2), nullable=False)
    unidade = db.Column(db.String(20), nullable=False)


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

@app.route("/teste-login")
def teste_login():
    return render_template("login.html")

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
        registro = OPAI(local_observado=request.form.get("local_observado",""), data_opai=to_date(request.form.get("data")), nome_ut=request.form.get("nome_ut",""), numero_ut=request.form.get("numero_ut",""), auditor=request.form.get("auditor",""), re=request.form.get("re",""), equipe_observada=request.form.get("equipe_observada",""), numero_pessoas=int(request.form.get("numero_pessoas")) if request.form.get("numero_pessoas") else None, status_opai=request.form.get("status_opai",""), comportamentos_positivos=request.form.get("comportamentos_positivos",""), usuario_id=session.get("usuario_id"))
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
        registro = AP(numero_nome_ut=request.form.get("numero_nome_ut",""), data_ocorrencia=to_date(request.form.get("data_ocorrencia")), hora_ocorrencia=to_time(request.form.get("hora_ocorrencia")), emitido_por=request.form.get("emitido_por",""), recebido_por=request.form.get("recebido_por",""), descricao_local=request.form.get("descricao_local",""), criticidade=request.form.get("criticidade",""), desvio_tratado=request.form.get("desvio_tratado",""), outros_texto=request.form.get("outros_texto",""), acao_outro_texto=request.form.get("acao_outro_texto",""), usuario_id=session.get("usuario_id"))
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
        registro = IPS(data_inspecao=to_date(request.form.get("data")), re=request.form.get("re",""), inspetor=request.form.get("inspetor",""), nome_ut=request.form.get("nome_ut",""), numero_ut=request.form.get("numero_ut",""), identificacao_tag=request.form.get("identificacao_tag",""), funcao=request.form.get("funcao",""), cipeiro=request.form.get("cipeiro",""), funcao_cipeiro=request.form.get("funcao_cipeiro",""), usuario_id=session.get("usuario_id"))
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

# Rotas de levantamento de materiais
@app.route("/materiais", methods=["GET", "POST"])
@login_required
def materiais():
    if request.method == "POST":
        atividade = request.form.get("atividade", "").strip()
        numero_om = request.form.get("numero_om", "").strip()
        solicitante = request.form.get("solicitante", "").strip()
        observacao = request.form.get("observacao", "").strip()

        materiais_lista = request.form.getlist("item_material[]")
        quantidades = request.form.getlist("item_quantidade[]")
        unidades = request.form.getlist("item_unidade[]")

        if not atividade or not solicitante:
            flash("Preencha a atividade/OM e o solicitante.", "danger")
            return redirect(url_for("materiais"))

        registro = LevantamentoMaterial(
            atividade=atividade,
            numero_om=numero_om,
            solicitante=solicitante,
            observacao=observacao,
            status="Pendente",
            usuario_id=session.get("usuario_id"),
        )

        tem_item_valido = False
        for i in range(len(materiais_lista)):
            material = materiais_lista[i].strip()
            quantidade_raw = quantidades[i].strip() if i < len(quantidades) else ""
            unidade = unidades[i].strip() if i < len(unidades) else ""

            if not material or not quantidade_raw:
                continue

            try:
                quantidade = float(quantidade_raw.replace(",", "."))
            except ValueError:
                continue

            tem_item_valido = True
            registro.itens.append(
                LevantamentoMaterialItem(material=material, quantidade=quantidade, unidade=unidade)
            )

        if not tem_item_valido:
            flash("Adicione pelo menos um material válido com quantidade.", "danger")
            return redirect(url_for("materiais"))

        db.session.add(registro)
        db.session.commit()
        flash("Levantamento de materiais enviado para análise.", "success")
        return redirect(url_for("materiais_historico"))

    return render_template("form_materiais.html", unidades=MATERIAL_UNIDADES)


@app.route("/materiais/historico")
@login_required
def materiais_historico():
    query = LevantamentoMaterial.query

    if session.get("usuario_perfil") not in ["admin", "supervisor"]:
        query = query.filter(LevantamentoMaterial.usuario_id == session.get("usuario_id"))

    status_filtro = request.args.get("status", "").strip()
    if status_filtro:
        query = query.filter(LevantamentoMaterial.status == status_filtro)

    busca = request.args.get("busca", "").strip()
    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            db.or_(
                LevantamentoMaterial.atividade.ilike(termo),
                LevantamentoMaterial.numero_om.ilike(termo),
                LevantamentoMaterial.numero_reserva.ilike(termo),
            )
        )

    levantamentos = query.order_by(LevantamentoMaterial.criado_em.desc()).all()

    return render_template(
        "materiais_historico.html",
        levantamentos=levantamentos,
        status_options=MATERIAL_STATUS,
        status_filtro=status_filtro,
        busca=busca,
    )


def _pode_editar_levantamento(levantamento):
    if levantamento.status != "Pendente":
        return False
    if session.get("usuario_perfil") in ["admin", "supervisor"]:
        return True
    return levantamento.usuario_id == session.get("usuario_id")


@app.route("/materiais/<int:levantamento_id>")
@login_required
def materiais_detalhe(levantamento_id):
    levantamento = LevantamentoMaterial.query.get_or_404(levantamento_id)

    if session.get("usuario_perfil") not in ["admin", "supervisor"] and levantamento.usuario_id != session.get("usuario_id"):
        flash("Você não tem permissão para acessar este levantamento.", "danger")
        return redirect(url_for("materiais_historico"))

    return render_template(
        "materiais_detalhe.html",
        levantamento=levantamento,
        pode_editar=_pode_editar_levantamento(levantamento),
    )


@app.route("/materiais/<int:levantamento_id>/analisar", methods=["POST"])
@perfil_required("admin", "supervisor")
def materiais_analisar(levantamento_id):
    levantamento = LevantamentoMaterial.query.get_or_404(levantamento_id)

    if levantamento.status != "Pendente":
        flash("Este levantamento já foi analisado.", "danger")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    decisao = request.form.get("decisao")
    observacao_analise = request.form.get("observacao_analise", "").strip()
    numero_reserva = request.form.get("numero_reserva", "").strip()

    if decisao not in ["Aprovado", "Rejeitado"]:
        flash("Decisão inválida.", "danger")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    if decisao == "Aprovado" and not numero_reserva:
        flash("Informe o número da reserva para aprovar o levantamento.", "danger")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    levantamento.status = decisao
    levantamento.observacao_analise = observacao_analise
    levantamento.numero_reserva = numero_reserva or None
    levantamento.analisado_por_id = session.get("usuario_id")
    levantamento.analisado_em = datetime.utcnow()

    db.session.commit()
    flash(f"Levantamento marcado como {decisao.lower()}.", "success")
    return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))


@app.route("/materiais/<int:levantamento_id>/editar", methods=["GET", "POST"])
@login_required
def materiais_editar(levantamento_id):
    levantamento = LevantamentoMaterial.query.get_or_404(levantamento_id)

    if not _pode_editar_levantamento(levantamento):
        flash("Este levantamento não pode mais ser editado.", "danger")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    if request.method == "POST":
        atividade = request.form.get("atividade", "").strip()
        numero_om = request.form.get("numero_om", "").strip()
        solicitante = request.form.get("solicitante", "").strip()
        observacao = request.form.get("observacao", "").strip()

        materiais_lista = request.form.getlist("item_material[]")
        quantidades = request.form.getlist("item_quantidade[]")
        unidades = request.form.getlist("item_unidade[]")

        if not atividade or not solicitante:
            flash("Preencha a atividade/OM e o solicitante.", "danger")
            return redirect(url_for("materiais_editar", levantamento_id=levantamento.id))

        itens_novos = []
        for i in range(len(materiais_lista)):
            material = materiais_lista[i].strip()
            quantidade_raw = quantidades[i].strip() if i < len(quantidades) else ""
            unidade = unidades[i].strip() if i < len(unidades) else ""

            if not material or not quantidade_raw:
                continue

            try:
                quantidade = float(quantidade_raw.replace(",", "."))
            except ValueError:
                continue

            itens_novos.append(LevantamentoMaterialItem(material=material, quantidade=quantidade, unidade=unidade))

        if not itens_novos:
            flash("Adicione pelo menos um material válido com quantidade.", "danger")
            return redirect(url_for("materiais_editar", levantamento_id=levantamento.id))

        levantamento.atividade = atividade
        levantamento.numero_om = numero_om
        levantamento.solicitante = solicitante
        levantamento.observacao = observacao
        levantamento.itens = itens_novos

        db.session.commit()
        flash("Levantamento atualizado.", "success")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    return render_template(
        "form_materiais.html",
        unidades=MATERIAL_UNIDADES,
        levantamento=levantamento,
    )


@app.route("/materiais/<int:levantamento_id>/cancelar", methods=["POST"])
@login_required
def materiais_cancelar(levantamento_id):
    levantamento = LevantamentoMaterial.query.get_or_404(levantamento_id)

    if not _pode_editar_levantamento(levantamento):
        flash("Este levantamento não pode mais ser cancelado.", "danger")
        return redirect(url_for("materiais_detalhe", levantamento_id=levantamento.id))

    levantamento.status = "Cancelado"
    levantamento.analisado_por_id = session.get("usuario_id")
    levantamento.analisado_em = datetime.utcnow()

    db.session.commit()
    flash("Levantamento cancelado.", "success")
    return redirect(url_for("materiais_historico"))


@app.route("/checklists")
@login_required
def checklist_modelos():
    modelos = ChecklistModelo.query.filter_by(ativo=True).order_by(ChecklistModelo.nome.asc()).all()
    return render_template("checklist_modelos.html", modelos=modelos)


@app.route("/checklists/<int:modelo_id>", methods=["GET", "POST"])
@login_required
def checklist_preencher(modelo_id):
    modelo = ChecklistModelo.query.get_or_404(modelo_id)

    campos_cabecalho = ChecklistCampoCabecalho.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistCampoCabecalho.ordem.asc()).all()

    secoes = ChecklistSecao.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistSecao.ordem.asc()).all()

    # Busca último histórico útil das observações gerais
    historico_observacoes = {}

    execucoes_anteriores = (
        ChecklistExecucao.query
        .filter_by(checklist_modelo_id=modelo.id)
        .order_by(ChecklistExecucao.id.desc())
        .all()
    )

    itens_processados = set()

    for exec_ant in execucoes_anteriores:
        for resposta in exec_ant.respostas:
            item_id = resposta.checklist_item_modelo_id

            if item_id in itens_processados:
                continue

            resolvido_norm = (resposta.resolvido or "").strip().lower()
            chamado = (resposta.chamado or "").strip()
            descricao = (resposta.descricao_problema or "").strip()

            # ignora respostas totalmente vazias
            if not resolvido_norm and not chamado and not descricao:
                continue

            itens_processados.add(item_id)

            # só reaproveita se o último estado útil foi "nao"
            if resolvido_norm == "nao" and descricao:
                historico_observacoes[item_id] = {
                    "chamado": chamado,
                    "descricao_problema": descricao,
                    "resolvido": resolvido_norm,
                }

    if request.method == "POST":
        execucao = ChecklistExecucao(
            checklist_modelo_id=modelo.id,
            usuario_id=session.get("usuario_id"),
            status_execucao="concluido"
        )

        for campo in campos_cabecalho:
            valor = request.form.get(campo.nome_campo, "").strip()
            execucao.cabecalhos.append(
                ChecklistExecucaoCabecalho(
                    nome_campo=campo.nome_campo,
                    valor_texto=valor
                )
            )

        for secao in secoes:
            itens_ordenados = sorted(secao.itens, key=lambda x: x.ordem)

            for item in itens_ordenados:
                status_marcacao = request.form.get(f"item_{item.id}_status", "").strip()
                valor_r = request.form.get(f"item_{item.id}_r", "").strip()
                valor_s = request.form.get(f"item_{item.id}_s", "").strip()
                valor_t = request.form.get(f"item_{item.id}_t", "").strip()
                observacao = request.form.get(f"item_{item.id}_observacao", "").strip()
                resolvido = request.form.get(f"item_{item.id}_resolvido", "").strip().lower()
                chamado = request.form.get(f"item_{item.id}_chamado", "").strip()
                descricao_problema = request.form.get(f"item_{item.id}_descricao_problema", "").strip()

                if resolvido == "sim":
                    descricao_problema = ""

                if resolvido == "nao" and not descricao_problema:
                    flash("Quando marcar 'Não' em Resolvido, a descrição do problema é obrigatória.", "danger")
                    return redirect(request.url)

                resposta = ChecklistResposta(
                    checklist_item_modelo_id=item.id,
                    status_marcacao=status_marcacao,
                    valor_r=valor_r,
                    valor_s=valor_s,
                    valor_t=valor_t,
                    observacao=observacao,
                    resolvido=resolvido,
                    chamado=chamado,
                    descricao_problema=descricao_problema,
                )

                execucao.respostas.append(resposta)

        db.session.add(execucao)
        db.session.commit()

        flash("Checklist salvo com sucesso.", "success")
        return redirect(url_for("checklist_historico"))

    return render_template(
        "checklist_preencher.html",
        modelo=modelo,
        campos_cabecalho=campos_cabecalho,
        secoes=secoes,
        historico_observacoes=historico_observacoes,
    )

# ====== ADMIN CHECKLISTS ======
# Cole este bloco no app.py, depois das rotas principais de checklist.
# Ajuste apenas se os nomes dos seus modelos/atributos forem diferentes.

from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func

@app.route("/admin/checklists")
@perfil_required("admin")
def admin_checklist_modelos():
    busca = request.args.get("q", "").strip()
    area = request.args.get("area", "").strip()
    ativo = request.args.get("ativo", "").strip()

    query = ChecklistModelo.query

    if busca:
        termo = f"%{busca}%"
        query = query.filter(
            db.or_(
                ChecklistModelo.nome.ilike(termo),
                ChecklistModelo.codigo.ilike(termo),
                ChecklistModelo.descricao.ilike(termo),
            )
        )

    if area:
        query = query.filter(ChecklistModelo.area_padrao == area)

    if ativo == "1":
        query = query.filter(ChecklistModelo.ativo.is_(True))
    elif ativo == "0":
        query = query.filter(ChecklistModelo.ativo.is_(False))

    modelos = query.order_by(ChecklistModelo.nome.asc()).all()

    areas = (
        db.session.query(ChecklistModelo.area_padrao)
        .filter(ChecklistModelo.area_padrao.isnot(None))
        .filter(ChecklistModelo.area_padrao != "")
        .distinct()
        .order_by(ChecklistModelo.area_padrao.asc())
        .all()
    )
    areas = [a[0] for a in areas]

    resumo = {}
    for modelo in modelos:
        total_secoes = ChecklistSecao.query.filter_by(checklist_modelo_id=modelo.id).count()
        total_itens = (
            db.session.query(func.count(ChecklistItemModelo.id))
            .join(ChecklistSecao, ChecklistItemModelo.checklist_secao_id == ChecklistSecao.id)
            .filter(ChecklistSecao.checklist_modelo_id == modelo.id)
            .scalar()
        ) or 0
        resumo[modelo.id] = {
            "total_secoes": total_secoes,
            "total_itens": total_itens,
        }

    return render_template(
        "admin_checklist_modelos.html",
        modelos=modelos,
        areas=areas,
        resumo=resumo,
        busca=busca,
        area=area,
        ativo=ativo,
    )


@app.route("/admin/checklists/<int:modelo_id>/editar", methods=["GET", "POST"])
@perfil_required("admin")
def admin_editar_checklist_modelo(modelo_id):
    modelo = ChecklistModelo.query.get_or_404(modelo_id)

    if request.method == "POST":
        modelo.nome = request.form.get("nome", "").strip()
        modelo.codigo = request.form.get("codigo", "").strip()
        modelo.descricao = request.form.get("descricao", "").strip()
        modelo.area_padrao = request.form.get("area_padrao", "").strip()
        modelo.ativo = request.form.get("ativo") == "1"

        if not modelo.nome:
            flash("O nome do modelo é obrigatório.", "danger")
            return redirect(request.url)

        secoes = ChecklistSecao.query.filter_by(
            checklist_modelo_id=modelo.id
        ).order_by(ChecklistSecao.ordem.asc()).all()

        for secao in secoes:
            titulo = request.form.get(f"secao_{secao.id}_titulo", "").strip()
            ordem = request.form.get(f"secao_{secao.id}_ordem", "").strip()

            if titulo:
                secao.titulo = titulo

            try:
                secao.ordem = int(ordem) if ordem else secao.ordem
            except ValueError:
                pass

            itens = ChecklistItemModelo.query.filter_by(
                checklist_secao_id=secao.id
            ).order_by(ChecklistItemModelo.ordem.asc()).all()

            for item in itens:
                numero_item = request.form.get(f"item_{item.id}_numero_item", "").strip()
                descricao = request.form.get(f"item_{item.id}_descricao", "").strip()
                ordem_item = request.form.get(f"item_{item.id}_ordem", "").strip()

                item.numero_item = numero_item
                item.descricao = descricao

                try:
                    item.ordem = int(ordem_item) if ordem_item else item.ordem
                except ValueError:
                    pass

                item.usa_normal_anormal = request.form.get(f"item_{item.id}_usa_normal_anormal") == "1"
                item.usa_valores_rst = request.form.get(f"item_{item.id}_usa_valores_rst") == "1"
                item.usa_observacao = request.form.get(f"item_{item.id}_usa_observacao") == "1"
                item.usa_resolvido = request.form.get(f"item_{item.id}_usa_resolvido") == "1"

        db.session.commit()
        flash("Modelo atualizado com sucesso.", "success")
        return redirect(url_for("admin_editar_checklist_modelo", modelo_id=modelo.id))

    secoes = ChecklistSecao.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistSecao.ordem.asc()).all()

    for secao in secoes:
        secao.itens_admin = ChecklistItemModelo.query.filter_by(
            checklist_secao_id=secao.id
        ).order_by(ChecklistItemModelo.ordem.asc()).all()

    return render_template(
        "admin_checklist_modelo_editar.html",
        modelo=modelo,
        secoes=secoes,
    )


@app.route("/admin/checklists/<int:modelo_id>/toggle-ativo", methods=["POST"])
@perfil_required("admin")
def admin_toggle_checklist_modelo(modelo_id):
    modelo = ChecklistModelo.query.get_or_404(modelo_id)
    modelo.ativo = not bool(modelo.ativo)
    db.session.commit()

    status = "ativado" if modelo.ativo else "desativado"
    flash(f'Modelo "{modelo.nome}" {status} com sucesso.', "success")
    return redirect(url_for("admin_checklist_modelos"))


@app.route("/admin/checklists/<int:modelo_id>/duplicar", methods=["POST"])
@perfil_required("admin")
def admin_duplicar_checklist_modelo(modelo_id):
    modelo = ChecklistModelo.query.get_or_404(modelo_id)

    novo_modelo = ChecklistModelo(
        nome=f"{modelo.nome} - Cópia",
        codigo=f"{(modelo.codigo or 'SEM-CODIGO')}-COPIA",
        descricao=modelo.descricao,
        area_padrao=modelo.area_padrao,
        ativo=False,
    )
    db.session.add(novo_modelo)
    db.session.flush()

    campos = ChecklistCampoCabecalho.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistCampoCabecalho.ordem.asc()).all()

    for campo in campos:
        db.session.add(
            ChecklistCampoCabecalho(
                checklist_modelo_id=novo_modelo.id,
                nome_campo=campo.nome_campo,
                label_campo=campo.label_campo,
                tipo_campo=campo.tipo_campo,
                obrigatorio=campo.obrigatorio,
                ordem=campo.ordem,
            )
        )

    secoes = ChecklistSecao.query.filter_by(
        checklist_modelo_id=modelo.id
    ).order_by(ChecklistSecao.ordem.asc()).all()

    for secao in secoes:
        nova_secao = ChecklistSecao(
            checklist_modelo_id=novo_modelo.id,
            titulo=secao.titulo,
            tipo_secao=secao.tipo_secao,
            ordem=secao.ordem,
        )
        db.session.add(nova_secao)
        db.session.flush()

        itens = ChecklistItemModelo.query.filter_by(
            checklist_secao_id=secao.id
        ).order_by(ChecklistItemModelo.ordem.asc()).all()

        for item in itens:
            db.session.add(
                ChecklistItemModelo(
                    checklist_secao_id=nova_secao.id,
                    numero_item=item.numero_item,
                    descricao=item.descricao,
                    tipo_resposta=item.tipo_resposta,
                    usa_normal_anormal=item.usa_normal_anormal,
                    usa_valores_rst=item.usa_valores_rst,
                    usa_observacao=item.usa_observacao,
                    usa_resolvido=item.usa_resolvido,
                    ordem=item.ordem,
                )
            )

    db.session.commit()
    flash(f'Modelo "{modelo.nome}" duplicado com sucesso.', "success")
    return redirect(url_for("admin_editar_checklist_modelo", modelo_id=novo_modelo.id))


@app.route("/checklists/historico")
@login_required
def checklist_historico():
    execucoes = ChecklistExecucao.query.order_by(ChecklistExecucao.criado_em.desc()).all()

    def valor_cabecalho(execucao, nome_campo):
        for campo in execucao.cabecalhos:
            if campo.nome_campo == nome_campo:
                return campo.valor_texto
        return ""

    return render_template(
        "checklist_historico.html",
        execucoes=execucoes,
        valor_cabecalho=valor_cabecalho
    )

    
@app.route("/checklists/historico/<int:execucao_id>")
@login_required
def checklist_execucao_detalhe(execucao_id):
    execucao = ChecklistExecucao.query.get_or_404(execucao_id)

    cabecalho = {}
    for campo in execucao.cabecalhos:
        cabecalho[campo.nome_campo] = campo.valor_texto

    respostas_map = {}
    for resposta in execucao.respostas:
        respostas_map[resposta.checklist_item_modelo_id] = resposta

    secoes = ChecklistSecao.query.filter_by(
        checklist_modelo_id=execucao.checklist_modelo_id
    ).order_by(ChecklistSecao.ordem.asc()).all()

    campos_modelo = ChecklistCampoCabecalho.query.filter_by(
        checklist_modelo_id=execucao.checklist_modelo_id
    ).order_by(ChecklistCampoCabecalho.ordem.asc()).all()

    labels_cabecalho = {}
    for campo in campos_modelo:
        labels_cabecalho[campo.nome_campo] = campo.label_campo

    total_respostas = len(execucao.respostas)
    total_normais = sum(1 for r in execucao.respostas if r.status_marcacao == "Normal")
    total_anormais = sum(1 for r in execucao.respostas if r.status_marcacao == "Anormal")
    total_com_obs = sum(
        1 for r in execucao.respostas
        if (r.observacao and r.observacao.strip()) or (r.descricao_problema and r.descricao_problema.strip())
    )
    total_resolvidos = sum(1 for r in execucao.respostas if r.resolvido == "Sim")



    return render_template(
        "checklist_execucao_detalhe.html",
        execucao=execucao,
        cabecalho=cabecalho,
        labels_cabecalho=labels_cabecalho,
        secoes=secoes,
        respostas_map=respostas_map,
        total_respostas=total_respostas,
        total_normais=total_normais,
        total_anormais=total_anormais,
        total_com_obs=total_com_obs,
        total_resolvidos=total_resolvidos
    )

class ChecklistExecucao(db.Model):
    __tablename__ = "checklist_execucoes"

    id = db.Column(db.Integer, primary_key=True)
    checklist_modelo_id = db.Column(db.Integer, db.ForeignKey("checklist_modelos.id"), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    status_execucao = db.Column(db.String(50), nullable=False, default="concluido")
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    modelo = db.relationship("ChecklistModelo", foreign_keys=[checklist_modelo_id])
    usuario = db.relationship("Usuario", foreign_keys=[usuario_id])

    cabecalhos = db.relationship(
        "ChecklistExecucaoCabecalho",
        backref="execucao",
        cascade="all, delete-orphan",
        lazy=True
    )

    respostas = db.relationship(
        "ChecklistResposta",
        backref="execucao",
        cascade="all, delete-orphan",
        lazy=True
    )


class ChecklistExecucaoCabecalho(db.Model):
    __tablename__ = "checklist_execucao_cabecalho"

    id = db.Column(db.Integer, primary_key=True)
    checklist_execucao_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_execucoes.id", ondelete="CASCADE"),
        nullable=False
    )
    nome_campo = db.Column(db.String(100), nullable=False)
    valor_texto = db.Column(db.Text)


class ChecklistResposta(db.Model):
    __tablename__ = "checklist_respostas"

    id = db.Column(db.Integer, primary_key=True)
    checklist_execucao_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_execucoes.id", ondelete="CASCADE"),
        nullable=False
    )
    checklist_item_modelo_id = db.Column(
        db.Integer,
        db.ForeignKey("checklist_itens_modelo.id", ondelete="CASCADE"),
        nullable=False
    )

    status_marcacao = db.Column(db.String(20))
    valor_r = db.Column(db.String(50))
    valor_s = db.Column(db.String(50))
    valor_t = db.Column(db.String(50))
    observacao = db.Column(db.Text)
    resolvido = db.Column(db.String(10))
    chamado = db.Column(db.String(50))
    descricao_problema = db.Column(db.Text)

    item_modelo = db.relationship("ChecklistItemModelo", foreign_keys=[checklist_item_modelo_id])



@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {"status":"ok","database":"connected"}
    except Exception as e:
        return {"status":"error","message":str(e)}, 500

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug_mode)


