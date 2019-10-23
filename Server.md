Object of this document is the Python 3.7 Code File,
present in Server/main.py and, by extension, other Files
in that directory.
This API Manual is written in German.

# Server/main.py API
Dieser Text handelt von dieser Datei,
die einen einfachen Flask Server startet.
Folgende URI-Routes sind vorhanden:
```
/login : Login mit Benutzername und Passwort
/register : Registriere dich mit Benutzername, Vor- und Nachnamen, einer Mail Addresse und einem Passwort
/vote : Wenn du eingeloggt bist, kannst du zu jeder aktuellen Wahl deine Stimme abgeben, indem du alle Optionen von deinem unbeliebtesten zu deinem Favoriten ordnest, du Teilst die Optionen mit ;
/election : Sehe die Wahlergebnisse vergangener Wahlen an.
```
