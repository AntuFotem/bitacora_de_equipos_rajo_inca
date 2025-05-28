import sqlite3
from werkzeug.security import generate_password_hash

# Conexión a la base de datos
conn = sqlite3.connect('catastro_caex.db')
cursor = conn.cursor()

# Usuario y contraseña
usuario = 'admin'
clave_plana = 'kjis1UgA'
clave_hash = generate_password_hash(clave_plana)

# Insertar usuario
try:
    cursor.execute('INSERT INTO usuarios (usuario, clave_hash) VALUES (?, ?)', (usuario, clave_hash))
    conn.commit()
    print("✅ Usuario administrador creado con éxito.")
except sqlite3.IntegrityError:
    print("⚠️ El usuario ya existe.")
finally:
    conn.close()
