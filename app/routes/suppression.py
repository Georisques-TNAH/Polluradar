from ..app import app, db
from flask import render_template, request, flash
from ..models.formulaires import SuppressionEtablissement
from ..models.georisques import Etablissements

@app.route("/suppressions/etablissement", methods=['GET', 'POST'])
def suppression_etablissement():
    form = SuppressionEtablissement()
    form.nom.choices = [('','')] + [(etablissement.id, etablissement.nom) for etablissement in Etablissements.query.all()]

    def delete_etablissement(id_etablissement):
        etablissement = Etablissements.query.get(id_etablissement)
        if etablissement:
            db.session.delete(etablissement)
            db.session.commit()

    try:
        if form.validate_on_submit():
            id_etablissement = request.form.get("nom_etablissement", None)
            if id_etablissement:
                delete_etablissement(id_etablissement)
                flash("La suppression de l'établissement s'est correctement déroulée", 'info')
            else:
                flash("Il n'y a aucun établissement spécifié", "error")
    
    except Exception as e :
        flash("Une erreur s'est produite lors de la suppression : " + str(e), "error")
    
    return render_template("pages/suppression_etablissement.html", 
            sous_titre= "Suppression établissement" , 
            form=form)
