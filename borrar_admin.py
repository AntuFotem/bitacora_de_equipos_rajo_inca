import sqlite3

usuario = 'admin'

# Conexión a la base de datos
conn = sqlite3.connect('catastro_caex.db')
cursor = conn.cursor()

# Eliminar al usuario 'admin'
cursor.execute('DELETE FROM usuarios WHERE usuario = ?', (usuario,))
conn.commit()
conn.close()

print(f"✅ Usuario '{usuario}' eliminado correctamente.")
