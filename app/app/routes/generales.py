from ..app import app, db
from flask import Flask, render_template, request, abort, flash, jsonify
from sqlalchemy import or_, func, text
from ..models.georisques import Etablissements, Departements, Polluants
from ..models.formulaires import Recherche

@app.route("/")
def accueil():
    """
    Route pour afficher la page d'accueil.

    Returns:
        template: Template de la page d'accueil.
    """
    return render_template("pages/accueil.html", sous_titre="Accueil")

@app.route("/test/<int:etablissement_id>")
def etablissement_detail(etablissement_id):
    """
    Route pour afficher les détails d'un établissement.

    Args:
        etablissement_id (int): L'identifiant de l'établissement.

    Returns:
        template: Template pour afficher les détails de l'établissement.
    """
    etablissement = Etablissements.query.get(etablissement_id)
    return render_template("pages/test.html", etablissement=etablissement)

@app.route("/etablissements")
@app.route("/etablissements/<int:page>")
def etablissements(page=1):
    """
    Route pour afficher la liste des établissements.

    Args:
        page (int, optional): Le numéro de page pour la pagination. Par défaut 1.

    Returns:
        template: Template pour afficher la liste des établissements.
    """
    return render_template("pages/etablissements.html",
        sous_titre="Etablissements", 
        etablissements= Etablissements.query.order_by(Etablissements.nom).paginate(page=page, per_page=app.config["ETABLISSEMENTS_PER_PAGE"]))

@app.route("/etablissements/<string:nom_etablissement>")
def un_etablissement(nom_etablissement:str):
    """
    Route pour afficher les détails d'un établissement spécifique.

    Args:
        nom_etablissement (str): Le nom de l'établissement.

    Returns:
        template: Template pour afficher les détails de l'établissement.
    """
    return render_template("pages/un_etablissement.html", 
        sous_titre=nom_etablissement, 
        donnees= Etablissements.query.filter(Etablissements.nom == nom_etablissement).first())

@app.route("/departements")
@app.route("/departements/<int:page>")
def departements(page=1):
    """
    Route pour afficher la liste des départements.

    Args:
        page (int, optional): Le numéro de page pour la pagination. Par défaut 1.

    Returns:
        template: Template pour afficher la liste des départements.
    """
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
    """
    Route pour afficher les établissements d'un département spécifique.

    Args:
        nom_departement (str): Le nom du département.

    Returns:
        template: Template pour afficher les établissements du département.
    """
    page=request.args.get('page', 1, type=int)
    departement_x = Departements.query.filter_by(nom=nom_departement).first()

    etablissements_departement = Etablissements.query.filter_by(departement=departement_x.id).order_by(Etablissements.nom).paginate(page=page, per_page=app.config["DPT_PER_PAGE"])
    return render_template("pages/un_departement.html", sous_titre=nom_departement, donnees=etablissements_departement, nom_departement=nom_departement)

@app.route("/polluants")
@app.route("/polluants/<int:page>")
def polluants(page=1):
    """
    Route pour afficher la liste des polluants.

    Args:
        page (int, optional): Le numéro de page pour la pagination. Par défaut 1.

    Returns:
        template: Template pour afficher la liste des polluants.
    """
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
    """
    Route pour afficher les établissements liés à un polluant spécifique.

    Args:
        nom_polluant (str): Le nom du polluant.

    Returns:
        template: Template pour afficher les établissements liés au polluant.
    """
    page = request.args.get('page', 1, type=int)
    polluant_x = Polluants.query.filter_by(nom=nom_polluant).first()
    etablissements_polluant = Etablissements.query.filter(Etablissements.polluant.contains(polluant_x)).order_by(Etablissements.nom).paginate(page=page, per_page=app.config["POLLUANT_PER_PAGE"])
    return render_template("pages/un_polluant.html", sous_titre=nom_polluant, donnees=etablissements_polluant)


@app.route("/recherche_rapide")
@app.route("/recherche_rapide/<int:page>")
def recherche_rapide(page=1):
    """
    Route pour effectuer une recherche rapide.

    Args:
        page (int, optional): Le numéro de page pour la pagination. Par défaut 1.

    Returns:
        template: Template pour afficher les résultats de la recherche rapide.
    """
    chaine = request.args.get("chaine", None)
    try: 
        if chaine:
            # Effectuer une recherche basée sur la chaîne fournie
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
    """
    Route pour effectuer une recherche avancée.

    Returns:
        template: Template pour afficher les résultats de la recherche avancée.
    """
    form = Recherche() 

    requete = None

    donnees = []

    try:
        if form.validate_on_submit():
            # Récupérer les données du formulaire de recherche
            nom_commune = request.form.get("nom_commune", None)
            code_postal = request.form.get("code_postal", None)

            if nom_commune or code_postal:
                query = Etablissements.query

                if nom_commune:
                    # Filtrer par nom de commune si fourni
                    query = query.filter(Etablissements.commune.ilike("%"+nom_commune.lower()+"%"))
                    requete = nom_commune

                if code_postal:
                    # Filtrer par code postal si fourni
                    query = query.filter(Etablissements.code_postal.ilike("%"+code_postal+"%"))
                    requete = code_postal
                
                # Exécuter la requête et récupérer les résultats
                donnees = query.order_by(Etablissements.commune).all()
                
                # Pré-remplir le formulaire avec les valeurs de la recherche
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

@app.route("/autocompletion/<string:chaine>")
def autocompletion(chaine=None):
    """
    Route pour l'autocomplétion des communes.

    Args:
        chaine (str): La chaîne pour laquelle l'autocomplétion est effectuée.

    Returns:
        list: Liste des communes correspondant à la chaîne fournie.
    """
    try: 
        query_results = Etablissements.query

        if chaine:
            # Filtrer les résultats basés sur la chaîne fournie
            query_results = query_results.filter(Etablissements.commune.ilike(chaine+"%"))
        
        # Récupérer les communes correspondant à la requête
        donnees = [r.commune for r in query_results.all()]
        
        return donnees
    
    except Exception as e:
        print(e)
        return []

@app.route('/carte')
def carte():
    # Création d'une liste pour stocker les données des marqueurs
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

            # Ajout du marqueur à la liste des marqueurs créés
            donnees.append(champs)

    return render_template('pages/carte.html', donnees=donnees)

@app.route('/datavisualisations')
def datavisualisations():
    return render_template('pages/datavisualisations.html')

@app.route("/graph1", methods=['GET', 'POST'])
def graph1():
    return render_template("pages/graph1.html")

@app.route("/graph1_donnees", methods=['GET', 'POST'])
def graph1_donnees():
    total = db.session.query(func.count(Etablissements.id)).scalar()
    donnees_brutes = db.session.query(Etablissements.secteur_na38, func.count(Etablissements.id)) \
        .group_by(Etablissements.secteur_na38) \
        .order_by(func.count(Etablissements.id).desc()) \
        .limit(20)

    donnees = []

    for secteur_na38, occurrences in donnees_brutes:
        pourcentage = (occurrences / total) * 100
        donnees.append({
            "secteur": secteur_na38,
            "pourcentage": pourcentage
        })

    return jsonify(donnees)