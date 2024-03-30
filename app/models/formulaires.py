from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import Optional
from ..models.georisques import Etablissements

# Formulaire de recherche pour les établissements
class Recherche(FlaskForm):
    nom_commune = StringField("nom_commune", validators=[]) 
    code_postal = StringField('code_postal', validators=[])

# Formulaire d'insertion pour les établissements
class InsertionEtablissement(FlaskForm):
    nom = StringField('Nom de l\'établissement', validators=[])
    id = StringField('Identifiant de l\'établissement', validators=[])
    siret = StringField('SIRET', validators=[Optional()])
    siren = StringField('SIREN', validators=[Optional()])
    adresse = StringField('Adresse', validators=[Optional()])
    code_postal = StringField('Code Postal', validators=[Optional()])
    code_ape = StringField('Code APE', validators=[Optional()])
    milieu_pollué = SelectField('Milieu Pollué', choices=[('', ''),('Air','Air'),('Sol', 'Sol'),('Eau','Eau'),('Air, Eau', 'Air, Eau'),('Air, Sol','Air, Sol'),('Eau, Sol', 'Eau, Sol'),('Air, Eau, Sol','Air, Eau, Sol')]) # Liste déroulante pour le milieu pollué
    secteur_na38 = SelectField('Secteur NA38', choices=[('', ''),
    ('AZ Agriculture, sylviculture et pêche', 'Agriculture, sylviculture et pêche'),
    ('BZ Industries extractives', 'Industries extractives'),
    ('CA Fabrication de denrées alimentaires, de boissons et de produits à base de tabac', 'Fabrication de denrées alimentaires, de boissons et de produits à base de tabac'),
    ('CB Fabrication de textiles, industries de l’habillement, industrie du cuir et de la chaussure', 'Fabrication de textiles, industries de l’habillement, industrie du cuir et de la chaussure'),
    ('CC Travail du bois, industries du papier et imprimerie', 'Travail du bois, industries du papier et imprimerie'),
    ('CD Cokéfaction et raffinage', 'Cokéfaction et raffinage'),
    ('CE Industrie chimique', 'Industrie chimique'),
    ('CF Industrie pharmaceutique', 'Industrie pharmaceutique'),
    ('CG Fabrication de produits en caoutchouc et en plastique ainsi que d’autres produits minéraux non métalliques', 'Fabrication de produits en caoutchouc et en plastique ainsi que d’autres produits minéraux non métalliques'),
    ('CH Métallurgie et fabrication de produits métalliques à l’exception des machines et des équipements', 'Métallurgie et fabrication de produits métalliques à l’exception des machines et des équipements'),
    ('CI Fabrication de produits informatiques, électroniques et optiques', 'Fabrication de produits informatiques, électroniques et optiques'),
    ('CJ Fabrication d’équipements électriques', 'Fabrication d’équipements électriques'),
    ('CK Fabrication de machines et équipements n.c.a.', 'Fabrication de machines et équipements n.c.a.'),
    ('CL Fabrication de matériels de transport', 'Fabrication de matériels de transport'),
    ('CM Autres industries manufacturières ; réparation et installation de machines et d’équipements', 'Autres industries manufacturières ; réparation et installation de machines et d’équipements'),
    ('DZ Production et distribution d’électricité, de gaz, de vapeur et d’air conditionné', 'Production et distribution d’électricité, de gaz, de vapeur et d’air conditionné'),
    ('EZ Production et distribution d’eau ; assainissement, gestion des déchets et dépollution', 'Production et distribution d’eau ; assainissement, gestion des déchets et dépollution'),
    ('FZ Construction', 'Construction'),
    ('GZ Commerce ; réparation d’automobiles et de motocycles', 'Commerce ; réparation d’automobiles et de motocycles'),
    ('HZ Transports et entreposage', 'Transports et entreposage'),
    ('IZ Hébergement et restauration', 'Hébergement et restauration'),
    ('JA Édition, audiovisuel et diffusion', 'Édition, audiovisuel et diffusion'),
    ('JB Télécommunications', 'Télécommunications'),
    ('JC Activités informatiques et services d’information', 'Activités informatiques et services d’information'),
    ('KZ Activités financières et d’assurance', 'Activités financières et d’assurance'),
    ('LZ Activités immobilières', 'Activités immobilières'),
    ('MA Activités juridiques, comptables, de gestion, d’architecture, d’ingénierie, de contrôle et d’analyses techniques', 'Activités juridiques, comptables, de gestion, d’architecture, d’ingénierie, de contrôle et d’analyses techniques'),
    ('MB Recherche-développement scientifique', 'Recherche-développement scientifique'),
    ('MC Autres activités spécialisées, scientifiques et techniques', 'Autres activités spécialisées, scientifiques et techniques'),
    ('NZ Activités de services administratifs et de soutien (dont : activités des agences de travail temporaire (intérim) ; activités des agences de voyage ; activités de sécurité privée ; nettoyage des bâtiments ; services d’aménagement paysager ; activités de centres d’appels)', 'Activités de services administratifs et de soutien (dont : activités des agences de travail temporaire (intérim) ; activités des agences de voyage ; activités de sécurité privée ; nettoyage des bâtiments ; services d’aménagement paysager ; activités de centres d’appels)'),
    ('OZ Administration publique', 'Administration publique'),
    ('PZ Enseignement', 'Enseignement'),
    ('QA Activités pour la santé humaine', 'Activités pour la santé humaine'),
    ('QB Hébergement médico-social et social et action sociale sans hébergement', 'Hébergement médico-social et social et action sociale sans hébergement'),
    ('RZ Arts, spectacles et activités récréatives', 'Arts, spectacles et activités récréatives'),
    ('SZ Autres activités de services', 'Autres activités de services'),
    ('TZ Activités des ménages en tant qu’employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre', 'Activités des ménages en tant qu’employeurs ; activités indifférenciées des ménages en tant que producteurs de biens et services pour usage propre'),
    ('UZ Activités extraterritoriales', 'Activités extraterritoriales')])  # Liste déroulante pour le secteur NA38
    produitLabel = StringField('Produit Label', validators=[Optional()])
    dateCreation = StringField('Date de Création', validators=[Optional()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    commune = StringField('Commune', validators=[Optional()])
    departement = IntegerField('Departement', validators=[])
    submit = SubmitField('Insérer', validators=[]) # Bouton de soumission du formulaire

# Formulaire de suppression pour les établissements
class SuppressionEtablissement(FlaskForm):        
    nom = StringField('Nom de l\'établissement', validators=[])
    code_postal = IntegerField('Code Postal', validators=[])


    