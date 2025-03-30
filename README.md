# Ohjelmistotekniikka, harjoitustyö
# Space Invaders
Space Invaders on sovellus, jossa pelaaja ohjaa avaruusalusta ja yrittää estää avaruusolentoja pääsemästä maahan. Peli sisältää erilaisia tasoja, joissa vihollisten määrä, voima ja nopeus kasvavat, ja pelaajan tavoitteena on selviytyä mahdollisimman pitkään hengissä.

## Dokumentaatio
* **TODO**: Käyttöohje
* [Vaatimusmäärittely](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/vaatimusmaarittely.md)
* **TODO**: Arkkitehtuurikuvaus
* **TODO**: Testausdokumentti
* [Työaikakirjanpito](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/tyoaikakirjanpito.md)
* [Changelog](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/changelog.md)


## Ohjelman asentaminen ja käynnistäminen
1. ``poetry install``

2. ``poetry run invoke start``

## Komentorivitoiminnot

### Käynnistäminen    
``poetry run invoke start``

### Testien ajaminen    
``poetry run invoke test``

### Testikattavuusraportin generoiminen 
``poetry run invoke coverage-report``    
Raportti löytyy projektin juuresta kansiosta: ``htmlcov/index.html``

### Pylintin ajaminen 
Projektissa käytetyn [.pylinrc](https://github.com/Tapir79/ot-harjoitustyo/tree/main/.pylintrc) -tiedoston ajaminen    
``poetry run invoke lint``

## Lisenssit
### Kuvat: 
- Kenney: https://kenney.nl/assets/space-shooter-extension 
CC lisenssi: https://creativecommons.org/publicdomain/zero/1.0/