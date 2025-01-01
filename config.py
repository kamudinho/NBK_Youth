import os
from dotenv import load_dotenv

# Indlæs miljøvariabler fra .env
load_dotenv()

# Miljøvariabler
DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

# Sikkerhedstjek
if not DATABASE_URL or not SECRET_KEY:
    raise ValueError("DATABASE_URL eller SECRET_KEY mangler i .env")

# Forbindelse til SQL Server
DB_DRIVER = "ODBC Driver 18 for SQL Server"
DB_SERVER = "127.0.0.1,4022"  # Hvis du har en lokal instans
DB_NAME = "NBK"
DB_USER = "sa"
DB_PASSWORD = os.getenv('DB_PASSWORD', 'default_password')  # Fallback hvis password mangler
DB_TRUST_SERVER_CERTIFICATE = "YES"


# Byg forbindelsesstrengen til SQL Server
SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER}&TrustServerCertificate={DB_TRUST_SERVER_CERTIFICATE}"

# Flask-konfiguration
class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
