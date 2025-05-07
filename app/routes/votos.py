from flask import Blueprint, jsonify, request
from app.db import supabase

votos_bp = Blueprint('votos', __name__)

@votos_bp.route("/votos", methods=["POST"])
def registrar_voto():
    body = request.json
    voto = {
        "eleccion_id": body["eleccion_id"],
        "partido_id": body["partido_id"],
        "total_votos": body["total_votos"]
    }
    data = supabase.table("voto").insert(voto).execute()
    return jsonify(data.data)

@votos_bp.route("/votos/eleccion/<int:eleccion_id>", methods=["GET"])
def get_votos_por_eleccion(eleccion_id):
    data = supabase.table("voto").select("*").eq("eleccion_id", eleccion_id).execute()
    return jsonify(data.data)