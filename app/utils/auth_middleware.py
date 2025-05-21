from functools import wraps
from flask import request, jsonify
from app.utils.auth_utils import verificar_token

def jwt_required(f):
    """
    Decorador para proteger rutas con JWT
    Se utiliza como:
    
    @app.route('/ruta-protegida')
    @jwt_required
    def funcion_protegida():
        ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtener el token del encabezado Authorization
        auth_header = request.headers.get('Authorization')
        
        # Verificar que exista el encabezado y tenga el formato correcto
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'No se proporcionó un token de autenticación válido'}), 401
        
        # Extraer el token
        token = auth_header.split(" ")[1]
        
        # Verificar la validez del token
        usuario = verificar_token(token)
        if not usuario:
            return jsonify({'error': 'Token inválido o expirado'}), 401
        
        # Si el token es válido, continuar con la función original
        return f(*args, **kwargs)
    
    return decorated_function