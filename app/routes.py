# Importiert notwendige Module und Funktionen aus Flask und der Applikation
from flask import render_template, flash, redirect, url_for, request
from app import app, db  # Flask-Anwendung und Datenbankinstanz aus app importieren
from app.forms import LoginForm, RegisterForm, SpieleForm, EditUserForm  # Formulare für Login, Registrierung, Spiel und Benutzerprofil
from app.models import User, Spiele  # Datenbankmodelle für User und Spiele importieren
from flask_login import login_user, current_user, logout_user, login_required  # Login-Management für Benutzerverwaltung
from werkzeug.urls import url_parse  # Hilfsfunktion, um URLs zu parsen

# Route für die Startseite ("/" oder "/index"), die nur für angemeldete Benutzer zugänglich ist
@app.route('/')
@app.route('/index')
@login_required  # Stellt sicher, dass die Route nur von angemeldeten Benutzern erreicht werden kann
def index():
    # Rendert die index.html-Seite mit dem Titel 'Quiz'
    return render_template('index.html', title='Quiz')

# Route für die Login-Seite, unterstützt GET- und POST-Anfragen
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Wenn der Benutzer bereits angemeldet ist, wird er zur Startseite weitergeleitet
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()  # Initialisiert das Login-Formular
    # Überprüft, ob das Formular korrekt ausgefüllt wurde
    if form.validate_on_submit():
        # Sucht nach einem Benutzer in der Datenbank, der mit dem eingegebenen Benutzernamen übereinstimmt
        user = User.query.filter_by(username=form.username.data).first()
        # Wenn der Benutzer nicht existiert oder das Passwort nicht übereinstimmt, wird eine Fehlermeldung angezeigt
        if user is None or not user.check_password(form.password.data):
            flash('Ungültiger Benutzername oder Passwort!')
            return redirect(url_for('login'))  # Leitet zurück zur Login-Seite
        # Loggt den Benutzer ein, wenn alles korrekt ist
        login_user(user, remember=form.remember_me.data)
        # Überprüft, ob der Benutzer zu einer bestimmten Seite weitergeleitet werden soll (z.B. nach Login-Umleitung)
        next_page = request.args.get('next')
        # Wenn keine gültige Weiterleitungsseite angegeben ist, wird die Startseite als Standard verwendet
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)  # Leitet den Benutzer zur nächsten Seite weiter
    # Rendert die Login-Seite mit dem Login-Formular
    return render_template('login.html', title='Login', form=form)

# Route zum Ausloggen des Benutzers
@app.route('/logout')
def logout():
    logout_user()  # Meldet den Benutzer ab
    return redirect(url_for('index'))  # Leitet den Benutzer zurück zur Startseite

# Route für die Registrierung von Benutzern, unterstützt GET- und POST-Anfragen
@app.route('/registrieren', methods=['GET', 'POST'])
def registrieren():
    # Wenn der Benutzer bereits angemeldet ist, wird er zur Startseite weitergeleitet
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()  # Initialisiert das Registrierungsformular
    # Überprüft, ob das Formular korrekt ausgefüllt wurde
    if form.validate_on_submit():
        # Erstellt einen neuen Benutzer mit den eingegebenen Daten und fügt ihn zur Datenbank hinzu
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Setzt das Passwort für den Benutzer
        db.session.add(user)
        db.session.commit()  # Speichert die Änderungen in der Datenbank
        flash('Benutzer {} ist jetzt Registriert'.format(form.username.data))  # Zeigt eine Bestätigungsmeldung an
        return redirect(url_for('login'))  # Leitet zur Login-Seite weiter
    # Rendert die Registrierungsseite mit dem Formular
    return render_template('registrieren.html', title='Registrierung', form=form)

# Route, um das Profil eines Benutzers anzuzeigen, erfordert Login
@app.route('/user/<username>')
@login_required
def user(username):
    # Sucht den Benutzer in der Datenbank anhand des Benutzernamens, gibt 404 zurück, falls er nicht gefunden wird
    user = User.query.filter_by(username=username).first_or_404()
    # Rendert die Seite zur Anzeige des Benutzerprofils
    return render_template('profil_anzeigen.html', user=user)

# Route zum Bearbeiten des Benutzerprofils, unterstützt GET- und POST-Anfragen
@app.route('/profil_editieren', methods=['GET', 'POST'])
@login_required
def profil_editieren():
    form = EditUserForm()  # Initialisiert das Formular zur Profilbearbeitung
    # Fügt eine Liste von Spielen zur Auswahl hinzu, geordnet nach Spielnamen
    form.lieblingsquiz.choices = [(s.spiel_id, s.spielname) for s in Spiele.query.order_by('spielname')]
    # Wenn das Formular validiert wurde, werden die Änderungen übernommen
    if form.validate_on_submit():
        if form.username.data:  # Wenn der Benutzername eingegeben wurde, wird er aktualisiert
            current_user.username = form.username.data
        current_user.lieblingsquiz_id = form.lieblingsquiz.data  # Aktualisiert das Lieblingsquiz des Benutzers
        db.session.commit()  # Speichert die Änderungen in der Datenbank
        flash('Profil wurde angepasst')  # Zeigt eine Bestätigungsmeldung an
        return redirect(url_for('profil_editieren'))  # Leitet zur Profilbearbeitungsseite zurück
    # Rendert die Seite zur Profilbearbeitung mit dem Formular
    return render_template('profil_editieren.html', title='Profil editieren', form=form)

# Route zur Anzeige aller Spiele, erfordert Login
@app.route('/spiele_anzeigen')
@login_required
def spiele_anzeigen():
    spiele = Spiele.query.all()  # Ruft alle Spiele aus der Datenbank ab
    # Rendert die Seite zur Anzeige der Spiele
    return render_template('quiz_anzeigen.html', title='Quiz anzeigen', spiele=spiele)

# Route zum Erfassen neuer Spiele, unterstützt GET- und POST-Anfragen
@app.route('/spiele_erfassen', methods=['GET', 'POST'])
@login_required
def spiele_erfassen():
    form = SpieleForm()  # Initialisiert das Formular zur Erfassung von Spielen
    # Wenn das Formular korrekt ausgefüllt wurde, wird das neue Spiel der Datenbank hinzugefügt
    if form.validate_on_submit():
        spiel = Spiele(spielname=form.spielname.data, spieler_min=form.spieler_min.data, 
                       spieler_max=form.spieler_max.data, dauer_min=form.dauer_min.data,
                       dauer_max=form.dauer_max.data)  # Erstellt ein neues Spielobjekt
        db.session.add(spiel)  # Fügt das Spiel der Datenbank hinzu
        db.session.commit()  # Speichert die Änderungen in der Datenbank
        flash('Spiel {} wurde erfasst.'.format(form.spielname.data))  # Zeigt eine Bestätigungsmeldung an
        return redirect(url_for('spiele_erfassen'))  # Leitet zur Erfassungsseite zurück
    # Rendert die Seite zur Erfassung von Spielen mit dem Formular
    return render_template('quiz_erfassen.html', title='Quiz erfassen', form=form)
