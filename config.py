"""
config.py — Configuración de conexión a la base de datos
=========================================================
DESARROLLO  → MODO=sqlite  (sin instalar nada extra)
PRODUCCIÓN  → MODO=mysql   (Railway, PlanetScale, Aiven…)

Para cambiar de modo edita la variable MODO O
pon la variable de entorno:
    export MANGAVERSE_MODO=mysql
"""

import os


# ─── MODO ACTIVO ─────────────────────────────────────────────
# Cambia 'sqlite' → 'mysql' cuando tengas la BD en la nube
MODO = os.getenv('MANGAVERSE_MODO', 'mysql')

# ─── SQLITE (solo desarrollo local) ─────────────────────────
SQLITE_URI = 'sqlite:///mangaverse.db'


# ─── MYSQL ───────────────────────────────────────────────────
# Rellena con los datos que te dé Railway / TablePlus / tu proveedor
# O ponlos como variables de entorno (más seguro)
MYSQL_HOST     = os.getenv('DB_HOST',     'localhost')
MYSQL_PORT     = os.getenv('DB_PORT',     '3306')
MYSQL_USER     = os.getenv('DB_USER',     'root')
MYSQL_PASSWORD = os.getenv('DB_PASSWORD', '')
MYSQL_DATABASE = os.getenv('DB_NAME',     'mangaverse')

MYSQL_URI = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    f"?charset=utf8mb4"
)


# ─── SELECTOR ────────────────────────────────────────────────
def get_database_uri() -> str:
    if MODO == 'mysql':
        return MYSQL_URI
    return SQLITE_URI


# ─── CLASE DE CONFIGURACIÓN FLASK ────────────────────────────
class Config:
    SECRET_KEY                     = os.getenv('SECRET_KEY', 'mangaverse-secret-2024')
    SQLALCHEMY_DATABASE_URI        = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Reconexión automática si la BD cierra la conexión (importante en nube)
    SQLALCHEMY_ENGINE_OPTIONS      = {
        'pool_pre_ping': True,
        'pool_recycle':  300,
    }
