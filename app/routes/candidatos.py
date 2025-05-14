from flask import Blueprint, jsonify, request
from app.db import supabase

candidatos_bp = Blueprint('candidatos', __name__)

@candidatos_bp.route("/candidatos", methods=["GET"])
def get_candidatos():
    data = supabase.table("candidato").select("*").execute()
    return jsonify(data.data)

@candidatos_bp.route("/candidatos", methods=["POST"])
def crear_candidato():
    body = request.json
    candidato = {
        "nombre": body["nombre"],
        "partido_id": body["partido_id"],
        "circunscripcion": body.get("circunscripcion", "")
    }
    data = supabase.table("candidato").insert(candidato).execute()
    return jsonify(data.data)

@candidatos_bp.route("/candidatos/partido/<int:partido_id>", methods=["GET"])
def get_candidatos_por_partido(partido_id):
    data = supabase.table("candidato").select("*").eq("partido_id", partido_id).execute()
    return jsonify(data.data)

@candidatos_bp.route("/candidatos/<int:candidato_id>", methods=["DELETE"])
def eliminar_candidato(candidato_id):
    try:
        # Eliminar el registro de Supabase
        response = supabase.table("candidato").delete().eq("id", candidato_id).execute()
        
        # Verificar si se eliminó correctamente
        if len(response.data) > 0:
            return jsonify({"mensaje": "Candidato eliminado correctamente", "id": candidato_id}), 200
        else:
            return jsonify({"error": "Candidato no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@candidatos_bp.route("/candidatos/<int:candidato_id>", methods=["GET"])
def get_candidato(candidato_id):
    data = supabase.table("candidato").select("*").eq("id", candidato_id).single().execute()
    return jsonify(data.data)