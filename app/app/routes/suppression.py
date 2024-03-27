from ..app import app, db
from flask import render_template, request, flash
from ..models.formulaires import SuppressionEtablissement
from ..models.georisques import Etablissements, etablissements_polluants

@app.route("/suppressions/etablissement", methods=['GET', 'POST'])
def suppression_etablissement():
    """
    Route pour la suppression d'un établissement de la base de données.

    Methods:
        GET: Affiche le formulaire de suppression avec la liste des établissements existants.
        POST: Traite les données soumises et supprime l'établissement sélectionné de la base de données.

    Returns:
        str: Redirection vers la page d'accueil après une suppression réussie.
             Rendu du template de suppression avec le formulaire et les messages flash en cas d'erreur.
    """
    # Création du formulaire de suppression d'établissement
    form = SuppressionEtablissement()

    # Remplissage des choix du formulaire avec les noms et codes postaux des établissements existants
    form.nom.choices = [('','')] + [(etablissement.nom, etablissement.code_postal) for etablissement in Etablissements.query.all()]

    # Fonction pour supprimer un établissement de la base de données
    def delete_etablissement(nom):
        etablissement = Etablissements.query.filter_by(nom=nom).first()
        if etablissement:
            # Supprimer les entrées associées dans la table de liaison
            delete_statement = etablissements_polluants.delete().where(etablissements_polluants.c.etablissement == etablissement.id)
            db.session.execute(delete_statement)
            # Supprimer l'établissement lui-même
            db.session.delete(etablissement)
            db.session.commit()

    try:
        # Vérifier si le formulaire a été soumis
        if form.validate_on_submit():
            nom = request.form.get("nom", None)
            if nom:
                # Appeler la fonction de suppression avec le nom de l'établissement à supprimer
                delete_etablissement(nom)
                flash("La suppression de l'établissement s'est correctement déroulée", 'info')
            else:
                # Afficher un message d'erreur si aucun établissement n'a été spécifié
                flash("Il n'y a aucun établissement spécifié", "error")
    
    except Exception as e :
        # En cas d'erreur lors de la suppression, afficher un message d'erreur
        flash("Une erreur s'est produite lors de la suppression : " + str(e), "error")
    
    # Rendre le template de suppression avec le formulaire
    return render_template("pages/suppression_etablissement.html", 
            sous_titre= "Suppression établissement" , 
            form=form)
