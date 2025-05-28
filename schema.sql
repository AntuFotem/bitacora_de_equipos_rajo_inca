-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    clave_hash TEXT NOT NULL
);

-- Tabla de CAEX
CREATE TABLE IF NOT EXISTS caex (
    id_caex INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

-- Insertar los 21 CAEX
INSERT INTO caex (nombre) VALUES
('CAEX-01'), ('CAEX-02'), ('CAEX-03'), ('CAEX-04'), ('CAEX-05'),
('CAEX-06'), ('CAEX-07'), ('CAEX-08'), ('CAEX-09'), ('CAEX-10'),
('CAEX-11'), ('CAEX-12'), ('CAEX-13'), ('CAEX-14'), ('CAEX-15'),
('CAEX-16'), ('CAEX-17'), ('CAEX-18'), ('CAEX-19'), ('CAEX-20'),
('CAEX-21');

-- Tabla de regletas
CREATE TABLE IF NOT EXISTS regletas (
    id_regleta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_caex INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    FOREIGN KEY (id_caex) REFERENCES caex(id_caex)
);

-- Puntos dentro de cada regleta
CREATE TABLE IF NOT EXISTS puntos_regleta (
    id_punto INTEGER PRIMARY KEY AUTOINCREMENT,
    id_regleta INTEGER NOT NULL,
    numero_punto TEXT NOT NULL,
    valor_ingresado TEXT,
    fecha_mod TEXT,
    FOREIGN KEY (id_regleta) REFERENCES regletas(id_regleta)
);

-- Tabla de tarjetas
CREATE TABLE IF NOT EXISTS tarjetas (
    id_tarjeta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_caex INTEGER NOT NULL,
    tipo_tarjeta TEXT NOT NULL,
    nombre_archivo TEXT NOT NULL,
    ruta_archivo TEXT NOT NULL,
    fecha_subida TEXT,
    FOREIGN KEY (id_caex) REFERENCES caex(id_caex)
);
