from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'clave_super_segura_123'
DATABASE = 'catastro_caex.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    clave = request.form['clave']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
    conn.close()

    if user and check_password_hash(user['clave_hash'], clave):
        session['usuario'] = user['usuario']
        return redirect(url_for('menu'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('index'))

@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('menu.html', usuario=session['usuario'])

@app.route('/caex')
def listar_caex():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('caex_list.html')

@app.route('/caex/<int:id_caex>')
def detalle_caex(id_caex):
    if 'usuario' not in session:
        return redirect(url_for('index'))
    return render_template('caex_detail.html', id_caex=id_caex)

# ---------------------
# REGLETAS
# ---------------------

@app.route('/caex/<int:id_caex>/regletas')
def ver_regletas(id_caex):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    regletas = []
    for i in range(1, 36):
        nombre = f'TB{i}'
        ruta_img = f'static/regletas/caex{id_caex}/tb{i}.jpg'
        ruta_txt = f'data/regletas/caex{id_caex}/tb{i}.txt'
        imagen = f'/static/regletas/caex{id_caex}/tb{i}.jpg' if os.path.exists(ruta_img) else None
        detalle = ''
        if os.path.exists(ruta_txt):
            with open(ruta_txt, 'r', encoding='utf-8') as f:
                detalle = f.read()
        regletas.append({'id': i, 'nombre': nombre, 'imagen': imagen, 'detalle': detalle})

    return render_template('regletas.html', id_caex=id_caex, regletas=regletas)

@app.route('/caex/<int:id_caex>/regletas/<int:tb_id>/subir', methods=['POST'])
def subir_imagen_regleta(id_caex, tb_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    archivo = request.files.get('nueva_imagen')
    if archivo:
        ruta = f"static/regletas/caex{id_caex}"
        os.makedirs(ruta, exist_ok=True)
        archivo.save(os.path.join(ruta, f"tb{tb_id}.jpg"))

    return redirect(url_for('ver_regletas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/regletas/<int:tb_id>/borrar', methods=['POST'])
def borrar_imagen_regleta(id_caex, tb_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    ruta = f"static/regletas/caex{id_caex}/tb{tb_id}.jpg"
    if os.path.exists(ruta):
        os.remove(ruta)

    return redirect(url_for('ver_regletas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/regletas/<int:tb_id>/guardar_detalle', methods=['POST'])
def guardar_detalle_regleta(id_caex, tb_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    detalle = request.form.get('detalle', '')
    ruta = f"data/regletas/caex{id_caex}"
    os.makedirs(ruta, exist_ok=True)
    with open(os.path.join(ruta, f"tb{tb_id}.txt"), "w", encoding='utf-8') as f:
        f.write(detalle)

    return redirect(url_for('ver_regletas', id_caex=id_caex))

# ---------------------
# TARJETAS PSC / TCI
# ---------------------

@app.route('/caex/<int:id_caex>/tarjetas')
def ver_tarjetas(id_caex):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    tarjetas = []
    nombres = [f'PSC{i}' for i in range(1, 11)]
    nombres[0] = 'PSC CPU'
    nombres += [f'TCI{i}' for i in range(1, 11)]
    nombres[10] = 'TCI CPU'

    for idx, nombre in enumerate(nombres, start=1):
        archivo_img = f'static/tarjetas/caex{id_caex}/tarjeta{idx}.jpg'
        archivo_txt = f'data/tarjetas/caex{id_caex}/tarjeta{idx}.txt'
        imagen = f'/static/tarjetas/caex{id_caex}/tarjeta{idx}.jpg' if os.path.exists(archivo_img) else None
        detalle = ''
        if os.path.exists(archivo_txt):
            with open(archivo_txt, 'r', encoding='utf-8') as f:
                detalle = f.read()
        tarjetas.append({'id': idx, 'nombre': nombre, 'imagen': imagen, 'detalle': detalle})

    return render_template('tarjetas.html', id_caex=id_caex, tarjetas=tarjetas)

@app.route('/caex/<int:id_caex>/tarjetas/<int:tarjeta_id>/subir', methods=['POST'])
def subir_imagen_tarjeta(id_caex, tarjeta_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    archivo = request.files.get('nueva_imagen')
    if archivo:
        ruta = f"static/tarjetas/caex{id_caex}"
        os.makedirs(ruta, exist_ok=True)
        archivo.save(os.path.join(ruta, f"tarjeta{tarjeta_id}.jpg"))

    return redirect(url_for('ver_tarjetas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/tarjetas/<int:tarjeta_id>/borrar', methods=['POST'])
def borrar_imagen_tarjeta(id_caex, tarjeta_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    ruta = f"static/tarjetas/caex{id_caex}/tarjeta{tarjeta_id}.jpg"
    if os.path.exists(ruta):
        os.remove(ruta)

    return redirect(url_for('ver_tarjetas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/tarjetas/<int:tarjeta_id>/guardar_detalle', methods=['POST'])
def guardar_detalle_tarjeta(id_caex, tarjeta_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    detalle = request.form.get('detalle', '')
    ruta = f"data/tarjetas/caex{id_caex}"
    os.makedirs(ruta, exist_ok=True)
    with open(os.path.join(ruta, f"tarjeta{tarjeta_id}.txt"), "w", encoding='utf-8') as f:
        f.write(detalle)

    return redirect(url_for('ver_tarjetas', id_caex=id_caex))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print("⚠️ No se encontró la base de datos.")
    app.run(debug=True)
