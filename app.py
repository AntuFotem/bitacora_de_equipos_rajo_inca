from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

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
        public_id = f'regletas/caex{id_caex}/tb{i}'
        imagen_url = None
        detalle = None
        try:
            recurso = cloudinary.api.resource(public_id, context=True)
            imagen_url = recurso.get('secure_url')
            detalle = recurso.get('context', {}).get('custom', {}).get('detalle')
        except cloudinary.exceptions.NotFound:
            pass
        regletas.append({'id': i, 'nombre': nombre, 'imagen': imagen_url, 'detalle': detalle})

    return render_template('regletas.html', id_caex=id_caex, regletas=regletas)

@app.route('/caex/<int:id_caex>/regletas/<int:tb_id>/subir', methods=['POST'])
def subir_imagen_regleta(id_caex, tb_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    archivo = request.files.get('nueva_imagen')
    detalle = request.form.get('detalle', '')
    if archivo:
        public_id = f'regletas/caex{id_caex}/tb{tb_id}'
        cloudinary.uploader.upload(archivo, public_id=public_id, overwrite=True, context={"detalle": detalle})

    return redirect(url_for('ver_regletas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/regletas/<int:tb_id>/borrar', methods=['POST'])
def borrar_imagen_regleta(id_caex, tb_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    public_id = f'regletas/caex{id_caex}/tb{tb_id}'
    cloudinary.uploader.destroy(public_id)

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
        public_id = f'tarjetas/caex{id_caex}/tarjeta{idx}'
        imagen_url = None
        detalle = None
        try:
            recurso = cloudinary.api.resource(public_id, context=True)
            imagen_url = recurso.get('secure_url')
            detalle = recurso.get('context', {}).get('custom', {}).get('detalle')
        except cloudinary.exceptions.NotFound:
            pass
        tarjetas.append({'id': idx, 'nombre': nombre, 'imagen': imagen_url, 'detalle': detalle})

    return render_template('tarjetas.html', id_caex=id_caex, tarjetas=tarjetas)

@app.route('/caex/<int:id_caex>/tarjetas/<int:tarjeta_id>/subir', methods=['POST'])
def subir_imagen_tarjeta(id_caex, tarjeta_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    archivo = request.files.get('nueva_imagen')
    detalle = request.form.get('detalle', '')
    if archivo:
        public_id = f'tarjetas/caex{id_caex}/tarjeta{tarjeta_id}'
        cloudinary.uploader.upload(archivo, public_id=public_id, overwrite=True, context={"detalle": detalle})

    return redirect(url_for('ver_tarjetas', id_caex=id_caex))

@app.route('/caex/<int:id_caex>/tarjetas/<int:tarjeta_id>/borrar', methods=['POST'])
def borrar_imagen_tarjeta(id_caex, tarjeta_id):
    if 'usuario' not in session:
        return redirect(url_for('index'))

    public_id = f'tarjetas/caex{id_caex}/tarjeta{tarjeta_id}'
    cloudinary.uploader.destroy(public_id)

    return redirect(url_for('ver_tarjetas', id_caex=id_caex))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print("⚠️ No se encontró la base de datos.")
    app.run(debug=True)
