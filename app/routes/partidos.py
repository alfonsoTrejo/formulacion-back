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