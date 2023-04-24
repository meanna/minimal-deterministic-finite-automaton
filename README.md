# Abschlussprojekt - Basismodul
##  Daciuk-Algorithmus

Daciuk-Algorithmus zur Konstruktion eines minimalen Lexikonautomaten mit verschiedenen Erweiterungen

- Folgende Erweiterungen wurden implementiert
  - **Sprache des Automaten**
  - **Graphische Darstellung**
  - **Speichern und Laden (von Automat und Tarjan-Tabelle)**
  - **Tarjan-Tabelle**

## Includes
- daciuk.py
- run.py
- wordlist.txt
- wordlist_abbauen.txt
- wordlist_acker.txt
- automat.pkl
- tarjan.pkl
- graph (Ordner)
  - aut1.gv
  - aut.gv.pdf

## Package requirements
- graphviz (`pip install graphviz` or `conda install python-graphviz`)
- python 3.8

## How to use the program
Um das Programm zu starten, bitte in die Kommandozeile eingeben: `python run.py`.


````angular2html
**********************************************************************
Daciuk-Algorithmus zur Konstruktion eines minimalen Lexikonautomaten
**********************************************************************

Automat erstellen
(1) Einen minimalen Automat aus einer Wortliste erstellen
(2) Einen gespeicherten Automat laden
````

(1) Einen minimalen Automat aus einer Wortliste erstellen
````
Bitte eine Nummer eingeben: 1
Bitte den Dateinamen eingeben: wordlist_abbilden.txt
````
- Wortliste, die getestet werden können: `wordlist_abbauen.txt`, `wordlist.txt`, `wordlist_acker.txt`

Ausgabe

````angular2html
Die Datei wordlist_abbauen.txt hat den folgenden Inhalt...

      abbau
      abbauen
      abbild
      abbilden
      abend
      ablauf

Der Automat wird mit diesen Wörtern erstellt.

------------------------------
````

(2) Einen gespeicherten Automat laden
````
Bitte eine Nummer eingeben: 2
Der abgespeicherte Automaten wird geladen...

Bitte den Dateinamen eingeben: automat.pkl
````
Ausgabe
````
=====================Min DEA===================
Sprache: ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf']

0    a    1
1    b    2
2    b    3
2    e    13
2    l    16
3    a    4
3    i    8
4    u    5
5    e    6
6    n    7
8    l    9
9    d    5
13    n    14
14    d    7
16    a    17
17    u    18
18    f    7
------------------------------
````
### Funktionalitäten
````
Was möchstest du tun?

(1) Wort abfragen
(2) Sprache abfragen
(3) Automaten zeichnen
(4) Automaten speichern und anzeigen
(5) Tarjan Tabelle erstellen, anzeigen und speichern
(6) Tarjan Tabelle laden und anzeigen
(7) oder leeres String: Exit

Bitte eine Nummer eingeben: 
````

(1) **Wort abfragen**. Durch die Eingabe `1` kann der Benutzer prüfen, ob ein Wort zur Sprache des Automaten gehört.

````angular2html
Bitte ein Wort eingeben: abbau
Ja, das Wort 'abbau' ist Teil der Sprache des Automaten.
````
````angular2html
Bitte ein Wort eingeben: new york
Nein, das Wort 'new york' ist NICHT Teil der Sprache des Automaten.
````

(2) **Sprache abfragen**. Durch die Eingabe `2` kann der Benutzer die Sprache des Automaten ausgeben. 
Der Inhalt der Wortliste wird ebenfalls zurückgegeben, um zu überprüfen, ob der Automat korrekt konstruiert ist.

````angular2html
Wortliste:  ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf']
Sprache des Automaten:  ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf']
````

(3) **Automaten zeichnen**. Durch die Eingabe `3` wird der Automat graphisch dargestellt mit Dateiname:
[graph/aut1.gv.pdf](graph/aut1.gv.pdf)

(4) **Automaten speichern**. Durch die Eingabe `4` wird der Automat abgespeichert um ihn später zu laden.
Der Automat und seine Sprache werden ebenfalls angezeigt.
````angular2html
Der Automaten wird gespeichert...
=====================Min DEA===================
Sprache: ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf'] 

0    a    1
1    b    2
2    b    3
2    e    13
2    l    16
3    a    4
3    i    8
4    u    5
5    e    6
6    n    7
8    l    9
9    d    5
13    n    14
14    d    7
16    a    17
17    u    18
18    f    7
=======================
Der Automaten wurde als 'automat.pkl' gespeichert.
````

(5) **Tarjan Tabelle erstellen und speichern**. Durch die Eingabe `5` wird eine Tarjan-Tabelle erstellt 
und abgespeichert. Die Ausgabe ist die Tabelle, der/die Startpunkt(e) und die entsprechende Wortliste.

````angular2html
Tarjan Tabelle wird erstellt...
Wörter:  ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf']
=====Tarjan Table=====
-       -       -
1       F       7
2       N       6
3       F       5
4       N       4
5       N       9
6       N       13
7       e       2
8       d       3
9       N       8
10      n       1
11      N       3
12      a       4
13      u       3
14      n       15
15      N       14
16      l       5
17      i       9
18      d       1
19      N       18
20      N       17
21      N       16
22      a       20
23      N       2
24      f       1
25      b       11
26      N       1
27      e       6
28      b       23
29      u       19
30      l       21
31      N       0
32      a       26
=====================
Startpunkt(e) der Tarjan-Tabelle [(32, 'a', 26)]
Die Tarjan-Tabelle wurde mit diesem Dateinamen gespeichtert: tarjan.pkl
````

(5) **Tarjan Tabelle laden**. Durch die Eingabe `6` wird eine abgespeicherte Tarjan-Tabelle geladen und angezeigt. 
````angular2html
Pickle Datei von der gespeicherte Tarjan Tabelle eingeben: tarjan.pkl

Die Tarjan-Tabelle aus tarjan.pkl wird geladen...
Wortliste:  ['abbau', 'abbauen', 'abbild', 'abbilden', 'abend', 'ablauf']
=====Tarjan Table=====
-       -       -
1       F       7
2       N       6
3       F       5
4       N       4
5       N       9
6       N       13
7       e       2
8       d       3
9       N       8
10      n       1
11      N       3
12      a       4
13      u       3
14      n       15
15      N       14
16      l       5
17      i       9
18      d       1
19      N       18
20      N       17
21      N       16
22      a       20
23      N       2
24      f       1
25      b       11
26      N       1
27      e       6
28      b       23
29      u       19
30      l       21
31      N       0
32      a       26
=====================
Die Startpunkt(e) der Tarjan-Tabelle sind:  [(32, 'a', 26)]
------------------------------
````

(7) **Exit**. Durch die Eingabe `7` oder ein leeres String wird das System beendet.
