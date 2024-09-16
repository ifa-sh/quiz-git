# Importiert das 'os'-Modul, um auf Umgebungsvariablen und Dateisystempfade zuzugreifen
import os

# Definiert den absoluten Pfad des Verzeichnisses, in dem sich die aktuelle Datei befindet.
# 'basedir' wird verwendet, um Pfade relativ zu diesem Verzeichnis zu erstellen.
basedir = os.path.abspath(os.path.dirname(__file__))

# Definiert eine Konfigurationsklasse 'Config', die von Flask verwendet wird
class Config(object):
    # 'SECRET_KEY' wird für die Sicherheit in Flask verwendet, z.B. für die Sitzungsverwaltung und CSRF-Schutz.
    # Hier wird versucht, die Umgebungsvariable 'SECRET_KEY' zu verwenden; wenn diese nicht vorhanden ist,
    # wird der Standardwert 'ein-geheimnis' verwendet.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ein-geheimnis'
    
    # SQLALCHEMY_DATABASE_URI definiert den Pfad zur Datenbank. Hier wird zuerst überprüft,
    # ob die Umgebungsvariable 'DATABASE_URL' gesetzt ist.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:ifa2024@localhost/quiz_db'
    
    # Verhindert die Verfolgung von Modifikationen an Objekten, um Speicher zu sparen, da dies
    # für die meisten Anwendungen nicht benötigt wird.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
