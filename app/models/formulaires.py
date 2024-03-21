from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField, IntegerField
from wtforms.validators import Optional
from ..models.georisques import Etablissements

class Recherche(FlaskForm):
    nom_commune = StringField("nom_commune", validators=[]) 
    code_postal = StringField('code_postal', validators=[])

class InsertionEtablissement(FlaskForm):
    nom = StringField('Nom de l\'établissement', validators=[])
    id = StringField('Identifiant de l\'établissement', validators=[])
    siret = StringField('SIRET', validators=[Optional()])
    siren = StringField('SIREN', validators=[Optional()])
    adresse = StringField('Adresse', validators=[Optional()])
    code_postal = StringField('Code Postal', validators=[Optional()])
    code_ape = StringField('Code APE', validators=[Optional()])
    milieu_pollué = SelectField('Milieu Pollué', choices=[('', ''),('Air','Air'),('Sol', 'Sol'),('Eau','Eau'),('Air, Eau', 'Air, Eau'),('Air, Sol','Air, Sol'),('Eau, Sol', 'Eau, Sol'),('Air, Eau, Sol','Air, Eau, Sol')])
    secteur_na38 = SelectField('Secteur NA38', choices=[('', ''), ('AZ Agriculture, sylviculture et pêche', 'Agriculture, sylviculture et pêche'), ('BZ Industries extractives', 'Industries extractives'), ('CA Fabrication de denrées alimentaires, de boissons et de produits à base de tabac', 'Fabrication de denrées alimentaires, de boissons et de produits à base de tabac'), ('CB Fabrication de textiles, industries de l’habillement, industrie du cuir et de la chaussure','Fabrication de textiles, industries de l’habillement, industrie du cuir et de la chaussure'),
       ('CC Travail du bois, industries du papier et imprimerie','Travail du bois, industries du papier et imprimerie'), ('CD Cokéfaction et raffinage', 'Cokéfaction et raffinage'), ('CE Industrie chimique', 'Industrie chimique')])
    produitLabel = StringField('Produit Label', validators=[Optional()])
    dateCreation = StringField('Date de Création', validators=[Optional()])
    latitude = FloatField('Latitude', validators=[Optional()])
    longitude = FloatField('Longitude', validators=[Optional()])
    commune = StringField('Commune', validators=[Optional()])
    departement = IntegerField('Departement', validators=[])
    submit = SubmitField('Insérer', validators=[])


class SuppressionEtablissement(FlaskForm):        
    nom = StringField('Nom de l\'établissement', validators=[])
    code_postal = SelectField('Code Postal', choices=[])

    def __init__(self, *args, **kwargs):
        super(SuppressionEtablissement, self).__init__(*args, **kwargs)
        self.code_postal.choices = self.get_code_postal_choices()

    def get_code_postal_choices(self):
        etablissements = Etablissements.query.all()
        return [(str(etablissement.code_postal), str(etablissement.code_postal)) for etablissement in etablissements]
