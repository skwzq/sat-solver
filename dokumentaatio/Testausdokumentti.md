Yksikkötestauksen kattavuusraportti (saatu komennoilla `coverage run --branch -m pytest src`, `coverage report -m`):
```
Name            Stmts   Miss Branch BrPart  Cover   Missing
-----------------------------------------------------------
src/solver.py      89      0     56      1    99%   202->218
-----------------------------------------------------------
TOTAL              89      0     56      1    99%
```
Raportissa näkyvä puuttuva haara on for-silmukka, jonka sisältö suoritetaan aina vähintään kerran. Kyseistä silmukkaa ei ole jätetty pois kattavuusmittauksesta, jotta sen sisällön testikattavuus tulee mitatuksi.

Testattu, että
- algoritmi palauttaa tyhjän listan, kun syötteenä annetaan tyhjä kaava
- algoritmi palauttaa arvon `None`, kun syöte on (hyvin yksinkertainen) toteutumaton kaava
- algoritmi palauttaa oikean totuusjakauman kolmella pienellä ja kahdella isommalla syötteellä.

Pienempien syötteiden tarkoitus on testata algoritmin toiminnan oikeellisuutta lähes kaikissa tapauksissa. Isompien syötteiden tarkoituksena on testata, että algoritmi toimii oikein myös isommilla syötteillä, sekä parissa tapauksessa, joita edeltävät pienemmillä syötteillä tehdyt testit eivät kata.

Ohjelmaa testataan pelkästään yksikkötesteillä, jotka toimivat käytännössä samalla päästä päähän -testeinä, koska ohjelmassa on vain yksi testattavissa oleva ydintoiminnallisuuden kannalta olennainen metodi. Vaikka toiminnallisuutta on jaettu useisiin pienempiin apumetodeihin, tämä on tehty lähinnä luettavuuden takia, ja näiden metodien testaaminen yksinään olisi vaikeaa.

Testit voi suorittaa Poetryn ja projektin riippuvuuksien asentamisen jälkeen komennolla `poetry run pytest src`.