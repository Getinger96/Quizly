# 📘 Quiz API – README

## Überblick
Diese API bietet folgende Funktionen:
- Benutzerregistrierung und Login via Cookie-basierter Authentifizierung
- Automatische Quizgenerierung über YouTube-URLs
- CRUD-Funktionen für Quizzes
- Zugriffsbeschränkungen basierend auf Benutzer-Ownership

Die Authentifizierung erfolgt über HttpOnly Cookies (access_token, refresh_token).

## Authentifizierung
| Token | Beschreibung |
|-------|--------------|
| access_token | JWT für autorisierte Requests |
| refresh_token | Token zur Erneuerung des Access Tokens |

# Endpoints

# Auth Endpoints

## POST /api/register/
Registriert einen neuen Benutzer.
### Request Body
{
  "username": "your_username",
  "password": "your_password",
  "confirmed_password": "your_confirmed_password",
  "email": "your_email@example.com"
}
### Status Codes
201 – Benutzer erfolgreich erstellt  
400 – Ungültige Daten  
500 – Serverfehler  

## POST /api/login/
Loggt den Benutzer ein und setzt Auth-Cookies.
### Request Body
{
  "username": "your_username",
  "password": "your_password"
}
### Status Codes
200 – Login erfolgreich  
401 – Ungültige Anmeldedaten  
500 – Serverfehler  

## POST /api/logout/
Loggt den Benutzer aus und löscht Tokens.
### Request Body
{}
### Status Codes
200 – Logout erfolgreich  
401 – Nicht authentifiziert  
500 – Serverfehler  

## POST /api/token/refresh/
Erneuert den Access Token anhand des Refresh Tokens.
### Request Body
{}
### Status Codes
200 – Token erfolgreich erneuert  
401 – Refresh Token ungültig oder fehlt  
500 – Serverfehler  

# Quiz Endpoints

## POST /api/createQuiz/
Erstellt ein Quiz basierend auf einer YouTube-URL.
### Request Body
{
  "url": "https://www.youtube.com/watch?v=example"
}
### Status Codes
201 – Quiz erfolgreich erstellt  
400 – Ungültige URL oder Daten  
401 – Nicht authentifiziert  
500 – Serverfehler  

## GET /api/quizzes/
Liefert alle Quizzes des authentifizierten Benutzers.
### Status Codes
200 – Erfolg  
401 – Nicht authentifiziert  
500 – Serverfehler  

## GET /api/quizzes/{id}/
Ruft ein bestimmtes Quiz ab.
### URL Parameter
id – ID des Quizzes  
### Status Codes
200 – Erfolg  
401 – Nicht authentifiziert  
403 – Zugriff verweigert  
404 – Quiz nicht gefunden  
500 – Serverfehler  

## PATCH /api/quizzes/{id}/
Partielle Aktualisierung eines Quiz.
### Request Body Beispiel
{
  "title": "New Title"
}
### Status Codes
200 – Aktualisiert  
400 – Ungültige Daten  
401 – Nicht authentifiziert  
403 – Kein Zugriff  
404 – Quiz nicht gefunden  
500 – Serverfehler  

## DELETE /api/quizzes/{id}/
Löscht ein Quiz permanent.
### Status Codes
204 – Erfolgreich gelöscht  
401 – Nicht authentifiziert  
403 – Kein Zugriff  
404 – Quiz nicht gefunden  
500 – Serverfehler  

# Fehlercodes
200 – Erfolg  
201 – Ressource erstellt  
204 – Erfolgreich gelöscht  
400 – Ungültige Daten  
401 – Nicht authentifiziert  
403 – Zugriff verweigert  
404 – Nicht gefunden  
500 – Serverfehler  

# Rate Limits
Diese API besitzt keine Rate Limits.
