from flask import render_template, request, redirect, url_for, flash, logging
from ..app import app, db
from ..models.georisques import Etablissements
from ..models.formulaires import InsertionEtablissement



@app.route("/insertions/etablissement", methods=['GET', 'POST'])
def insertion_etablissement():
    form = InsertionEtablissement() 

    if form.validate_on_submit():
        # Récupérer les données du formulaire
        print('VALIDATE')
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
        departement=form.departement.data

        # Vérifier si les champs obligatoires sont remplis
        if nom and adresse and code_postal and secteur_na38 and siret and siren and code_ape and milieu_pollué and produitLabel and dateCreation and latitude and longitude and commune and departement :
            try:
                # Créer un nouvel établissement
                nouvel_etablissement = Etablissements(
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

                # Ajouter et enregistrer le nouvel établissement dans la base de données
                db.session.add(nouvel_etablissement)
                db.session.commit()

                # Afficher un message de succès
                flash("L'insertion de l'établissement {} s'est correctement déroulée.".format(nom), 'info')
                return redirect(url_for('accueil'))
            
            except Exception as e:
                # En cas d'erreur, annuler les modifications et afficher un message d'erreur
                db.session.rollback()
                flash("Une erreur s'est produite lors de l'insertion de l'établissement : {}".format(str(e)), 'error')
        else:
            flash("Veuillez remplir tous les champs obligatoires.", 'error')
            return redirect(url_for('accueil'))

    return render_template("pages/insertion_etablissement.html", 
                           sous_titre="Insertion établissement", 
                           form=form)





"""
@app.route("/insertions/ressource", methods=['GET', 'POST'])
def insertion_ressource():
    form = InsertionRessource() 

    try:
        if form.validate_on_submit():
            nom_res =  clean_arg(request.form.get("nom_res", None))
            id_res =  clean_arg(request.form.get("code_res", None))

            nouvelle_ressource = Resources(id=id_res, 
                name=nom_res)

            db.session.add(nouvelle_ressource)
            db.session.commit()

            flash("L'insertion de la ressource "+ nom_res + " s'est correctement déroulée", 'info')
    
    except Exception as e :
        flash("Une erreur s'est produite lors de l'insertion de " + nom_res + " : " + str(e), "error")

        db.session.rollback()
    
    return render_template("pages/insertion_ressource.html", 
            sous_titre= "Insertion ressource" , 
            form=form)

"""