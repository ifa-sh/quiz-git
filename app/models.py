# Importiert die Datenbankinstanz und die Flask-Login-Erweiterung aus der app
from app import db, login
# UserMixin bietet Standardimplementierungen für Flask-Login
from flask_login import UserMixin
# Importiert Funktionen zur Passwort-Hash-Erstellung und -Überprüfung
from werkzeug.security import generate_password_hash, check_password_hash

# Definiert das User-Modell, das die Benutzer in der Datenbank repräsentiert
class User(UserMixin, db.Model):
    # Primärschlüssel: Einzigartige ID für jeden Benutzer
    id = db.Column(db.Integer, primary_key=True)
    # Benutzername: Einzigartig und indiziert für schnelle Suchen
    username = db.Column(db.String(64), index=True, unique=True)
    # E-Mail: Einzigartig und ebenfalls indiziert
    email = db.Column(db.String(128), index=True, unique=True)
    # Passwort-Hash: Speichert den verschlüsselten Hash des Passworts
    passwort_hash = db.Column(db.String(128))
    # Lieblingsquiz: Fremdschlüssel, der auf die Tabelle 'Spiele' verweist
    lieblingsquiz_id = db.Column(db.Integer, db.ForeignKey('spiele.spiel_id'))

    # Beziehungsdefinition: Verknüpft das Lieblingsquiz mit dem entsprechenden Eintrag in der 'Spiele'-Tabelle
    lieblingsquiz = db.relationship('Spiele')

    # Repräsentiert den Benutzer in der Konsole (nützlich für Debugging)
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # Methode zum Setzen des Passworts, speichert das Passwort als Hash
    def set_password(self, password):
        self.passwort_hash = generate_password_hash(password)
    
    # Methode zur Passwortüberprüfung, indem der gespeicherte Hash mit dem eingegebenen Passwort verglichen wird
    def check_password(self, password):
        return check_password_hash(self.passwort_hash, password)
    
    # Methode zur Rückgabe der Benutzerinformationen als Wörterbuch (nützlich für APIs)
    def to_dict(self):
        # Wenn kein Lieblingsquiz ausgewählt ist, wird eine entsprechende Nachricht angezeigt
        spiel = self.lieblingsquiz.spielname if self.lieblingsquiz else "Kein Lieblingsquiz ausgewählt"
        data = {
            'id': self.id,
            'Username': self.username,
            'Email': self.email,
            'Lieblingsquiz': spiel
        }
        return data
    
    # Statische Methode zur Rückgabe aller Benutzer als Sammlung von Wörterbüchern
    @staticmethod
    def to_collection():
        users = User.query.all()  # Ruft alle Benutzer aus der Datenbank ab
        data = {'items': [item.to_dict() for item in users]}  # Wandelt jeden Benutzer in ein Wörterbuch um
        return data

# Flask-Login benötigt diese Funktion, um einen Benutzer anhand seiner ID zu laden
@login.user_loader
def load_user(id):
    return User.query.get(int(id))  # Ruft den Benutzer anhand der ID aus der Datenbank ab

# Definiert das Spiele-Modell, das die Spiele in der Datenbank repräsentiert
class Spiele(db.Model):
    # Primärschlüssel: Einzigartige ID für jedes Spiel
    spiel_id = db.Column(db.Integer, primary_key=True)
    # Spielname: Einzigartig und indiziert für schnelle Suchen
    spielname = db.Column(db.String(64), index=True, unique=True)
    # Minimale Spieleranzahl
    spieler_min = db.Column(db.Integer)
    # Maximale Spieleranzahl
    spieler_max = db.Column(db.Integer)
    # Minimale Spieldauer in Minuten
    dauer_min = db.Column(db.Integer)
    # Maximale Spieldauer in Minuten
    dauer_max = db.Column(db.Integer)

    # Repräsentiert das Spiel in der Konsole (nützlich für Debugging)
    def __repr__(self):
        return '<Spiel {}>'.format(self.spielname)

    # Methode zur Rückgabe der Spieldetails 
    def to_dict(self):
        data = {
            'id': self.spiel_id,
            'Spielname': self.spielname,
            'Spieleranzahl': str(self.spieler_min) + " bis " + str(self.spieler_max),
            'Spieldauer': str(self.dauer_min) + " bis " + str(self.dauer_max) + " Minuten"
        }
        return data

    # Statische Methode zur Rückgabe aller Spiele als Sammlung von Wörterbüchern
    @staticmethod
    def to_collection():
        spiele = Spiele.query.all()  # Ruft alle Spiele aus der Datenbank ab
        data = {'items': [item.to_dict() for item in spiele]}  
        return data
