from ..app import app, db

etablissements_polluants = db.Table(
    "etablissements_polluants",
    db.Column("etablissement", db.Integer, db.ForeignKey("etablissements.id"), primary_key=True, nullable=False),
    db.Column("polluant", db.Integer, db.ForeignKey("polluants.id"), primary_key=True, nullable=False)
)

class Etablissements(db.Model):
    __tablename__ = "etablissements"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    siret = db.Column(db.Integer, nullable=True)
    siren = db.Column(db.Integer, nullable=True)
    adresse = db.Column(db.String, nullable=False)
    code_ape = db.Column(db.String(5), nullable=False)
    milieu_pollué = db.Column(db.String(3), nullable=True)
    secteur_na38 = db.Column(db.String, nullable=False)
    produitLabel = db.Column(db.String, nullable=True)
    dateCreation = db.Column(db.DateTime, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    departement = db.relationship("Departements", db.ForeignKey('departements.id'))
    code_postal = db.relationship("Communes", db.ForeignKey('communes.id'))

    etablissements_polluants = db.relationship(
        'Polluants',
        secondary=etablissements_polluants,
        backref="etablissements",
        lazy="dynamic"
    )

    def __repr__(self):
        return '<Etablissements %r>' % self.nom
    
class Departements(db.Model):
    __tablename__ = "departements"
    id = db.Column(db.String, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    surface_km2 = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    votes_urgence_ecologie = db.Column(db.Float, nullable=False)
    votes_envie_d_europe_ecologique_et_sociale = db.Column(db.Float, nullable=False)
    votes_europe_ecologie_les_verts = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Departements %r>' % self.nom

class Polluants(db.Model):
    __tablename__ = "polluants"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    fiche_inrs = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<Polluants %r>' % self.nom
        
class Communes(db.Model):
    __tablename__ = "communes"
    id = db.Column(db.String(5), primary_key=True)
    nom = db.Column(db.String, nullabe=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)*

    departement = db.relationship("Departements", db.ForeignKey('departements.id'))

    def __repr__(self):
        return '<Communes %r>' % self.nom
