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