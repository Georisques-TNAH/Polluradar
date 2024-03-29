# Manuel de l'application :

Notre application a pour objectif d'informer le public sur les installations rejetant des polluants en France. Les informations relatives aux établissements sont accessibles via la liste des établissements ou leurs regroupements par département ou par polluants rejetés. Une carte interactive des installations, réalisée grâce aux coordonnées présentes dans les données de la base Géorisques, permet de visualiser les installations présentes sur un territoire choisi et d'accéder directement aux fiches de ces établissements. Un moteur de recherche permet d'afficher la liste des établissements présents dans la commune recherchée.

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
Créer un fichier texte nommé `.env` au même niveau que le dossier `env` précédemment créé en collant la commande suivante dans votre terminal : 

    touch .env 
Coller les lignes suivantes dans le `.env` en les adaptant comme indiqué : 

    DEBUG=True
    SQLALCHEMY_DATABASE_URI=[URI DE LA BASE DE DONNÉES SQLITE]
    POLLUANT_PER_PAGE=10
    ETABLISSEMENT_PER_PAGE=10
    DPT_PER_PAGE=10
    SQLALCHEMY_ECHO=False
    WTF_CSRF_ENABLE=True
    SECRET_KEY=[CRÉER UNE CLÉ SECRÈTE]
Sur Linux, l'URI de la base de données est du type : sqlite://///[chemin personnel]/polluradar.db
### Etape 5 : Installer les requirements
Entrez la commande suivante dans votre terminal :

    source env/bin/activate
Puis la commande : 

    pip install -r requirements.txt

### Etape 6 : Lancer l'application
Entrez la commande suivante dans votre terminal :

    python3 run.py
Ceci lance l'application et un message du type `* Running on http://127.0.0.1:5000` s'affiche dans votre teminal. Cliquez sur le lien ou copiez/collez le dans votre navigateur. 

### Etape 7 : Quitter l'application 
Afin quitter l'application, effectuer un `ctrl+C` dans le terminal puis entrez `deactivate` dans votre terminal. 

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Cette application a été réalisée par [Selma Bensidhoum](https://github.com/SelmaKaina), [Mathilde Prades](https://github.com/Mathilde-prds) et [Ronan Vichot](https://github.com/RonanT8).
