# Importiert die Flask-Anwendung und die Datenbankinstanz aus dem app-Paket
from app import app, db

# Importiert die Modelle 'User' und 'Spiele' aus der Datei 'models.py' im app-Paket
from app.models import User, Spiele

# Definiert eine Funktion, die beim Starten einer Flask-Shell automatisch ausgeführt wird.
# Diese Funktion stellt sicher, dass die Datenbankinstanz sowie die 'User'- und 'Spiele'-Modelle
# im Shell-Kontext zur Verfügung stehen. Dadurch können sie direkt in der Shell verwendet werden,
# ohne dass sie jedes Mal manuell importiert werden müssen.
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Spiele': Spiele}