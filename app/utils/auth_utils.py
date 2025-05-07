from app.db import supabase

def verificar_token(token):
    """
    Verifica la validez de un token de autenticación.
    
    Args:
        token (str): Token JWT a verificar
        
    Returns:
        dict: Información del usuario si el token es válido, None en caso contrario
    """
    try:
        user = supabase.auth.get_user(token)
        if user:
            return user
        return None
    except Exception as e:
        print(f"Error verificando token: {str(e)}")
        return None