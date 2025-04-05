# Arkkitehtuurikuvaus

## Rakenne 

Pelin rakenne neudattaa seuraavanlaista kolmikerrosarkkitehtuuria: 

```mermaid
graph TD
    UI[UI - Pygame] --> Services
    Services[Services - Logiikka] --> Models
    Services --> Repositories[Repositories - Tulossa]
    Repositories --> Entities[Entities - Tulossa]

```

- ui-pakkaus sisältää käyttöliittymän eli pygame-osuuden 
- services-pakkaus sisältää pelilogiikan
- models-pakkaus sisältää luokkia, joita käytetään logiikkapakkauksessa esim. tietojen organisointiin
- TODO vaiheessa on repositories ja entities, jonne tulee myöhemmin tietojen pysyväistallennuksesta vastaava koodi ja tietokantatauluja vastaavat python-rakenteet eli entiteetit.  

## Käyttöliittymä 

Käyttöliittymä sisältää Pygame-pelin. Se sisältää tällä hetkellä pelkän pelinäkymän, joka alkaa suoraan, kun sovellus käynnistetään. 
TODO vaiheessa ovat käyttäjän luominen ja kirjautuminen eli aloitusnäkymä ja kirjautumisnäkymä. Näkymät sijaitsevat ui-kansiossa, jonne on eristetty kaikki Pygame-koodi. Kansion entrypoint on game.py. Peli käynnistetään src-kansion juuresta, tiedostosta main.py.  

## Sovelluslogiikka 


```mermaid
classDiagram
    class BaseSpriteService {
        +sprite_info: SpriteInfo
        +speed: int
        +get_position()
        +increase_speed()
        +decrease_speed()
    }

    class PlayerService {
        +move(key)
        +shoot()
    }

    class BulletService {
        +move()
        +update()
    }

    BaseSpriteService <|-- PlayerService
    BaseSpriteService <|-- BulletService


```
playerservice, bulletservice
TODO enemyservice, jotka jakavat base-luokan base_sprite_service. Base-luokassa on kaikille yhteisiä yleisiä ominaisuuksia, kuten koko ja sijainti. 

Service-luokkien ja luokan ja ohjelman muiden osien suhdetta kuvaava luokka/pakkauskaavio:


## Tietojen pysyväistallennus 

Tämä osio on vielä toteuttamatta, mutta tietokantaan tallennetaan jatkossa rekisteröityneet käyttäjät ja käyttäjät pelistatistiikat. 

## Ohjaustiedostot 

Sovelluksen globaalit vakiot on tallennettu config.py-tiedostoon. 

Sovellukselle on myös tulossa SQLite-tietokannan alustustiedosto. 

---

### Päätoiminnallisuudet

Kuvataan seuraavaksi sovelluksen toimintalogiikka muutaman päätoiminnallisuuden osalta sekvenssikaaviona.

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant PlayerSprite
    participant PlayerService
    participant BulletService
    participant BulletSprite

    Main->>Game: aloita peli
    Game->>PlayerSprite:luo pelaaja()
    Game->>Game: luo pelisimukka

    loop peli-iteraatio
        PlayerSprite->>PlayerService: painaa "a" / "d"
        PlayerService->>PlayerService: päivitä sijainti
        PlayerSprite->>Game: piirrä pelaajan sijainti
        PlayerSprite->>PlayerService: painaa "SPACE"
        PlayerService->>BulletService: luo uusi bullet
        BulletService-->>BulletSprite: uusi bullet sprite
        BulletService->>BulletService: päivitä sijainti
        BulletSprite->>Game: piirrä luoti
    end
```

## Käyttäjän kirjautuminen 

Toteuttamatta 

## Uuden käyttäjän luominen 

Toteuttamatta 

## Pelin eteneminen 



# Jatkokehitystä vaativat toiminnallisuudet ja rakenteelliset heikkoudet

Toteuttamatta