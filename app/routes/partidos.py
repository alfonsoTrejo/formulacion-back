from flask import Blueprint, jsonify, request
from app.db import supabase

partidos_bp = Blueprint('partidos', __name__)

@partidos_bp.route("/partidos", methods=["GET"])
def get_partidos():
    data = supabase.table("partido").select("*").execute()
    return jsonify(data.data)

@partidos_bp.route("/partidos", methods=["POST"])
def crear_partido():
    body = request.json
    partido = {
        "nombre": body["nombre"],
        "siglas": body.get("siglas", ""),
        "logo_url": body.get("logo_url", "")
    }
    data = supabase.table("partido").insert(partido).execute()
    return jsonify(data.data)

@partidos_bp.route("/partidos/eleccion/<int:eleccion_id>", methods=["GET"])
def get_partidos_por_eleccion(eleccion_id):
    data = supabase.table("partido").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

@partidos_bp.route("/partidos/eleccion/<int:eleccion_id>/candidatos", methods=["GET"])
def get_partidos_con_candidatos(eleccion_id):
    data = supabase.table("partido").select("*").eq("eleccion_id", eleccion_id).execute()
    partidos = data.data
    for partido in partidos:
        candidatos_data = supabase.table("candidato").select("*").eq("partido_id", partido["id"]).execute()
        partido["candidatos"] = candidatos_data.data
    return jsonify(partidos)

@partidos_bp.route("/partidos/<int:partido_id>/candidatos", methods=["GET"])
def get_candidatos_por_partido(partido_id): 
    data = supabase.table("candidato").select("*").eq("partido_id", partido_id).execute()
    return jsonify(data.data)

@partidos_bp.route("/partidos/<int:partido_id>", methods=["PUT"])
def actualizar_partido(partido_id): 
    body = request.json
    partido = {
        "nombre": body["nombre"],
        "siglas": body.get("siglas", ""),
        "logo_url": body.get("logo_url", "")
    }
    data = supabase.table("partido").update(partido).eq("id", partido_id).execute()
    return jsonify(data.data)

@partidos_bp.route("/partidos/<int:partido_id>", methods=["DELETE"])
def eliminar_partido(partido_id):
    try:
        # Eliminar el registro de Supabase
        response = supabase.table("partido").delete().eq("id", partido_id).execute()
        
        # Verificar si se eliminó correctamente
        if len(response.data) > 0:
            return jsonify({"mensaje": "Partido eliminado correctamente", "id": partido_id}), 200
        else:
            return jsonify({"error": "Partido no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@partidos_bp.route("/partidos/<int:partido_id>", methods=["GET"])
def get_partido(partido_id):
    data = supabase.table("partido").select("*").eq("id", partido_id).single().execute()
    return jsonify(data.data)