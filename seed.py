"""
seed.py — Datos iniciales de MangaVerse
========================================
Se ejecuta automáticamente al iniciar la app si la BD está vacía.
Solo inserta si no hay datos (es idempotente: puedes llamarlo N veces).
"""

from werkzeug.security import generate_password_hash
from database.models import db, Usuario, Manga, Capitulo


MANGAS_DEMO = [
    {"titulo": "Demon Slayer",      "autor": "Koyoharu Gotouge",  "descripcion": "Tanjiro Kamado se convierte en un cazador de demonios para salvar a su hermana transformada en demonio.",           "genero": "Acción, Aventura, Sobrenatural",    "portada_url": "https://cdn.myanimelist.net/images/manga/3/179023l.jpg", "banner_url": "https://cdn.myanimelist.net/images/manga/3/179023l.jpg", "acceso_libre": True,  "capitulos_num": 205,  "valoracion": 9.1, "estado": "Completo"},
    {"titulo": "One Piece",         "autor": "Eiichiro Oda",      "descripcion": "Monkey D. Luffy explora el Grand Line en busca del legendario tesoro conocido como One Piece.",                    "genero": "Aventura, Fantasía, Comedia",       "portada_url": "https://cdn.myanimelist.net/images/manga/2/253146l.jpg", "banner_url": "https://cdn.myanimelist.net/images/manga/2/253146l.jpg", "acceso_libre": True,  "capitulos_num": 1110, "valoracion": 9.5, "estado": "En emisión"},
    {"titulo": "Jujutsu Kaisen",    "autor": "Gege Akutami",      "descripcion": "Yuji Itadori se une a una organización secreta de hechiceros para matar a Ryomen Sukuna, el Rey de las Maldiciones.", "genero": "Acción, Sobrenatural, Horror",   "portada_url": "/static/img/Jujutsu.jpg",                                "banner_url": "/static/img/Jujutsu.jpg",                                "acceso_libre": False, "capitulos_num": 266,  "valoracion": 9.3, "estado": "Completo"},
    {"titulo": "Attack on Titan",   "autor": "Hajime Isayama",    "descripcion": "En un mundo rodeado de muros, Eren Jaeger jura destruir a todos los titanes.",                                       "genero": "Acción, Drama, Misterio",          "portada_url": "https://cdn.myanimelist.net/images/manga/2/37846l.jpg",  "banner_url": "https://cdn.myanimelist.net/images/manga/2/37846l.jpg",  "acceso_libre": False, "capitulos_num": 139,  "valoracion": 9.7, "estado": "Completo"},
    {"titulo": "My Hero Academia",  "autor": "Kōhei Horikoshi",   "descripcion": "Izuku Midoriya nació sin poderes pero sueña con convertirse en el mejor héroe.",                                    "genero": "Acción, Superhéroes, Escolar",      "portada_url": "https://cdn.myanimelist.net/images/manga/1/209370l.jpg", "banner_url": "https://cdn.myanimelist.net/images/manga/1/209370l.jpg", "acceso_libre": True,  "capitulos_num": 430,  "valoracion": 8.9, "estado": "Completo"},
    {"titulo": "Chainsaw Man",      "autor": "Tatsuki Fujimoto",  "descripcion": "Denji fusiona su cuerpo con su demonio perro Pochita, adquiriendo poderes de motosierra.",                          "genero": "Acción, Horror, Sobrenatural",      "portada_url": "https://cdn.myanimelist.net/images/manga/3/216464l.jpg", "banner_url": "https://cdn.myanimelist.net/images/manga/3/216464l.jpg", "acceso_libre": False, "capitulos_num": 197,  "valoracion": 9.4, "estado": "En emisión"},
    {"titulo": "Naruto",            "autor": "Masashi Kishimoto", "descripcion": "Naruto Uzumaki sueña con convertirse en Hokage y carga con el espíritu del zorro de nueve colas.",                  "genero": "Acción, Aventura, Artes marciales", "portada_url": "https://cdn.myanimelist.net/images/manga/3/117681l.jpg", "banner_url": "https://cdn.myanimelist.net/images/manga/3/117681l.jpg", "acceso_libre": True,  "capitulos_num": 700,  "valoracion": 9.0, "estado": "Completo"},
    {"titulo": "Tokyo Revengers",   "autor": "Ken Wakui",         "descripcion": "Takemichi Hanagaki viaja al pasado para salvar a su ex novia de una banda de delincuentes.",                        "genero": "Acción, Drama, Viaje en el tiempo", "portada_url": "/static/img/Tokyio.jpg",                                 "banner_url": "/static/img/Tokyio.jpg",                                 "acceso_libre": False, "capitulos_num": 278,  "valoracion": 8.7, "estado": "Completo"},
    {"titulo": "My Happy Marriage", "autor": "Akumi Agitogi",     "descripcion": "Una joven infeliz es casada con un frío comandante. Cuando se conocen mejor, el amor tiene una oportunidad.",       "genero": "Romance, Drama, Fantasía",          "portada_url": "/static/img/myhappymarriage.jpg",                        "banner_url": "/static/img/myhappymarriage.jpg",                        "acceso_libre": False, "capitulos_num": 33,   "valoracion": 9.0, "estado": "En emisión"},
]


def sembrar_bd():
    """Crea tablas e inserta datos si la BD está vacía."""
    db.create_all()

    if Manga.query.count() == 0:
        for data in MANGAS_DEMO:
            manga = Manga(**data)
            db.session.add(manga)
            for i in range(1, min(6, data['capitulos_num'] + 1)):
                db.session.add(Capitulo(manga=manga, numero=i, titulo=f'Capítulo {i}', paginas=22))
        db.session.commit()
        print('✅ Mangas de demo insertados.')

    if not Usuario.query.filter_by(email='demo@manga.com').first():
        db.session.add(Usuario(
            nombre='Demo User',
            email='demo@manga.com',
            password_hash=generate_password_hash('demo1234'),
            plan='premium'
        ))
        db.session.commit()
        print('✅ Usuario demo: demo@manga.com / demo1234')
