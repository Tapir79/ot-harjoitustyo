## Viikko 3

- Lisätty pelin perusrunko
- Lisätty Player luokka eli pelaaja ja pelaajalle lisätty kuva, sijainti ja liikkuminen
näppäimistöllä
- Lisätty yksikkötestit pelaajan liikkumiselle
- Erotettu pelilogiikka omaan pakettiin käyttöliittymästä

## Viikko 4 

- Lisätty Bullet luokka eli ammus käyttöliittymään. 
- Lisätty service luokka ammukselle eli ampumisen logiikka 
- Toteutettu pelaajan ampumislogiikka
- Lisätty yksikkötestit pelaajan ampumiselle ja refaktoroitu yksikkötestejä yleisesti 
- Lisätty projektiin koodin laadunvarmistus (lint) ja korjattu koodista kaikki löydetyt laatuvirheet

## Viikko 5 

- Lisätty pelaajan luotien ja vihollisten välinen törmäystarkastelu pygamella
- Lisätty pelaajan ja vihollisten luotien väliset törmäystarkastelut pygamella
- Lisätty pelin lopetus, kun pelaajaan osuu 3 vihollisen luotia. 
- Lisätty animaatiot osumiselle ja pelaajan tuhoutumiselle
- Lisätty pelin loppuminen jos pelaaja kuolee
- Lisätty peliin tasot ja tasokonfiguraatio, jolla generoidaan tasot pelin alkaessa
- Lisätty pelaajan elämät ja niiden näyttäminen käyttöliittymässä
- Lisätty pelille apumetodeja, jotka eivät suoraan sovi tietyn luokan alle
- Lisätty yksikkötestejä pelaajalle ja apumetodeille 
- Korjattu koodista kaikki löydetyt laatuvirheet
- Päivitetty arkkitehtuuridokumentaatio muutosten osalta ja lisätty uusia sekvenssikaavioita kuvaamaan yhteentörmäyksiä
- Pelaajan tulosten tallentaminen ja päivittäminen tietokantaan.

## Viikko 6 

- Refaktoroitu kaikki models-luokat ja service-luokat siten, että muuttujista on pythonin suositusten mukaisesti tehty yksityisiä ja kaikille yksityisille muuttujille property/setter-metodit. 
- Kaikki muu tähän asti tehty koodi dokumentoitu docstringeillä paitsi game.py-luokka
- Luotu aloitusvalikko, rekisteröityminen ja sisäänkirjautuminen ja niille yhteinen base-näkymä.  
- Lisätty sqlite-tietokanta. Tietokantaan tallennetaan pelaajan käyttäjätunnus ja salasana.
- Tietokantaan tallennetaan pelaajan paras tulos ja korkein saavutettu taso. 
- Lisätty tietokantaa kutsuville funktioille testejä.
- Tyylitelty ja refaktoroitu aloitusvalikko.  