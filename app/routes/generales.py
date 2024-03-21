from ..app import app, db
from flask import Flask, render_template, request, abort, flash, jsonify
from sqlalchemy import or_
import geojson
from ..models.georisques import Etablissements, Departements, Polluants
from ..models.formulaires import Recherche

@app.route("/")
def accueil():
     return render_template("pages/accueil.html", sous_titre="Accueil")

@app.route("/test/<int:etablissement_id>")
def etablissement_detail(etablissement_id):
    etablissement = Etablissements.query.get(etablissement_id)
    return render_template("pages/test.html", etablissement=etablissement)


@app.route("/etablissements")
@app.route("/etablissements/<int:page>")
def etablissements(page=1):
    return render_template("pages/etablissements.html",
        sous_titre="Etablissements", 
        etablissements= Etablissements.query.order_by(Etablissements.nom).paginate(page=page, per_page=app.config["ETABLISSEMENTS_PER_PAGE"]))

@app.route("/etablissements/<string:nom_etablissement>")
def un_etablissement(nom_etablissement:str):
    
    return render_template("pages/un_etablissement.html", 
        sous_titre=nom_etablissement, 
        donnees= Etablissements.query.filter(Etablissements.nom == nom_etablissement).first())


@app.route("/departements")
@app.route("/departements/<int:page>")
def departements(page=1):
    etablissements_par_departement = {}

    for etablissement in Etablissements.query.all():
        departement = Departements.query.filter_by(id=etablissement.departement).first()
        if departement.nom in etablissements_par_departement:
            etablissements_par_departement[departement.nom].append(etablissement)
        else:
            etablissements_par_departement[departement.nom] = [etablissement]

    return render_template("pages/departements.html",
        sous_titre="Départements",
        donnees=Departements.query.order_by(Departements.nom).paginate(page=page, per_page=app.config["DPT_PER_PAGE"]),
        donnees_generales=etablissements_par_departement, page=page)

        
@app.route("/departements/<string:nom_departement>")
def un_departement(nom_departement):
    page=request.args.get('page', 1, type=int)
    departement_x = Departements.query.filter_by(nom=nom_departement).first()

    etablissements_departement = Etablissements.query.filter_by(departement=departement_x.id).order_by(Etablissements.nom).paginate(page=page, per_page=app.config["DPT_PER_PAGE"])
    return render_template("pages/un_departement.html", sous_titre=nom_departement, donnees=etablissements_departement, nom_departement=nom_departement)
    

@app.route("/polluants")
@app.route("/polluants/<int:page>")
def polluants(page=1):
    etablissement_par_polluant = {}

    for etablissement in Etablissements.query.all():
        for polluant in etablissement.polluant:
            if polluant.nom in etablissement_par_polluant:
                if etablissement.nom not in etablissement_par_polluant[polluant.nom]:
                    etablissement_par_polluant[polluant.nom].append(etablissement.nom)
            else:
                etablissement_par_polluant[polluant.nom] = [etablissement.nom]
    
    return render_template("pages/polluants.html",
        sous_titre="Polluants",
        donnees=Polluants.query.paginate(page=page, per_page=app.config["POLLUANT_PER_PAGE"]),
        donnees_generales=etablissement_par_polluant)


@app.route("/polluants/<string:nom_polluant>")
def un_polluant(nom_polluant):
    page = request.args.get('page', 1, type=int)
    polluant_x = Polluants.query.filter_by(nom=nom_polluant).first()
    etablissements_polluant = Etablissements.query.filter(Etablissements.polluant.contains(polluant_x)).order_by(Etablissements.nom).paginate(page=page, per_page=app.config["POLLUANT_PER_PAGE"])
    return render_template("pages/un_polluant.html", sous_titre=nom_polluant, donnees=etablissements_polluant)


@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    chaine = request.args.get("chaine", None)
    try: 
        if chaine:
            resultats = Etablissements.query.filter(
                Etablissements.commune.ilike("%"+chaine+"%")
            ).order_by(Etablissements.nom).paginate(page=page, per_page=app.config["ETABLISSEMENTS_PER_PAGE"])
            
        else:
            resultats = None
            
        # Vérifier si chaine est None avant de la concaténer avec une chaîne
        sous_titre = "Recherche | Commune : " + (chaine if chaine else "")
        
        return render_template("pages/resultats_recherche_etablissements.html", 
                sous_titre=sous_titre, 
                donnees=resultats,
                requete=chaine)
    
    except Exception as e:
        print(e)
        abort(500)

@app.route("/recherche", methods=['GET', 'POST'])
def recherche():
    form = Recherche() 

    requete = None

    donnees = []

    try:
        if form.validate_on_submit():
            nom_commune = request.form.get("nom_commune", None)
            code_postal = request.form.get("code_postal", None)

            if nom_commune or code_postal:
                query = Etablissements.query

                if nom_commune:
                    query = query.filter(Etablissements.commune.ilike("%"+nom_commune.lower()+"%"))
                    requete = nom_commune

                if code_postal:
                    query = query.filter(Etablissements.code_postal.ilike("%"+code_postal+"%"))
                    requete=code_postal
                
                donnees = query.order_by(Etablissements.commune).all()
                
                form.nom_commune.data = nom_commune
                form.code_postal.data = code_postal
            flash("La recherche a été effectuée avec succès", "info")
    except Exception as e:
        flash("La recherche a rencontré une erreur "+ str(e), "info")

    return render_template("pages/resultats_recherche.html", 
            sous_titre= "Recherche" , 
            donnees=donnees,
            form=form,
            requete=requete)


@app.route("/autocompletion")
@app.route("/autocompletion/<string:chaine>")
def autocompletion(chaine=None):
    try: 
        query = Etablissements.query

        if chaine:
            query = query.filter(Etablissements.commune.ilike("%"+chaine.lower()+"%"))
        
        donnees = [r.commune for r in query.all()]
    except Exception as e:
        print(e)
        donnees = []
    return donnees


@app.route('/carte')
def carte():
    # Création d'une liste pour stocker les données des marqueurs GeoJSON
    donnees = []

    # Appel des données contenues dans Etablissements
    for etablissement in Etablissements.query.all():
        # Vérifier si les coordonnées de latitude et de longitude sont disponibles
        if etablissement.latitude != "" and etablissement.longitude != "":
            # Création des propriétés de l'établissement
            champs = {
                "nom": etablissement.nom if etablissement.nom is not None else "Nom_par_défaut",
                "latitude": etablissement.latitude,
                "longitude": etablissement.longitude,
            }

            # Création du point GeoJSON
            localisation = geojson.Point((etablissement.latitude, etablissement.longitude))

            # Création du marqueur du point GeoJSON
            marqueur = geojson.Feature(
                geometry=localisation,
                properties=champs
            )

            # Ajout du marqueur à la liste des marqueurs créés
            donnees.append(marqueur)

    # Création de la collection de points GeoJSON
    feature_collection = geojson.FeatureCollection(donnees)
    
    return render_template('pages/carte.html', etablissements=feature_collection)

# BAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRIEEEEEEEEEEEEEEEEEEEEEEEEEREEEEEEEEEEEEEEEEEEEEEEEE




# Convertir les établissements en GeoJSON


    # Liste de sites géolocalisés
    # sites = [
    #     {"name": "Site 1", "location": [48.8566, 2.3522]},  # Exemple de coordonnées (Paris)
    #     {"name": "Site 2", "location": [51.5074, -0.1278]},  # Exemple de coordonnées (Londres)
    #     # Ajoutez d'autres sites avec leurs coordonnées
    # ]
    
    # return render_template('pages/carte.html', sites=sites)


    # code_postal = request.form.get("code_postal", None)

    # sites = {}

    # for etablissement in Etablissements.query.all():
    #     name = Departements.query.filter_by(id=etablissement.departement).first()
    #     if departement.nom in sites:
    #         sites[departement.nom].append(etablissement)
    #     else:
    #         sites[departement.nom] = [etablissement]