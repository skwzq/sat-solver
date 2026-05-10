### Ohjelman yleisrakenne
Ohjelma koostuu kolmesta moduulista: *solver.py*, *parse_files.py* ja *main.py*. *solver.py* sisältää ohjelman päätoiminnallisuuden. *parse_files.py* sisältää tiedostojen käsittelyyn liittyvät funktiot. *main.py* on ohjelman päämoduuli, joka käyttää *solver.py*:n solve_sat-funktiota ja *parse_files.py*:n parse_cnf-funktiota.

### Aika- ja tilavaativuudet
Aikavaativuudeltaan vaativin osa ohjelmaa on yksikköpropagaatio. Epätosien watched literalien läpikäynnin aikavaativuus on pahimmassa tapauksessa *O*(*mn*), missä *n* on muuttujien lukumäärä ja *m* on klausuulien lukumäärä. Jokaista näistä kohti käydään läpi senhetkinen totuusjakauma, minkä aikavaativuus on pahimmillaan *O*(*n*), joten yksikköpropagaation ja samalla koko ohjelman aikavaativuudeksi tulee *O*(*mn*²).

Ohjelman tilavaativuus on *O*(*L*), missä *L* on literaalien lukumäärä.

Wikipediassa DPLL-algoritmille ilmoitettujen aika- ja tilavaativuuden perusteella (*O*(2*ⁿ*) ja *O*(*n*)) ohjelma on siis aikavaativuudeltaan perus-DPLL:ää selvästi tehokkaampi ja tilavaativuudeltaan samaa tasoa.

### Puutteet
Projektin testaus on puutteellista.

### Laajojen kielimallien käyttö
Tämän harjoitustyön tekemisessä ei ole käytetty laajoja kielimalleja.

### Lähteet
- Automated Reasoning -kanava YouTubessa: *Lecture 06-1 SAT solver optimizations: 2-watched literals*, 2020. https://www.youtube.com/watch?v=n3e-f0vMHz8, katsottu 8.4.2026.
- *DIMACS CNF*. https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html, vierailtu 27.3.2026.
- Tommi Junttila: *Conflict-driven clause learning (CDCL) SAT solvers*, 2020. https://users.aalto.fi/~tjunttil/2020-DP-AUT/notes-sat/cdcl.html, vierailtu 25.4.2026.
- Wikipedia: *DPLL algorithm*, 2026. https://en.wikipedia.org/wiki/DPLL_algorithm, vierailtu 21.3.2026.
