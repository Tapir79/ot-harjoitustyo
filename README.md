# Ohjelmistotekniikka, harjoitustyö
# Alien Attack
[Space Invadersin](https://fi.wikipedia.org/wiki/Space_Invaders) kaltainen peli on sovellus, jossa pelaaja ohjaa avaruusalusta ja yrittää estää avaruusolentoja pääsemästä maahan. Peli sisältää erilaisia tasoja, joissa vihollisten määrä, voima ja nopeus kasvavat, ja pelaajan tavoitteena on selviytyä mahdollisimman pitkään hengissä.

## Julkaisu (release)

Lataa uusin julkaisu täältä:  
[![GitHub release](https://img.shields.io/github/v/release/Tapir79/ot-harjoitustyo?label=Release&cacheSeconds=0)](https://github.com/Tapir79/ot-harjoitustyo/releases/latest)



## Dokumentaatio
* [Käyttöohje](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/kayttoohje.md)
* [Vaatimusmäärittely](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/vaatimusmaarittely.md)
* [Arkkitehtuuri](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/arkkitehtuuri.md)
* [Testausdokumentti](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/testaus.md)
* [Työaikakirjanpito](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/tyoaikakirjanpito.md)
* [Changelog](https://github.com/Tapir79/ot-harjoitustyo/tree/main/dokumentaatio/changelog.md)


## Ohjelman asentaminen ja käynnistäminen
1. ``poetry install``

2. ``poetry run invoke build``

3. ``poetry run invoke start``

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
- Kenney Space Shooter Extension: https://kenney.nl/assets/space-shooter-extension     
CC lisenssi: https://creativecommons.org/publicdomain/zero/1.0/
- Kenney Board Game Icons: https://kenney.nl/assets/board-game-icons     
CC lisenssi: https://creativecommons.org/publicdomain/zero/1.0/
- Pelin otsikkokuvan luomisessa on käytetty mallina ANSI Shadow -fonttia: https://github.com/pwaller/pyfiglet.    
MIT lisenssi: https://opensource.org/license/mit     

## Tekoälyn käyttö
Projektissa on käytetty [ChatGPT 4o](https://chatgpt.com/)-kielimallia virheviestien ja pylint-virheiden tulkintaan ja virheiden etsimiseen. Tekoälyä on myös käytetty tukena docstring-pohjien tekemiseen. Tekoälyllä ei ole kuitenkaan generoitu koodia tai tekstiä. 
