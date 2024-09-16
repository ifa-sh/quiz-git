# Importiert das Flask-Framework für den Aufbau der Webanwendung
from flask import Flask
# Importiert Flask-Bootstrap zur Integration von Bootstrap für das Styling der Anwendung
from flask_bootstrap import Bootstrap
# Importiert SQLAlchemy zur Interaktion mit der Datenbank
from flask_sqlalchemy import SQLAlchemy
# Importiert Flask-Migrate zur Verwaltung von Datenbankmigrationen
from flask_migrate import Migrate
# Importiert Flask-Login zur Verwaltung der Benutzer-Authentifizierung
from flask_login import LoginManager
# Importiert die Konfigurationsklasse, um die Anwendungseinstellungen zu laden
from config import Config

# Initialisiert die Flask-Anwendung
app = Flask(__name__)
# Initialisiert Bootstrap zur Verwendung in der Anwendung
bootstrap = Bootstrap(app)
# Lädt die Konfigurationseinstellungen aus der Config-Klasse
app.config.from_object(Config)
# Initialisiert SQLAlchemy, um die Verbindung zur Datenbank herzustellen
db = SQLAlchemy(app)
# Initialisiert Flask-Migrate, um Datenbankmigrationen durchzuführen
migrate = Migrate(app, db)
# Initialisiert Flask-Login, um die Benutzer-Authentifizierung zu verwalten
login = LoginManager(app)
# Definiert den Endpunkt, auf den umgeleitet wird, wenn ein nicht authentifizierter Benutzer eine geschützte Route aufruft
login.login_view = 'login'

# Importiert die Routen, Modelle und API-Funktionen der Anwendung, um sie in die App zu integrieren
from app import routes, models, api
