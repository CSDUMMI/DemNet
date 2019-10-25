Object of this document is the Python 3.7 Code File,
present in Server/main.py and, by extension, other Files
in that directory.
This API Manual is written in German.

# Server/main.py API
Dieser Text handelt von dieser Datei,
die einen einfachen Flask Server startet.
Folgende URI-Routes sind vorhanden:

[`/login`](#login) : Login mit Benutzername und Passwort

[`/register`](#register) : Registriere dich mit Benutzername, Vor- und Nachnamen, einer Mail Addresse und einem Passwort

[`/vote`](#vote) : Wenn du eingeloggt bist, kannst du zu jeder aktuellen Wahl deine Stimme abgeben, indem du alle Optionen von deinem unbeliebtesten zu deinem Favoriten ordnest, du Teilst die Optionen mit ;

[`/election`](#election) : Sehe die Wahlergebnisse vergangener Wahlen an.

## Login
Argumente:
```
username :: String - Benutzername des Nutzers 
password :: String - Passwort des Nutzer
```

Antwort (Response):
- Wenn eingeloggt : `LoggedIn`
- Wenn ein Fehler passiert : `NotLoggedIn`

## Register
Registriert einen neuen Nutzer:
Argumente:
```
username :: String - Benutzername des neuen Nutzers
password :: String - Passwort des neues Nutzers
email :: String - E-Mail Addresse des neuen Nutzers
firstName :: String - Vorname des neuen Nutzers
secondName :: String - Nachname des neuen Nutzers
```
Der Benutzer wird immer durch einen einzigartigen `username` identifiziert,
aber hinter der Meinung des Benutzers, wenn dieser sie nicht in einer Wahl
äußert, muss der Name stehen, damit niemand versucht eine Diskussion zu zerstören
und damit klar ist, dass jeder mit dem du redest ein Mensch ist und so behandelt werden sollte.

Antwort (Response):
- Wenn registriert: `Registered`
- Wenn nicht registriert: `NotRegistered`

## Vote
Äquivalent zum phyisichen Akt, einen Wahlzettel in die Urne zu werfen.
Argumente:
```
election :: String -  Name der Wahl
vote :: Liste von Optionen, getrennt mit ; - Der Wahlzettel.
```

Es gibt einige Regeln für `vote` und wenn diese nicht befolgt werden,
werden sie rausgeschmissen:
1. Die Option, die du am wenigsten magst kommt zuerst, gefolgt von der die du etwas mehr magst, bis zur letzten, die Option, die dein Favorit ist.
1. Wähle keine Option, die es nicht gibt
2. Wähle jede Option nur einmal
3. Mach soviele alternative Wahlen, wie es Optionen gibt.

Zu 3., wenn du keine der anderen Optionen mehr magst, gibt es immer die Option
`NoneOfTheOtherOptions` und wenn 50 % der Wähler `NoneOfTheOtherOptions` wählen, ( zum Schluss wählen ), wird die Wahl als unrechtmäßig angesehen und niemand gewinnt.

Antwort ( Response ):
- Erfolgreich gewählt: `Voted`
- Nicht gewählt, Fehler: `NotVoted`

## Election
Hole die Ergebnisse von vergangenen Wahlen:
```
election :: String - Name der Wahl
```
Antwort (Response).
- Wenn die Wahl existiert, aber nicht vorbei ist: `BallotNotClosed`
- Wenn die Wahl nicht existiert: `NotAnElection`
- Wenn es die Wahl gibt und sie vorbei ist, gibt es einen JSON Response: (eine Beispiel Wahl, wo 'D' gewonnen hat)
```json
{
  "option": "D", 
  "support": [
              ["A", "B", "C", "D"], 
              ["B", "C", "A", "D"], 
              ["B", "C', "A", "D"], 
              ["C", "A", "D"], 
              ["C", "A", "D"], 
              ["A", "B", "D"],
              ["C", "A", "D"],
              ["C", "A", "D"]
             ],
  "participants_count": 12
} 
```

- `option` : Name der Option, die gewählt wurde
- `support` : Wahlzettel, die diese Option irgedenwann gewählt hat, man kann sehen, wieviele `D` zuerst gewählt haben und wieviele `D` nur als Alternative sehen.
- `participants_count` : Anzahl der Wähler, damit kann ausgerechnet werden, wieviele Prozent zum Schluss `D` gewählt haben. ( Im Beispiel: 8 / 12 =  66.66 % )
in 
Dieses Beispiel, von zufälligen Wahlzetteln, zeigt, dass `D` hier deutlich höhere Unterstützung hat,
als alle Bundestagsabgeordnete, [die ihren Sitz 2017 in einer Direktenwahl in Wahlkreisen bekammen.](https://www.spiegel.de/politik/deutschland/bundestagswahl-2017-alle-ergebnisse-im-ueberblick-a-1167247.html)
