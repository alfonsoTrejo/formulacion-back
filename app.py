from flask import Flask
from flask_cors import CORS
from app.routes.elecciones import elecciones_bp
from app.routes.votos import votos_bp
from app.routes.escanos import escanos_bp
from app.routes.formulas import formulas_bp
from app.routes.partidos import partidos_bp
from app.routes.candidatos import candidatos_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(elecciones_bp)
    app.register_blueprint(votos_bp)
    app.register_blueprint(escanos_bp)
    app.register_blueprint(formulas_bp)
    app.register_blueprint(partidos_bp)
    app.register_blueprint(candidatos_bp)
    app.register_blueprint(auth_bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)