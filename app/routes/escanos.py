from flask import Blueprint, jsonify, request
from app.db import supabase

escanos_bp = Blueprint('escanos', __name__)

@escanos_bp.route("/escanos/<int:eleccion_id>", methods=["GET"])
def obtener_escanos(eleccion_id):
    data = supabase.table("escano").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

@escanos_bp.route("/escanos/eleccion/<int:eleccion_id>", methods=["GET"])
def get_escanos_por_eleccion(eleccion_id):
    data = supabase.table("escano").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)

@escanos_bp.route("/escanos", methods=["POST"])
def asignar_escanos():
    body = request.json
    data = supabase.table("escano").insert(body).execute()
    return jsonify(data.data)

@escanos_bp.route("/escanos/<int:escano_id>", methods=["DELETE"])
def eliminar_escano(escano_id):
    try:
        # Eliminar el registro de Supabase
        response = supabase.table("escano").delete().eq("id", escano_id).execute()
        
        # Verificar si se eliminó correctamente
        if len(response.data) > 0:
            return jsonify({"mensaje": "Escano eliminado correctamente", "id": escano_id}), 200
        else:
            return jsonify({"error": "Escano no encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500