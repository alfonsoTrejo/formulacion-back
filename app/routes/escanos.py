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