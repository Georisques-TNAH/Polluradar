import dotenv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config():
    DEBUG = os.environ.get("DEBUG")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    ETABLISSEMENTS_PER_PAGE = int(os.environ.get("ETABLISSEMENT_PER_PAGE"))
    POLLUANT_PER_PAGE = int(os.environ.get("POLLUANT_PER_PAGE"))
    DPT_PER_PAGE = int(os.environ.get("DPT_PER_PAGE"))