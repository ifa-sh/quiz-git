# Importiert FlaskForm von flask_wtf, das die Erstellung von Formularen erleichtert
from flask_wtf import FlaskForm
# Importiert verschiedene Feldtypen (String, Passwort, Boolean, Integer, etc.) und Validierungen für die Formulare
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
# Importiert verschiedene Validatoren wie DataRequired, Email, EqualTo, NumberRange
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange
# Importiert die User
from app.models import User, Spiele

# Definiert das Login-Formular mit Feldern für den Benutzernamen, Passwort, "Angemeldet bleiben" und den Absenden-Button
class LoginForm(FlaskForm):
    # Das Username-Feld, das obligatorisch ausgefüllt werden muss
    username = StringField('Username', validators=[DataRequired()])
    # Das Passwort-Feld, ebenfalls obligatorisch
    password = PasswordField('Password', validators=[DataRequired()])
    # Ein optionales Feld, das den Benutzer angemeldet lässt, auch wenn er den Browser schliesst
    remember_me = BooleanField('Remember Me')
    # Der Button zum Absenden des Formulars
    submit = SubmitField('Sign In')

# Definiert das Registrierungsformular mit Feldern für Benutzername, E-Mail, Passwort und die Passwortbestätigung
class RegisterForm(FlaskForm):
    # Benutzername: Pflichtfeld
    username = StringField('Benutzername', validators=[DataRequired()])
    # E-Mail-Adresse: Pflichtfeld und muss ein gültiges E-Mail-Format haben
    email = StringField('Email', validators=[Email(), DataRequired()])
    # Passwort: Pflichtfeld
    password = PasswordField('Passwort', validators=[DataRequired()])
    # Passwortwiederholung: Pflichtfeld, muss mit dem Passwort übereinstimmen (EqualTo)
    password2 = PasswordField('Passwort wiederholen', validators=[DataRequired(), EqualTo('password')])
    # Absenden-Button
    submit = SubmitField('Registrieren')

    # Validiert, ob der eingegebene Benutzername bereits in der Datenbank existiert
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            # Fehlermeldung, wenn der Benutzername bereits existiert
            raise ValidationError('Bitte einen anderen Benutzernamen verwenden.')
    
    # Validiert, ob die eingegebene E-Mail-Adresse bereits registriert ist
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            # Fehlermeldung, wenn die E-Mail-Adresse bereits verwendet wird
            raise ValidationError('Bitte eine andere Email Adresse verwenden.')

# Formular zur Bearbeitung von Benutzerprofilen
class EditUserForm(FlaskForm):
    # Benutzername: Optionales Feld zur Aktualisierung des Benutzernamens
    username = StringField('Benutzername')
    # Lieblingsquiz: Ein Dropdown-Feld (SelectField) mit einer Auswahl an Lieblingsspielen, basierend auf der Spiele-Datenbank
    lieblingsquiz  = SelectField('Lieblingsquiz', coerce=int)
    # Absenden-Button
    submit = SubmitField('Ändern')

# Formular zur Erfassung neuer Spiele
class SpieleForm(FlaskForm):
    # Spielname: Pflichtfeld
    spielname = StringField('Quizname', validators=[DataRequired()])
    # Minimale Spieldauer: Pflichtfeld und muss zwischen 1 und 240 Minuten liegen
    dauer_min = IntegerField('Minimaldauer Min.', validators=[DataRequired(), NumberRange(1,240)])
    # Maximale Spieldauer: Pflichtfeld und muss zwischen 1 und 240 Minuten liegen
    dauer_max = IntegerField('Maximaldauer Min.', validators=[DataRequired(), NumberRange(1,240)])
    # Mindestanzahl an Spielern: Pflichtfeld und muss zwischen 1 und 20 Spielern liegen
    spieler_min = IntegerField('Mindestteilnehmer', validators=[DataRequired(), NumberRange(1,20)])
    # Maximale Anzahl an Spielern: Pflichtfeld und muss zwischen 1 und 20 Spielern liegen
    spieler_max = IntegerField('Höchstteilnehmer', validators=[DataRequired(), NumberRange(1,20)])
    # Absenden-Button
    submit = SubmitField('Speichern')
