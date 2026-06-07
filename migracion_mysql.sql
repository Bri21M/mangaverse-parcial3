-- ============================================================
--  MangaVerse — Script de migración SQLite → MySQL
--  Ejecuta esto en TablePlus o en tu cliente MySQL
--  Paso 1: Crea la BD  |  Paso 2: Tablas  |  Paso 3: Datos
-- ============================================================

-- PASO 1 ─ Crear la base de datos
CREATE DATABASE IF NOT EXISTS mangaverse
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE mangaverse;

-- ============================================================
-- PASO 2 ─ Crear tablas (mismo esquema, sintaxis MySQL)
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id             INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(100)  NOT NULL,
    email          VARCHAR(150)  NOT NULL UNIQUE,
    password_hash  VARCHAR(256)  NOT NULL,
    plan           VARCHAR(20)   DEFAULT 'free',
    activo         TINYINT(1)    DEFAULT 1,
    fecha_registro DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS mangas (
    id            INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    titulo        VARCHAR(200)  NOT NULL,
    autor         VARCHAR(100)  NOT NULL,
    descripcion   TEXT          NOT NULL,
    genero        VARCHAR(100)  NOT NULL,
    portada_url   VARCHAR(300)  NOT NULL,
    banner_url    VARCHAR(300)  DEFAULT NULL,
    acceso_libre  TINYINT(1)    DEFAULT 0,
    capitulos_num INT           DEFAULT 0,
    valoracion    FLOAT         DEFAULT 0.0,
    estado        VARCHAR(30)   DEFAULT 'En emisión',
    fecha_adicion DATETIME      DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS capitulos (
    id        INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    manga_id  INT           NOT NULL,
    numero    INT           NOT NULL,
    titulo    VARCHAR(200)  DEFAULT NULL,
    paginas   INT           DEFAULT 20,
    fecha_pub DATETIME      DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manga_id) REFERENCES mangas(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS favoritos (
    id         INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT      NOT NULL,
    manga_id   INT      NOT NULL,
    fecha      DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (manga_id)   REFERENCES mangas(id)   ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS historial (
    id              INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
    usuario_id      INT      NOT NULL,
    manga_id        INT      NOT NULL,
    ultimo_capitulo INT      DEFAULT 1,
    ultima_lectura  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (manga_id)   REFERENCES mangas(id)   ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- PASO 3 ─ Insertar datos migrados desde SQLite
-- ============================================================

-- Usuarios (passwords en scrypt, compatibles con werkzeug)
INSERT INTO usuarios (id, nombre, email, password_hash, plan, activo, fecha_registro) VALUES
(1, 'Demo User',    'demo@manga.com',                         'scrypt:32768:8:1$nN0ic4Lup8eDb4Jg$15b6307d6beb30d7bbc4cee1de2135513f1c00669f611f75eaf5a185247003e7a5f8d74bb9da14d5c36475a20754976e9401733075e80e3e15a355c896e3aeda', 'premium', 1, '2026-05-30 17:13:14'),
(2, 'Bristom_21',   'brisaguadalupemartinezmendez@gmail.com',  'scrypt:32768:8:1$OLe6h0JNr5WsiOjA$4457c29568a2bd03e0f7b6b1183efec884f95ec594315fd7d0fb494e843eb34d6067be236af66170dbe5df2aef14e552eaf7db2717f8e2e0d376c215f9d05513', 'free',    1, '2026-05-30 17:22:37');

-- Mangas
INSERT INTO mangas (id, titulo, autor, descripcion, genero, portada_url, banner_url, acceso_libre, capitulos_num, valoracion, estado, fecha_adicion) VALUES
(1, 'Demon Slayer',      'Koyoharu Gotouge', 'Tanjiro Kamado se convierte en un cazador de demonios para salvar a su hermana transformada en demonio y vengar a su familia masacrada.',                                                                                                    'Acción, Aventura, Sobrenatural',       'https://cdn.myanimelist.net/images/manga/3/179023l.jpg', 'https://cdn.myanimelist.net/images/manga/3/179023l.jpg', 1, 205,  9.1, 'Completo',   '2026-05-30 17:13:14'),
(2, 'One Piece',         'Eiichiro Oda',     'Monkey D. Luffy explora el Grand Line en busca del legendario tesoro conocido como One Piece para convertirse en el Rey de los Piratas.',                                                                                                  'Aventura, Fantasía, Comedia',          'https://cdn.myanimelist.net/images/manga/2/253146l.jpg', 'https://cdn.myanimelist.net/images/manga/2/253146l.jpg', 1, 1110, 9.5, 'En emisión', '2026-05-30 17:13:14'),
(3, 'Jujutsu Kaisen',    'Gege Akutami',     'Yuji Itadori se une a una organización secreta de hechiceros para matar a Ryomen Sukuna, el Rey de las Maldiciones.',                                                                                                                    'Acción, Sobrenatural, Horror',         '/static/img/Jujutsu.jpg',                                '/static/img/Jujutsu.jpg',                                0, 266,  9.3, 'Completo',   '2026-05-30 17:13:14'),
(4, 'Attack on Titan',   'Hajime Isayama',   'En un mundo donde la humanidad vive rodeada de muros para protegerse de los titanes, Eren Jaeger jura destruir a todos los titanes.',                                                                                                      'Acción, Drama, Misterio',              'https://cdn.myanimelist.net/images/manga/2/37846l.jpg',  'https://cdn.myanimelist.net/images/manga/2/37846l.jpg',  0, 139,  9.7, 'Completo',   '2026-05-30 17:13:14'),
(5, 'My Hero Academia',  'Kōhei Horikoshi',  'En un mundo donde la mayoría posee superpoderes llamados Quirks, Izuku Midoriya nació sin ninguno pero sueña con convertirse en el mejor héroe.',                                                                                          'Acción, Superhéroes, Escolar',         'https://cdn.myanimelist.net/images/manga/1/209370l.jpg', 'https://cdn.myanimelist.net/images/manga/1/209370l.jpg', 1, 430,  8.9, 'Completo',   '2026-05-30 17:13:14'),
(6, 'Chainsaw Man',      'Tatsuki Fujimoto', 'Denji es un joven cazador de demonios en deuda que fusiona su cuerpo con su demonio perro Pochita, adquiriendo poderes de motosierra.',                                                                                                    'Acción, Horror, Sobrenatural',         'https://cdn.myanimelist.net/images/manga/3/216464l.jpg', 'https://cdn.myanimelist.net/images/manga/3/216464l.jpg', 0, 197,  9.4, 'En emisión', '2026-05-30 17:13:14'),
(7, 'Naruto',            'Masashi Kishimoto','Naruto Uzumaki, un joven ninja con el sueño de convertirse en Hokage, el líder de su aldea, carga con el espíritu del zorro de nueve colas.',                                                                                              'Acción, Aventura, Artes marciales',    'https://cdn.myanimelist.net/images/manga/3/117681l.jpg', 'https://cdn.myanimelist.net/images/manga/3/117681l.jpg', 1, 700,  9.0, 'Completo',   '2026-05-30 17:13:14'),
(8, 'Tokyo Revengers',   'Ken Wakui',        'Takemichi Hanagaki viaja al pasado para salvar a su ex novia de morir a manos de una peligrosa banda de delincuentes.',                                                                                                                    'Acción, Drama, Viaje en el tiempo',    '/static/img/Tokyio.jpg',                                 '/static/img/Tokyio.jpg',                                 0, 278,  8.7, 'Completo',   '2026-05-30 17:13:14'),
(9, 'My Happy Marriage', 'Akumi Agitogi',    'Una joven infeliz de que viene de una familia abusiva es casada con un temible y frío comandante del ejército. Pero cuando ambos se conocen mejor, el amor puede tener una oportunidad.',                                                   'Romance, Drama, Fantasía',             '/static/img/myhappymarriage.jpg',                        '/static/img/myhappymarriage.jpg',                        0, 33,   9.0, 'En emisión', '2026-05-30 17:13:14');

-- Capítulos (5 por manga, 45 total)
INSERT INTO capitulos (id, manga_id, numero, titulo, paginas, fecha_pub) VALUES
( 1,1,1,'Capítulo 1',22,'2026-05-30 17:13:14'), ( 2,1,2,'Capítulo 2',22,'2026-05-30 17:13:14'),
( 3,1,3,'Capítulo 3',22,'2026-05-30 17:13:14'), ( 4,1,4,'Capítulo 4',22,'2026-05-30 17:13:14'),
( 5,1,5,'Capítulo 5',22,'2026-05-30 17:13:14'), ( 6,2,1,'Capítulo 1',22,'2026-05-30 17:13:14'),
( 7,2,2,'Capítulo 2',22,'2026-05-30 17:13:14'), ( 8,2,3,'Capítulo 3',22,'2026-05-30 17:13:14'),
( 9,2,4,'Capítulo 4',22,'2026-05-30 17:13:14'), (10,2,5,'Capítulo 5',22,'2026-05-30 17:13:14'),
(11,3,1,'Capítulo 1',22,'2026-05-30 17:13:14'), (12,3,2,'Capítulo 2',22,'2026-05-30 17:13:14'),
(13,3,3,'Capítulo 3',22,'2026-05-30 17:13:14'), (14,3,4,'Capítulo 4',22,'2026-05-30 17:13:14'),
(15,3,5,'Capítulo 5',22,'2026-05-30 17:13:14'), (16,4,1,'Capítulo 1',22,'2026-05-30 17:13:14'),
(17,4,2,'Capítulo 2',22,'2026-05-30 17:13:14'), (18,4,3,'Capítulo 3',22,'2026-05-30 17:13:14'),
(19,4,4,'Capítulo 4',22,'2026-05-30 17:13:14'), (20,4,5,'Capítulo 5',22,'2026-05-30 17:13:14'),
(21,5,1,'Capítulo 1',22,'2026-05-30 17:13:14'), (22,5,2,'Capítulo 2',22,'2026-05-30 17:13:14'),
(23,5,3,'Capítulo 3',22,'2026-05-30 17:13:14'), (24,5,4,'Capítulo 4',22,'2026-05-30 17:13:14'),
(25,5,5,'Capítulo 5',22,'2026-05-30 17:13:14'), (26,6,1,'Capítulo 1',22,'2026-05-30 17:13:14'),
(27,6,2,'Capítulo 2',22,'2026-05-30 17:13:14'), (28,6,3,'Capítulo 3',22,'2026-05-30 17:13:14'),
(29,6,4,'Capítulo 4',22,'2026-05-30 17:13:14'), (30,6,5,'Capítulo 5',22,'2026-05-30 17:13:14'),
(31,7,1,'Capítulo 1',22,'2026-05-30 17:13:14'), (32,7,2,'Capítulo 2',22,'2026-05-30 17:13:14'),
(33,7,3,'Capítulo 3',22,'2026-05-30 17:13:14'), (34,7,4,'Capítulo 4',22,'2026-05-30 17:13:14'),
(35,7,5,'Capítulo 5',22,'2026-05-30 17:13:14'), (36,8,1,'Capítulo 1',22,'2026-05-30 17:13:14'),
(37,8,2,'Capítulo 2',22,'2026-05-30 17:13:14'), (38,8,3,'Capítulo 3',22,'2026-05-30 17:13:14'),
(39,8,4,'Capítulo 4',22,'2026-05-30 17:13:14'), (40,8,5,'Capítulo 5',22,'2026-05-30 17:13:14'),
(41,9,1,'Capítulo 1',22,'2026-05-30 17:13:14'), (42,9,2,'Capítulo 2',22,'2026-05-30 17:13:14'),
(43,9,3,'Capítulo 3',22,'2026-05-30 17:13:14'), (44,9,4,'Capítulo 4',22,'2026-05-30 17:13:14'),
(45,9,5,'Capítulo 5',22,'2026-05-30 17:13:14');

-- Favoritos e historial
INSERT INTO favoritos (id, usuario_id, manga_id, fecha) VALUES
(1, 2, 1, '2026-05-30 17:27:45');

INSERT INTO historial (id, usuario_id, manga_id, ultimo_capitulo, ultima_lectura) VALUES
(1, 2, 7, 1, '2026-05-30 17:25:04'),
(2, 2, 1, 1, '2026-05-30 17:28:00');

-- ============================================================
-- PASO 4 ─ Verificar (ejecuta esto al final para confirmar)
-- ============================================================
-- SELECT 'usuarios' AS tabla, COUNT(*) AS filas FROM usuarios
-- UNION ALL SELECT 'mangas',   COUNT(*) FROM mangas
-- UNION ALL SELECT 'capitulos',COUNT(*) FROM capitulos
-- UNION ALL SELECT 'favoritos',COUNT(*) FROM favoritos
-- UNION ALL SELECT 'historial', COUNT(*) FROM historial;
