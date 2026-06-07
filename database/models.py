"""
database/models.py
==================
Modelos ORM para MangaVerse (SQLAlchemy).
Compatible con SQLite (desarrollo) y MySQL (producción).

Aquí se DEFINE la estructura de la base de datos.
db.create_all() (llamado desde seed.py) CREA las tablas físicas.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id             = db.Column(db.Integer,      primary_key=True)
    nombre         = db.Column(db.String(100),  nullable=False)
    email          = db.Column(db.String(150),  nullable=False, unique=True)
    password_hash  = db.Column(db.String(256),  nullable=False)
    plan           = db.Column(db.String(20),   default='free')   # free | premium | ultra
    activo         = db.Column(db.Boolean,      default=True)
    fecha_registro = db.Column(db.DateTime,     default=datetime.utcnow)

    favoritos = db.relationship('Favorito',  back_populates='usuario', cascade='all, delete-orphan')
    historial = db.relationship('Historial', back_populates='usuario', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Usuario {self.email} | {self.plan}>'

    def puede_leer(self, manga) -> bool:
        """Devuelve True si el usuario tiene acceso al manga según su plan."""
        if self.plan in ('premium', 'ultra'):
            return True
        return manga.acceso_libre


class Manga(db.Model):
    __tablename__ = 'mangas'

    id            = db.Column(db.Integer,      primary_key=True)
    titulo        = db.Column(db.String(200),  nullable=False)
    autor         = db.Column(db.String(100),  nullable=False)
    descripcion   = db.Column(db.Text,         nullable=False)
    genero        = db.Column(db.String(100),  nullable=False)
    portada_url   = db.Column(db.String(300),  nullable=False)
    banner_url    = db.Column(db.String(300),  nullable=True)
    acceso_libre  = db.Column(db.Boolean,      default=False)
    capitulos_num = db.Column(db.Integer,      default=0)
    valoracion    = db.Column(db.Float,        default=0.0)
    estado        = db.Column(db.String(30),   default='En emisión')
    fecha_adicion = db.Column(db.DateTime,     default=datetime.utcnow)

    capitulos = db.relationship('Capitulo',  back_populates='manga', cascade='all, delete-orphan')
    favoritos = db.relationship('Favorito',  back_populates='manga', cascade='all, delete-orphan')
    historial = db.relationship('Historial', back_populates='manga', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Manga {self.titulo}>'


class Capitulo(db.Model):
    __tablename__ = 'capitulos'

    id        = db.Column(db.Integer,     primary_key=True)
    manga_id  = db.Column(db.Integer,     db.ForeignKey('mangas.id'), nullable=False)
    numero    = db.Column(db.Integer,     nullable=False)
    titulo    = db.Column(db.String(200), nullable=True)
    paginas   = db.Column(db.Integer,     default=20)
    fecha_pub = db.Column(db.DateTime,    default=datetime.utcnow)

    manga = db.relationship('Manga', back_populates='capitulos')

    def __repr__(self):
        return f'<Capitulo {self.numero} — {self.manga.titulo}>'


class Favorito(db.Model):
    __tablename__ = 'favoritos'

    id         = db.Column(db.Integer,  primary_key=True)
    usuario_id = db.Column(db.Integer,  db.ForeignKey('usuarios.id'), nullable=False)
    manga_id   = db.Column(db.Integer,  db.ForeignKey('mangas.id'),   nullable=False)
    fecha      = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', back_populates='favoritos')
    manga   = db.relationship('Manga',   back_populates='favoritos')


class Historial(db.Model):
    __tablename__ = 'historial'

    id              = db.Column(db.Integer,  primary_key=True)
    usuario_id      = db.Column(db.Integer,  db.ForeignKey('usuarios.id'), nullable=False)
    manga_id        = db.Column(db.Integer,  db.ForeignKey('mangas.id'),   nullable=False)
    ultimo_capitulo = db.Column(db.Integer,  default=1)
    ultima_lectura  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = db.relationship('Usuario', back_populates='historial')
    manga   = db.relationship('Manga',   back_populates='historial')
