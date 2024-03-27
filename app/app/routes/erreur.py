from ..app import app, db
from flask import render_template

@app.errorhandler(404)
def not_found_error(error):
    """
    Gère les erreurs 404 (Not Found) en affichant une page personnalisée.

    Args:
        error (Exception): L'erreur 404.

    Returns:
        tuple: Un tuple contenant le rendu du template 'erreurs/404.html' et le code d'erreur 404.
    """
    return render_template('erreurs/404.html'), 404

@app.errorhandler(500)
@app.errorhandler(503)
def internal_error(error):
    """
    Gère les erreurs 500 (Internal Server Error) et 503 (Service Unavailable) en affichant une page personnalisée
    et en effectuant un rollback de la session de base de données.

    Args:
        error (Exception): L'erreur 500 ou 503.

    Returns:
        tuple: Un tuple contenant le rendu du template 'erreurs/500.html' et le code d'erreur correspondant.
    """
    # Effectue un rollback de la session de base de données en cas d'erreur interne
    db.session.rollback()
    return render_template('erreurs/500.html'), error.code
