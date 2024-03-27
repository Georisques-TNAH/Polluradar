# Manuel de l'application :

L’objectif de l’application est de permettre aux utilisateurs de chercher les établissements industriels rejetant des polluants autour d’un lieu donné (ville + département), 
la recherche renvoie une carte avec des ronds de couleurs (en fonction de la dangerosité des polluants rejetés) et chaque rond est cliquable et renvoie à une fiche plus détaillée 
concernant l’entreprise, le type de polluants, le milieu pollué.

## Instructions pour un premier lancement :
Il est à noter que ces instructions s'adressent  à des utilisateurs de Linux. 

### Etape 1 : Installer Python (optionnel)
Si cela n'est pas déjà fait, il est nécessaire d'installer python sur votre machine en entrant la commande suivante dans votre terminal :

    sudo apt install python3

### Etape 2 : Cloner l'application
Entrez la commande suivante dans votre terminal : 

    git clone https://github.com/Georisques-TNAH/Polluradar.git

### Etape 3 : Créer un environnement virtuel
Entrez la commande suivante dans votre terminal : 

    virtualenv env -p python3

### Etape 4 : Saisir les variables d'environnement 
Créer un fichier texte nommé `.env` au même niveau que le dossier `env` précédemment créé. 
Coller les lignes suivantes dans le `.env` en les adaptant : 

    DEBUG=True
    SQLALCHEMY_DATABASE_URI=[URI DE LA BASE DE DONNÉES SQLITE SITUÉ DANS LE DOSSIER APP/DATA]
    POLLUANT_PER_PAGE=10
    ETABLISSEMENT_PER_PAGE=10
    DPT_PER_PAGE=10
    SQLALCHEMY_ECHO=False
    WTF_CSRF_ENABLE=True
    SECRET_KEY=[CRÉER UNE CLÉ SECRÈTE]

### Etape 5 : Installer les requierments (dépendances ?)
Entrez la commande suivante dans votre terminal :

    source env/Scripts/activate
Puis la commande : 

    pip install -r requirements.txt

### Etape 6 : Lancer l'application
Entrez la commande suivante dans votre terminal :

    python3 run.py
Ceci lance l'application et un message du type `* Running on http://127.0.0.1:5000` s'affiche dans votre teminal. Cliquez sur le lien ou copiez/collez le dans votre navigateur. 

### Etape 7 : Quitter l'application 
Afin quitter l'application, effectuer un `ctrl+C` dans le terminal puis entrez `deactivate` dans votre terminal. 

Cette application a été réalisée par [Selma Bensidhoum](https://github.com/SelmaKaina), [Mathilde Prades](https://github.com/Mathilde-prds) et [Ronan Vichot](https://github.com/RonanT8).
