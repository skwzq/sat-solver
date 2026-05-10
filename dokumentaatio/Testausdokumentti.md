Yksikkötestauksen kattavuusraportti (saatu komennoilla `coverage run --branch -m pytest src`, `coverage report -m`):
```
Name            Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------
src/solver.py     105      1     78      2    98%   153, 198->214
-----------------------------------------------------------
TOTAL             105      1     78      2    98%
```

Testattu, että
- algoritmi palauttaa tyhjän listan, kun syötteenä annetaan tyhjä kaava
- algoritmi palauttaa arvon `None`, kun syöte on (hyvin yksinkertainen) toteutumaton kaava
- algoritmi palauttaa oikean totuusjakauman kolmella pienellä ja kahdella isommalla syötteellä.

Toteutettujen testien tarkoitus on testata solver-moduulin koodin kaikki haarat. Testit ovat kuitenkin hyvin pintapuolisia, eivätkä tällä hetkellä edes testaa kaikkia haaroja, kuten kattavuusraportista näkyy.

Testit voi suorittaa Poetryn ja projektin riippuvuuksien asentamisen jälkeen komennolla `poetry run pytest src`.