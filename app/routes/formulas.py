from flask import Blueprint, jsonify, request
from app.db import supabase

formulas_bp = Blueprint('formulas', __name__)

@formulas_bp.route("/formulas", methods=["GET"])
def get_formulas():
    data = supabase.table("formula").select("*").execute()
    return jsonify(data.data)

@formulas_bp.route("/formulas", methods=["POST"])
def crear_formula():
    body = request.json
    formula = {
        "nombre": body["nombre"],
        "descripcion": body.get("descripcion", ""),
        "logica_algoritmica": body.get("logica_algoritmica", "")
    }
    data = supabase.table("formula").insert(formula).execute()
    return jsonify(data.data)

@formulas_bp.route("/formulas/<int:formula_id>", methods=["DELETE"])
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
    
@formulas_bp.route("/formulas/<int:formula_id>", methods=["GET"])
def get_formula(formula_id):
    data = supabase.table("formula").select("*").eq("id", formula_id).single().execute()
    return jsonify(data.data)