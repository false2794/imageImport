# Guten Hallo.

**imageImport** ist ein Werkzeug, um - wie der Name vermuten lässt - Bilddateien zu importieren bzw. kopieren.<br>
Es wurde in [Python](https://www.python.org/downloads/) [3.13.7](https://www.python.org/downloads/release/python-3137/) entwickelt und benötigt daher zum Ausführen [Python](https://www.python.org/downloads/) (*vorzugsweise [3.13.7](https://www.python.org/downloads/release/python-3137/) oder neuer*) auf dem Computer.

## Installation der Python Module
Wir nutzen den Package Manager [pip](https://pip.pypa.io/en/stable/) zum installieren der Module.<br>
Netterweise habe ich eine *requirements.txt* bereitgestellt. Rechnung kommt per Mail.<br>
Öffne die Kommandozeile dort, wo du die Dateien entpackt hast (*main.py sollte sich am selben Ort befinden*)
```bash
pip install -r requirements.txt
```
oder
```bash
python -m pip install -r requirements.txt
```

## Erster Anlauf
Zum Ausführen öffnen wir erneut die Kommandozeile, wie beim vorherigen Schritt.<br>
Folgender Befehl startet unser kleines Script.
```bash
python main.py
```
Beim ersten Mal (*hihi*) wirst du beim Initialisierungsvorgang einige Dinge gefragt.<br>
Besonders wichtig ist die Angabe des Verzeichnisses, das als Wurzelverzeichnis für zukünftige Import/Kopier-Vorgänge dienen soll. Hierbei ist auf die Verwendung eines *absoluten Pfades* zu achten. Z. B.
```bash
C:\Pfad\zum\Wurzelverzeichnis
C:/Pfad/zum/Wurzelverzeichnis
```
Aber bitte **for fucks sake**, speicher nicht deine tausenden Fotos auf der Systemfestplatte ab.<br>
Solltest du das irgendwie verkackt haben oder du hast das Bedürfnis die vorgenommenen Einstellungen zu ändern, hast du dazu jedes Mal erneut die Gelegenheit durch das folgende Argument:
```bash
python main.py init
```
## Bekannte Fehler
Bei bearbeiteten oder exportierten Bilddateien kann das korrekte Datum (Aufnahmedatum) nicht richtig ausgelesen werden und es wird alternativ ein anderes Datum (z. B. letztes Änderungsdatum) verwendet.
## Nachwort
Dat Ding is neu und wahrscheinlich an einigen Stellen dezent fehlerhaft -> mit Vorsicht genießen und den Kopiervorang im Nachhinein überprüfen.<br>
Im Verzeichnis *"logs"* findest du Logs - wer hätte es gedacht. Aktuell besteht das logging ausschließlich aus DEBUG und EXCEPTION und wird bei Bedarf in der Zukunft um INFO, WARNING und ERROR erweitert.