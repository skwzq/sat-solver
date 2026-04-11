Yksikkötestauksen kattavuusraportti (saatu komennoilla `coverage run --branch -m pytest src`, `coverage report -m`):
```
Name            Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------
src/solver.py      34      0     26      0   100%
-----------------------------------------------------------
TOTAL              34      0     26      0   100%
```

Testattu, että
- algoritmi palauttaa tyhjän listan, kun syötteenä annetaan tyhjä kaava
- algoritmi palauttaa arvon `None`, kun syöte on (hyvin yksinkertainen) toteutumaton kaava
- algoritmi palauttaa oikean totuusjakauman, kun syötteenä annetaan yksinkertainen 2 tai 4 muuttujan toteutuva kaava

Testit voidaan toistaa ajamalla komento `pytest src` Poetry-virtuaaliympäristössä projektin juurihakemistossa.