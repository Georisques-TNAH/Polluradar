from ..app import app, db
from flask import Flask, render_template, request
from ..models.georisques import Etablissements, Departements

@app.route("/")
def accueil():
     return render_template("pages/accueil.html", sous_titre="Accueil")


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
        for departement in str(etablissement.departement):   #cette ligne fait tout buguer pourtant elle me semble cohérente, l'erreur : int object is not iterable
            #erreur de int résolue mais ne change pas le pb je crois
            if Departements.nom in etablissements_par_departement:
                if etablissement.nom not in etablissements_par_departement[Departements.nom]: #De base departement.nom
                    etablissements_par_departement[Departements.nom].append(etablissement.nom)
            else:
                etablissements_par_departement[Departements.nom] = [etablissement.nom]

    return render_template("pages/departements.html",
        sous_titre="Départements",
        donnees=Departements.query.paginate(page=page, per_page=app.config["DPT_PER_PAGE"]),
        donnees_generales=etablissements_par_departement, page=page)

        
@app.route("/departements/<string:nom_departement>")
def un_departement(nom_departement):
    departement_x = Departements.query.filter(Departements.nom == nom_departement).first()

    return render_template("pages/un_departement.html", 
        sous_titre=nom_departement, 
        donnees= Etablissements.query.filter(Etablissements.departement.contains(departement_x)).order_by(Etablissements.nom).all(), nom_departement=departement_x.nom)
#pas sûre du departements dans Etablissements.departements.contains(departements)).

"""
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
    polluant = Polluants.query.filter(Polluants.nom == nom_polluant).first()

    return render_template("pages/un_polluant.html", 
        sous_titre=nom_polluant, 
        donnees= Etablissements.query.filter(Etablissements.polluant.contains(polluant)).order_by(Etablissements.nom).all())
"""
    #pas sûre du polluant 1 dans Etablissements.polluant.contains(polluant)).

