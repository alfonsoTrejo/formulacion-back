from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase_client import supabase

app = Flask(__name__)
CORS(app)

@app.route("/elecciones", methods=["GET"])
def get_elecciones():
    data = supabase.table("eleccion").select("*").execute()
    return jsonify(data.data)

@app.route("/elecciones", methods=["POST"])
def crear_eleccion():
    body = request.json
    nueva = {
        "nombre": body["nombre"],
        "fecha_inicio": body["fecha_inicio"],
        "fecha_fin": body["fecha_fin"],
        "tipo": body["tipo"],
        "formula_id": body["formula_id"]
    }
    data = supabase.table("eleccion").insert(nueva).execute()
    return jsonify(data.data)

@app.route("/votos", methods=["POST"])
def registrar_voto():
    body = request.json
    voto = {
        "eleccion_id": body["eleccion_id"],
        "partido_id": body["partido_id"],
        "total_votos": body["total_votos"]
    }
    data = supabase.table("voto").insert(voto).execute()
    return jsonify(data.data)

@app.route("/escanos/<int:eleccion_id>", methods=["GET"])
def obtener_escanos(eleccion_id):
    data = supabase.table("escano").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

# FORMULAS
@app.route("/formulas", methods=["GET"])
def get_formulas():
    data = supabase.table("formula").select("*").execute()
    return jsonify(data.data)

@app.route("/formulas", methods=["POST"])
def crear_formula():
    body = request.json
    formula = {
        "nombre": body["nombre"],
        "descripcion": body.get("descripcion", ""),
        "logica_algoritmica": body.get("logica_algoritmica", "")
    }
    data = supabase.table("formula").insert(formula).execute()
    return jsonify(data.data)

@app.route("/formulas/<int:formula_id>", methods=["DELETE"])
def eliminar_formula(formula_id):
    try:
        # Eliminar el registro de Supabase
        response = supabase.table("formula").delete().eq("id", formula_id).execute()
        
        # Verificar si se eliminó correctamente
        if len(response.data) > 0:
            return jsonify({"mensaje": "Fórmula eliminada correctamente", "id": formula_id}), 200
        else:
            return jsonify({"error": "Fórmula no encontrada"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PARTIDOS
@app.route("/partidos", methods=["GET"])
def get_partidos():
    data = supabase.table("partido").select("*").execute()
    return jsonify(data.data)

@app.route("/partidos", methods=["POST"])
def crear_partido():
    body = request.json
    partido = {
        "nombre": body["nombre"],
        "siglas": body.get("siglas", ""),
        "logo_url": body.get("logo_url", "")
    }
    data = supabase.table("partido").insert(partido).execute()
    return jsonify(data.data)

# CANDIDATOS
@app.route("/candidatos", methods=["GET"])
def get_candidatos():
    data = supabase.table("candidato").select("*").execute()
    return jsonify(data.data)

@app.route("/candidatos", methods=["POST"])
def crear_candidato():
    body = request.json
    candidato = {
        "nombre": body["nombre"],
        "partido_id": body["partido_id"],
        "circunscripcion": body.get("circunscripcion", "")
    }
    data = supabase.table("candidato").insert(candidato).execute()
    return jsonify(data.data)

@app.route("/candidatos/partido/<int:partido_id>", methods=["GET"])
def get_candidatos_por_partido(partido_id):
    data = supabase.table("candidato").select("*").eq("partido_id", partido_id).execute()
    return jsonify(data.data)

# ELECCION DETALLE Y DELETE
@app.route("/elecciones/<int:id>", methods=["GET"])
def get_eleccion(id):
    data = supabase.table("eleccion").select("*").eq("id", id).single().execute()
    return jsonify(data.data)

@app.route("/elecciones/<int:id>", methods=["DELETE"])
def eliminar_eleccion(id):
    data = supabase.table("eleccion").delete().eq("id", id).execute()
    return jsonify({"eliminado": True})

# VOTOS por eleccion
@app.route("/votos/eleccion/<int:eleccion_id>", methods=["GET"])
def get_votos_por_eleccion(eleccion_id):
    data = supabase.table("voto").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

# ESCANOS por eleccion
@app.route("/escanos/eleccion/<int:eleccion_id>", methods=["GET"])
def get_escanos_por_eleccion(eleccion_id):
    data = supabase.table("escano").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

@app.route("/escanos", methods=["POST"])
def asignar_escanos():
    body = request.json
    data = supabase.table("escano").insert(body).execute()
    return jsonify(data.data)


@app.route('/auth/signOut', methods=['POST'])
def auth_sign_out():
    response = supabase.auth.sign_out()

@app.route('/auth/login', methods=['POST'])
def auth_login():
    data = request.get_json()
    print(data)
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


@app.route('/auth/verificar', methods=['POST'])
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
    

@app.route('/auth/singUp', methods=['POST'])
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

def verificar_token(token):
    try:
        user = response = supabase.auth.get_user(token)
        if user:
            return user
        return None
    except Exception as e:
        print(f"Error verificando token: {str(e)}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)
