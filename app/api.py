# Importiert die Flask-Anwendung aus der app und die Modelle User und Spiele
from app import app
from app.models import User, Spiele
# Importiert die jsonify-Funktion, um Daten in JSON umzuwandeln
from flask import jsonify
# Importiert HTTPBasicAuth für die Implementierung der Basis-Authentifizierung
from flask_httpauth import HTTPBasicAuth

# Erstellt eine Instanz der HTTPBasicAuth zur Verwaltung der Authentifizierung
auth = HTTPBasicAuth()

# Definiert ein Wörterbuch mit Benutzernamen und Passwörtern für die API-Authentifizierung
users = {
    "admin": "api123",  # Admin-Benutzer
    "user": "api123"    # Normaler Benutzer
}

# Authentifizierungsfunktion: Überprüft den Benutzernamen und gibt das zugehörige Passwort zurück
@auth.get_password
def get_password(username):
    if username in users:
        # Gibt das Passwort zurück, wenn der Benutzername gefunden wurde
        return users.get(username)
    # Gibt None zurück, wenn der Benutzername nicht vorhanden ist
    return None

# Definiert eine API-Route, um alle Benutzer abzurufen, geschützt durch Basic Auth
@app.route('/api/users', methods=['GET'])
@auth.login_required  # Stellt sicher, dass nur authentifizierte Benutzer auf die Route zugreifen können
def get_users():
    # Ruft alle Benutzer aus der Datenbank ab und gibt sie im JSON-Format zurück
    data = User.to_collection()
    return jsonify(data)

# Definiert eine API-Route, um einen bestimmten Benutzer anhand seiner ID abzurufen, geschützt durch Basic Auth
@app.route('/api/users/<int:id>', methods=['GET'])
@auth.login_required  # Stellt sicher, dass nur authentifizierte Benutzer auf die Route zugreifen können
def get_user(id):
    # Ruft den Benutzer mit der angegebenen ID ab und gibt seine Daten im JSON-Format zurück
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

# Definiert eine API-Route, um alle Spiele abzurufen, geschützt durch Basic Auth
@app.route('/api/spiele', methods=['GET'])
@auth.login_required  # Stellt sicher, dass nur authentifizierte Benutzer auf die Route zugreifen können
def get_spiele():
    # Ruft alle Spiele aus der Datenbank ab und gibt sie im JSON-Format zurück
    data = Spiele.to_collection()
    return jsonify(data)

# Fehlerbehandlung für unautorisierte Anfragen: Gibt einen Fehler im JSON-Format zurück
@auth.error_handler
def unauthorized():
    # Gibt eine Fehlermeldung im JSON-Format und den HTTP-Statuscode 403 zurück
    return jsonify({'error': 'Unautorisierten Anfragen'}), 403
