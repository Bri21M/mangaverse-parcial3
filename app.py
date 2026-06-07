"""
app.py — MangaVerse · Punto de entrada Flask
=============================================
Solo contiene rutas. Cada responsabilidad en su propio archivo:
  config.py   → conexión a BD (SQLite / MySQL)
  database/   → modelos ORM
  seed.py     → datos de demo
"""

from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

from config import Config
from database.models import db, Usuario, Manga, Capitulo, Favorito, Historial
from seed import sembrar_bd


# ─── Inicialización ───────────────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view    = 'login'
login_manager.login_message = 'Inicia sesión para continuar.'


@login_manager.user_loader
def cargar_usuario(uid):
    return Usuario.query.get(int(uid))


# ─── Rutas públicas ───────────────────────────────────────────

@app.route('/')
def index():
    destacados = Manga.query.order_by(Manga.valoracion.desc()).limit(6).all()
    recientes  = Manga.query.order_by(Manga.fecha_adicion.desc()).limit(8).all()
    libres     = Manga.query.filter_by(acceso_libre=True).limit(4).all()
    return render_template('index.html',
                           destacados=destacados,
                           recientes=recientes,
                           libres=libres)


@app.route('/catalogo')
def catalogo():
    genero = request.args.get('genero', '')
    buscar = request.args.get('q', '')
    query  = Manga.query
    if genero:
        query = query.filter(Manga.genero.contains(genero))
    if buscar:
        query = query.filter(Manga.titulo.ilike(f'%{buscar}%'))
    mangas  = query.order_by(Manga.valoracion.desc()).all()
    generos = ['Acción', 'Aventura', 'Romance', 'Comedia', 'Horror', 'Drama', 'Sobrenatural', 'Fantasía']
    return render_template('catalogo.html', mangas=mangas, generos=generos,
                           genero_activo=genero, busqueda=buscar)


@app.route('/manga/<int:manga_id>')
def detalle_manga(manga_id):
    manga       = Manga.query.get_or_404(manga_id)
    capitulos   = Capitulo.query.filter_by(manga_id=manga_id).order_by(Capitulo.numero).all()
    puede_leer  = True
    es_favorito = False
    if current_user.is_authenticated:
        puede_leer  = current_user.puede_leer(manga)
        es_favorito = Favorito.query.filter_by(
            usuario_id=current_user.id, manga_id=manga_id).first() is not None
    return render_template('detalle.html', manga=manga, capitulos=capitulos,
                           puede_leer=puede_leer, es_favorito=es_favorito)


@app.route('/planes')
def planes():
    return render_template('planes.html')


# ─── Rutas protegidas ─────────────────────────────────────────

@app.route('/leer/<int:manga_id>/<int:cap_num>')
@login_required
def leer(manga_id, cap_num):
    manga = Manga.query.get_or_404(manga_id)
    if not current_user.puede_leer(manga):
        flash('Necesitas suscripción Premium para leer este manga.', 'warning')
        return redirect(url_for('planes'))
    capitulo = Capitulo.query.filter_by(manga_id=manga_id, numero=cap_num).first_or_404()
    hist = Historial.query.filter_by(usuario_id=current_user.id, manga_id=manga_id).first()
    if hist:
        hist.ultimo_capitulo = cap_num
    else:
        db.session.add(Historial(usuario_id=current_user.id, manga_id=manga_id, ultimo_capitulo=cap_num))
    db.session.commit()
    return render_template('leer.html', manga=manga, capitulo=capitulo)


@app.route('/favorito/<int:manga_id>', methods=['POST'])
@login_required
def toggle_favorito(manga_id):
    fav = Favorito.query.filter_by(usuario_id=current_user.id, manga_id=manga_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({'estado': 'eliminado'})
    db.session.add(Favorito(usuario_id=current_user.id, manga_id=manga_id))
    db.session.commit()
    return jsonify({'estado': 'agregado'})


@app.route('/perfil')
@login_required
def perfil():
    favoritos = Favorito.query.filter_by(usuario_id=current_user.id).join(Manga).all()
    historial = (Historial.query
                 .filter_by(usuario_id=current_user.id)
                 .order_by(Historial.ultima_lectura.desc()).all())
    return render_template('perfil.html', favoritos=favoritos, historial=historial)


# ─── Autenticación ────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Autenticación contra la BD (local o en nube según config.py).
    Flujo:
      1. Busca el usuario por email en la tabla `usuarios`
      2. Verifica la contraseña con check_password_hash
      3. Si OK  → login_user() y redirige al inicio
      4. Si NO  → flash de error, muestra el form otra vez
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # 1. Consulta a la BD (SQLite o MySQL, transparente)
        usuario = Usuario.query.filter_by(email=email).first()

        # 2. Validación de credenciales
        if usuario and usuario.activo and check_password_hash(usuario.password_hash, password):
            # 3. Acceso concedido
            login_user(usuario, remember=True)
            flash(f'¡Bienvenido de vuelta, {usuario.nombre}!', 'success')
            # Redirige a la página que intentaba visitar, o al inicio
            siguiente = request.args.get('next') or url_for('index')
            return redirect(siguiente)

        # 4. Acceso denegado
        flash('Correo o contraseña incorrectos. Inténtalo de nuevo.', 'error')

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre   = request.form.get('nombre', '').strip()
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('Ese correo ya está registrado.', 'error')
            return redirect(url_for('registro'))

        nuevo = Usuario(
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
            plan='free'
        )
        db.session.add(nuevo)
        db.session.commit()
        login_user(nuevo)
        flash('¡Cuenta creada exitosamente!', 'success')
        return redirect(url_for('index'))

    return render_template('registro.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# ─── Arranque ─────────────────────────────────────────────────
if __name__ == '__main__':
    with app.app_context():
        sembrar_bd()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5050)), debug=False)
