from ..app import app, db
from flask import Flask, render_template, request, abort
from sqlalchemy import or_
from ..models.georisques import Etablissements, Departements, Polluants


@app.route("/")
def accueil():
     return render_template("pages/accueil.html", sous_titre="Accueil")

@app.route("/test/<int:etablissement_id>")
def etablissement_detail(etablissement_id):
    etablissement = Etablissements.query.get(etablissement_id)
    return render_template("pages/etablissement_detail.html", etablissement=etablissement)


@app.route("/etablissements")
@app.route("/etablissements/<int:page>")
def etablissements(page=1):
    return render_template("pages/etablissements.html",
        sous_titre="Etablissements", 
        etablissements= Etablissements.query.order_by(Etablissements.nom).paginate(page=page, per_page=app.config["ETABLISSEMENT_PER_PAGE"]))

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
        donnees=Departements.query.paginate(page=page, per_page=app.config["DPT_PER_PAGE"]),
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
    polluant_x = Polluants.query.filter_by(nom=nom_polluant).first()
    etablissements_polluant = Etablissements.query.filter(Etablissements.polluant.contains(polluant_x)).order_by(Etablissements.nom).all()
    return render_template("pages/un_polluant.html", sous_titre=nom_polluant, donnees=etablissements_polluant)
    

@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    commune_recherchee = request.args.get("commune", None)
    try: 
        if commune_recherchee:
            resultats = Etablissements.query.filter(
                Etablissements.commune.ilike("%"+commune_recherchee+"%")
            ).paginate(page=page, per_page=app.config["ETABLISSEMENT_PER_PAGE"])
        else:
            resultats = None
            
        # Vérifier si commune_recherchee est None avant de la concaténer avec une chaîne
        sous_titre = "Recherche | Commune : " + (commune_recherchee if commune_recherchee else "")
        
        return render_template("pages/resultats_recherche_etablissements.html", 
                sous_titre=sous_titre, 
                donnees=resultats,
                requete=commune_recherchee)
    
    except Exception as e:
        print(e)
        abort(500)



