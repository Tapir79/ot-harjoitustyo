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

playerservice, bulletservice ja enemyservice, jakavat base-luokan base_sprite_service. Lisäksi player- ja enemyservice perivät shootingSpriteService:n. Base-luokassa on kaikille yhteisiä yleisiä ominaisuuksia, kuten koko, sijainti ja nopeus. 

Service-luokkien ja luokan ja ohjelman muiden osien suhdetta kuvaava luokkakaavio:

```mermaid
classDiagram
    class BaseSpriteService {
        +sprite_info: SpriteInfo
        +get_position()
        +increase_speed()
        +decrease_speed()
    }

    class ShootingSpriteService {
        +move(key)
        +shoot()
        +update()
    }

    class PlayerService {
       
    }

    class EnemyService {

    }

    class BulletService {
        +move()
        +update()
    }

    class SpriteInfo{
        +size:Size
        +position:Point
        +speed: int
    }

    class Size{
        +width:int
        +height:int
    }

    class  Point{
        +x:int
        +y:int
    }
 

    BaseSpriteService <|-- ShootingSpriteService
    BaseSpriteService <|-- BulletService

    ShootingSpriteService <|-- PlayerService
    ShootingSpriteService <|-- EnemyService

    SpriteInfo --> Size
    SpriteInfo --> Point
    BaseSpriteService --> SpriteInfo
```



## Tietojen pysyväistallennus 

Tämä osio on vielä toteuttamatta, mutta tietokantaan tallennetaan jatkossa rekisteröityneet käyttäjät ja käyttäjät pelistatistiikat. 

## Ohjaustiedostot 

Sovelluksen globaalit vakiot on tallennettu config.py-tiedostoon. 

Sovellukselle on myös tulossa SQLite-tietokannan alustustiedosto. 


## Päätoiminnallisuudet

Kuvataan seuraavaksi sovelluksen toimintalogiikka muutaman päätoiminnallisuuden osalta sekvenssikaaviona.


## Käyttäjän kirjautuminen 

Toiminnallisuus toteuttamatta 

## Uuden käyttäjän luominen 

Toiminnallisuus toteuttamatta

## Pelin eteneminen 

Pelin ylätasokaavio:

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant PlayerSprite
    participant BulletSprite
    participant EnemySprite

    Main->>Game: aloita peli
    Game->>PlayerSprite:luo pelaaja()
    Game->>EnemySprite: luo viholliset()
    Game->>Game: luo pelisimukka

    loop peli-iteraatio
        PlayerSprite->>Game: liiku ja ammu
        EnemySprite->>Game: liiku ja ammu
        BulletSprite->>Game: liiku
    end
```

Pelin käynnistyminen ja pelaajan toiminnot:

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

Pelin käynnistyminen ja vihollisen toiminnot:

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant EnemySprite
    participant EnemyService
    participant BulletService
    participant BulletSprite

    Main->>Game: aloita peli
    Game->>EnemySprite:luo viholliset()
    Game->>Game: luo pelisimukka

    loop peli-iteraatio jokainen vihollinen ja luoti
        EnemySprite->>EnemyService: liiku() 
        EnemyService->>EnemyService: päivitä suunta ja sijainti()
        EnemySprite->>Game: piirrä vihollisen sijainti()
        EnemySprite->>EnemyService: arvo luodaanko luoti()
        EnemyService->>BulletService: luo uusi bullet()
        BulletService-->>BulletSprite: uusi bullet sprite()
        BulletService->>BulletService: päivitä luodin sijainti()
        BulletSprite->>Game: piirrä luoti()
    end
```

# Jatkokehitystä vaativat toiminnallisuudet ja rakenteelliset heikkoudet

Toiminnallisuus toteuttamatta