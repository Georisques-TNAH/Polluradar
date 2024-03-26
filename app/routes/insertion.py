from flask import render_template, request, redirect, url_for, flash, logging
from ..app import app, db
from ..models.georisques import Etablissements
from ..models.formulaires import InsertionEtablissement



@app.route("/insertions/etablissement", methods=['GET', 'POST'])
def insertion_etablissement():
    """
    Route pour l'insertion d'un établissement dans la base de données.

    Methods:
        GET: Affiche le formulaire d'insertion.
        POST: Traite les données soumises et insère un nouvel établissement dans la base de données.

    Returns:
        str: Redirection vers la page d'accueil après une insertion réussie.
             Rendu du template d'insertion avec le formulaire et les messages flash en cas d'erreur.
    """
    # Création du formulaire d'insertion d'établissement
    form = InsertionEtablissement() 

    if form.validate_on_submit():
        # Récupérer les données du formulaire soumises
        id = form.id.data
        nom = form.nom.data
        siret = form.siret.data
        siren = form.siren.data
        adresse = form.adresse.data
        code_postal = form.code_postal.data
        code_ape = form.code_ape.data
        milieu_pollué = form.milieu_pollué.data
        secteur_na38 = form.secteur_na38.data
        produitLabel = form.produitLabel.data
        dateCreation = form.dateCreation.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        commune = form.commune.data
        departement = form.departement.data

        # Vérifier si les champs obligatoires sont remplis
        if nom and id and departement :
            try:
                # Créer un nouvel établissement avec les données fournies
                nouvel_etablissement = Etablissements(
                    id=id,
                    nom=nom,
                    siret=siret,
                    siren=siren,
                    adresse=adresse,
                    code_postal=code_postal,
                    code_ape=code_ape,
                    milieu_pollué=milieu_pollué,
                    secteur_na38=secteur_na38,
                    produitLabel=produitLabel,
                    dateCreation=dateCreation,
                    latitude=latitude,
                    longitude=longitude,
                    commune=commune,
                    departement=departement
                )

                # Ajouter le nouvel établissement à la session et enregistrer les modifications
                db.session.add(nouvel_etablissement)
                db.session.commit()

                # Afficher un message de succès et rediriger vers la page d'accueil
                flash("L'insertion de l'établissement {} s'est correctement déroulée.".format(nom), 'info')
                return redirect(url_for('accueil'))
            
            except Exception as e:
                # En cas d'erreur, annuler les modifications et afficher un message d'erreur
                db.session.rollback()
                flash("Une erreur s'est produite lors de l'insertion de l'établissement : {}".format(str(e)), 'error')
        else:
            # Si des champs obligatoires sont manquants, afficher un message d'erreur
            flash("Veuillez remplir tous les champs obligatoires.", 'error')
            return redirect(url_for('accueil'))

    # Rendre le template d'insertion avec le formulaire
    return render_template("pages/insertion_etablissement.html", 
                           sous_titre="Insertion établissement", 
                           form=form)


