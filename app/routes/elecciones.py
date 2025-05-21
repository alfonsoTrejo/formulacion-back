from flask import Blueprint, jsonify, request
from app.db import supabase
from app.utils.auth_middleware import jwt_required

elecciones_bp = Blueprint('elecciones', __name__)

@elecciones_bp.route("/elecciones", methods=["GET"])
@jwt_required
def get_elecciones():
    data = supabase.table("eleccion").select("*").execute()
    return jsonify(data.data)

@elecciones_bp.route("/elecciones", methods=["POST"])
@jwt_required
def crear_eleccion():
    body = request.json
    nueva = {
        "nombre": body["nombre"],
        "fecha_inicio": body["fecha_inicio"],
        "fecha_fin": body["fecha_fin"],
        "numero_escano": body["numero_escano"],
        "formula_id": body["formula_id"]
    }
    data = supabase.table("eleccion").insert(nueva).execute()
    return jsonify(data.data)

@elecciones_bp.route("/elecciones/<int:id>", methods=["GET"])
@jwt_required
def get_eleccion(id):
    data = supabase.table("eleccion").select("*").eq("id", id).single().execute()
    return jsonify(data.data)

@elecciones_bp.route("/elecciones/<int:id>", methods=["DELETE"])
@jwt_required
def eliminar_eleccion(id):
    data = supabase.table("eleccion").delete().eq("id", id).execute()
    return jsonify({"eliminado": True})

@elecciones_bp.route("/elecciones/<int:id>", methods=["PUT"])
@jwt_required
def actualizar_eleccion(id):
    body = request.json
    eleccion = {
        "nombre": body["nombre"],
        "fecha_inicio": body["fecha_inicio"],
        "fecha_fin": body["fecha_fin"],
        "numero_escano": body["numero_escano"],
        "formula_id": body["formula_id"]
    }
    data = supabase.table("eleccion").update(eleccion).eq("id", id).execute()
    return jsonify(data.data)