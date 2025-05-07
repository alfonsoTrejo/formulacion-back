from flask import Blueprint, jsonify, request
from app.db import supabase

elecciones_bp = Blueprint('elecciones', __name__)

@elecciones_bp.route("/elecciones", methods=["GET"])
def get_elecciones():
    data = supabase.table("eleccion").select("*").execute()
    return jsonify(data.data)

@elecciones_bp.route("/elecciones", methods=["POST"])
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

@elecciones_bp.route("/elecciones/<int:id>", methods=["GET"])
def get_eleccion(id):
    data = supabase.table("eleccion").select("*").eq("id", id).single().execute()
    return jsonify(data.data)

@elecciones_bp.route("/elecciones/<int:id>", methods=["DELETE"])
def eliminar_eleccion(id):
    data = supabase.table("eleccion").delete().eq("id", id).execute()
    return jsonify({"eliminado": True})