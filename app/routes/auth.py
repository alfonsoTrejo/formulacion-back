from flask import Blueprint, jsonify, request
from app.db import supabase
from app.utils.auth_utils import verificar_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/signOut', methods=['POST'])
def auth_sign_out():
    response = supabase.auth.sign_out()
    return jsonify({"mensaje": "Sesión cerrada exitosamente"}), 200

@auth_bp.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    email = data.get('email','')
    password = data.get('password','')

    if not email or not password:
        return jsonify({'Error': "Faltan credenciales"}), 400

    try:
        response = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if not response:
            raise ValueError(response)
        
        access_token = response.session.access_token

        # Devolver el mensaje junto con el JWT
        return jsonify({'Mensaje': 'Inicio de sesión exitoso', 'JWT': access_token}), 200
        
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@auth_bp.route('/auth/verificar', methods=['POST'])
def auth_verificar():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'Error': "No se proporcionó un token válido"}), 401

    token = auth_header.split(" ")[1]  # Extraer el token después de 'Bearer'
    
    # Verificar si el usuario está autenticado
    usuario = verificar_token(token)
    if not usuario:
        return jsonify({'Error': "Usuario no autenticado"}), 401

    return jsonify({'200': 'verificado'}), 200

@auth_bp.route('/auth/singUp', methods=['POST'])
def auth_sing_up():
    data = request.get_json()
    email = data.get('email','')
    password = data.get('password','')

    if not email or not password:
        return jsonify({'Error': "Faltan credenciales"}), 400

    try:
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
        })

        if not response:
            raise ValueError(response)

        return jsonify({'Mensaje': 'Registro exitoso'}), 201

    except Exception as e:
        return jsonify({'Error': str(e)}), 500