# Arkkitehtuurikuvaus

## Rakenne 

Pelin rakenne neudattaa seuraavanlaista kolmikerrosarkkitehtuuria: 

```mermaid
graph TD
    UI[UI - Pygame] --> Services
    UI[UI - Pygame] --> Utils
    Services[Services - Logiikka] --> Models
    Services --> Repositories[Repositories]
    Repositories --> Entities[Entities]

```

- ui-pakkaus sisältää käyttöliittymän eli pygame-osuuden 
- services-pakkaus sisältää pelilogiikan
- models-pakkaus sisältää luokkia, joita käytetään logiikkapakkauksessa esim. tietojen organisointiin
- utils-pakkaus sisältää nyt UI:sta erotettuja apufunktioita, jotka eivät suoraan kuuluu mihinkään serviceen, mutta logiikka on haluttu erottaa käyttöliittymästä, jotta sitä voi testata.
- repositories-pakkaus vastaa pysyväistallennuksesta sqlite-tietokantaan. 
- entities-pakkaus, jossa on tietokantatauluja vastaavat python-rakenteet eli entiteetit.  

## Käyttöliittymä 

Käyttöliittymä koostuu uuden käyttäjän luomisesta, kirjautumisesta ja itse pelistä. Näkymät sijaitsevat "ui/game_views"-kansiossa, jonne on eristetty kaikki Pygame-koodi. Kansion entrypoint on main.py. Peli käynnistetään src-kansion juuresta, tiedostosta main.py. Aloitusnäkymässä voi siirtyä suoraan pelinäkymään, jolloin pelaajan henkilökohtaisia tuloksia ei tallenneta. Käyttäjä voi myös luoda uuden käyttäjätunnuksen ja kirjautua sisään, jolloin tulokset tallennetaan tietokantaan.   

Käyttöliittymän flowchart-kaavio:
```mermaid
flowchart TD
    StartScreenView -->|Luo uusi käyttäjä| CreateUserView
    CreateUserView -->|Success| StartScreenView
    StartScreenView -->|Login| LoginView
    LoginView -->|Success| StartScreenView
    StartScreenView -->|Aloita peli| Game
```
---

Käyttäjähallintanäkymät:

```mermaid 
classDiagram

    class BaseView {
        +screen
        +run()
        +render()
        +handle_event()
        +handle_keydown()
        +on_submit()
    }

    class CreateUserView {
        +input_boxes
        +on_submit()
    }

    class LoginView {
        +username
        +password
        +user
        +on_submit()
    }

    class StartScreenView {
        +user
        +render()
        +handle_keydown()
    }

    %% Inheritance
    BaseView --|>  CreateUserView 
    BaseView --|>  LoginView 
    BaseView --|>  StartScreenView

```

## Sovelluslogiikka 

Playerservice, bulletservice ja enemyservice, jakavat base-luokan base_sprite_service. Lisäksi player- ja enemyservice perivät shootingSpriteService:n. Base-luokassa on kaikille yhteisiä yleisiä ominaisuuksia, kuten koko, sijainti ja nopeus. 

Service-luokkien ja luokan ja ohjelman muiden osien suhdetta kuvaava luokkakaavio:

```mermaid
classDiagram
    class BaseSpriteService {
        +sprite_info: SpriteInfo
        +increase_speed(amount:int)
        +decrease_speed(amount:int)
    }

    class ShootingSpriteService {
        +move(key)
        +shoot()
        +update()
        +is_dead()
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
        +hit: Hit
        +speed: int   
        +add_hit()
        +is_dead()  
    }

    class Size{
        +width:int
        +height:int
        +get_buffered_size(buffer):Size
    }

    class  Point{
        +x:int
        +y:int
    }

    class  Hit{
        +hitcount:int
        +max_hits:int
    }
 

    BaseSpriteService <|-- ShootingSpriteService
    BaseSpriteService <|-- BulletService

    ShootingSpriteService <|-- PlayerService
    ShootingSpriteService <|-- EnemyService

    SpriteInfo --> Size
    SpriteInfo --> Point
    SpriteInfo --> Hit
    BaseSpriteService --> SpriteInfo
```

### Tasojen generointi

Tasot generoidaan levelservice-luokassa level_config-tiedoston vakioarvojen ohjaamana. 

## Tietojen pysyväistallennus 

Tietokantaan tallennetaan rekisteröityneet käyttäjät ja käyttäjät pelistatistiikat. 

Tietojen pysyväistallennuksen yleiskaavio: 

```mermaid
flowchart TD
    UI[UI View: LoginView / CreateUserView]

    UI <--> US[UserService]
    UI <--> USS[UserStatisticsService]

    US <--> UR[UserRepository]
    USS <--> USR[UserStatisticsRepository]

    UR <--> DB_USERS[SQLite Taulu: users]
    USR <--> DB_STATS[SQLite Taulu: user_statistics]
```


## Ohjaustiedostot 

Sovelluksen globaalit vakiot on tallennettu config.py-tiedostoon. Lisäksi tasojen vakiottiedot on tallennettu level config-tiedostoon. Tasovakioilla ohjataan pelille oikea arvo, esim. vihollisen kestävyys, pelin edetessä. 

Sovellukselle on myös tulossa SQLite-tietokannan alustustiedosto. 


## Päätoiminnallisuudet

Kuvataan seuraavaksi sovelluksen toimintalogiikka muutaman päätoiminnallisuuden osalta sekvenssikaaviona.


## Käyttäjän kirjautuminen  

```mermaid 
sequenceDiagram
    participant Main
    participant StartScreenView
    participant LoginView
    participant UserService
    participant UserRepository
    participant DB

    Main->>StartScreenView: aloita()
    StartScreenView->>LoginView: valitse "Login"
    LoginView->>UserService: tarkista sisäänkirjautuminen
    UserService->>UserRepository: suorita käyttäjän luontilause
    UserRepository->>DB: haet käyttäjä ja varmista, että salasana täsmää
    DB->>UserRepository: palauta käyttäjä_id
    UserRepository->>UserService: palauta käyttäjä_id
    LoginView-->>StartScreenView: palaa aloitusvalikkoon
    StartScreenView->>StartScreenView: odota seuraavaa valintaa


```

## Uuden käyttäjän luominen 

```mermaid 
sequenceDiagram
    participant Main
    participant StartScreenView
    participant CreateUserView
    participant UserService
    participant UserRepository
    participant DB

    Main->>StartScreenView: aloita()
    StartScreenView->>CreateUserView: valitse "Create Account"
    CreateUserView->>UserService: luo uusi käyttäjä
    UserService->>UserRepository: suorita käyttäjän luontilause
    UserRepository->>DB: lisää uusi käyttäjä tietokantaan
    DB->>UserRepository: palauta käyttäjä entiteetti
    UserRepository->>UserService: palauta käyttäjä entiteetti
    CreateUserView-->>StartScreenView: palaa aloitusvalikkoon
    StartScreenView->>StartScreenView: odota seuraavaa valintaa


```

## Pelin eteneminen 

Pelin ylätasokaavio:

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant Level
    participant PlayerSprite
    participant BulletSprite
    participant EnemySprite

    Main->>Game: aloita peli()
    Game->>Level: luo pelitasot()
    Game->>PlayerSprite:luo pelaaja()
    Game->>Game: luo pelisimukka()
    Game->>Game: Aloita 1. taso()
    Game->>EnemySprite: luo viholliset()
    
    loop peli-iteraatio
        PlayerSprite->>Game: liiku ja ammu
        EnemySprite->>Game: liiku ja ammu
        BulletSprite->>Game: liiku
        PlayerSprite->>Main: Pelaaja kuolee. GAME OVER
        EnemySprite->>Level: Viimeinen tason vihollinen kuolee
        Level->>Game: tuhoa vanha taso ja luo uusi taso
    end
```
---

### Pelaajan ja vihollisen perustoiminnot

Pelin käynnistyminen ja pelaajan toiminnot:

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant PlayerSprite
    participant PlayerService
    participant BulletService
    participant BulletSprite

    Main->>Game: aloita peli()
    Game->>PlayerSprite:luo pelaaja()
    Game->>Game: luo pelisimukka()

    loop peli-iteraatio
        PlayerSprite->>PlayerService: painaa "a" / "d"
        PlayerService->>PlayerService: päivitä sijainti
        PlayerSprite->>Game: piirrä pelaajan sijainti
        PlayerSprite->>PlayerService: painaa "SPACE"
        PlayerService->>BulletService: luo uusi bullet
        BulletService->>BulletSprite: uusi bullet sprite
        BulletService->>BulletService: päivitä sijainti
        BulletSprite->>Game: piirrä luoti
    end
```
---
Pelin käynnistyminen ja vihollisen toiminnot:

```mermaid
sequenceDiagram
    participant Main
    participant Game
    participant EnemySprite
    participant EnemyService
    participant BulletService
    participant BulletSprite

    Main->>Game: aloita peli()
    Game->>EnemySprite:luo viholliset()
    Game->>Game: luo pelisimukka()

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
---

### Yhteentörmäystarkistukset:

Pelaajan luoti ja vihollisen luoti

```mermaid

sequenceDiagram
    participant Game
    participant PlayerBullet
    participant EnemyBullet
    participant EnemySprite
    participant HitAnimation

    loop peli-iteraatio
        Game->>PlayerBullet: päivitä sijainti()
        Game->>EnemyBullet: päivitä sijainti()
        Game->>Game: tarkista luotien törmäykset()

        alt pelaajan luodin törmäys vihollisluotiin
            EnemyBullet-->>Game: tuhoa vihollisluoti
            PlayerBullet-->>Game: tuhoa pelaajan luoti
            Game->>HitAnimation: luo pieni räjähdys
        end
    end
```
---

Pelaajan luoti ja viholliset:

```mermaid
sequenceDiagram
    participant Game
    participant PlayerBullet
    participant EnemySprite
    participant HitAnimation
    participant Level

    loop peli-iteraatio
        Game->>PlayerBullet: päivitä sijainti()
        Game->>PlayerBullet: tarkista törmäykset()

        alt törmäys viholliseen
            PlayerBullet-->>EnemySprite: osuma
            EnemySprite->>EnemySprite: lisää osuma viholliselle
            alt vihollinen kuolee
                EnemySprite-->>Game: poista vihollinen ryhmästä
                Game-->>PlayerBullet: poista luoti
                Game->>HitAnimation: luo räjähdys
            end
            alt viimeinen vihollinen tason ryhmässä kuolee
                Game->>Level: Luo uusi taso
                Level->>Level: Tuhoa kaikki luodit
                Level->>Level: Tuhoa kaikki tason viholliset
                Level->>Level: TUhoa kaikki tason animaatiot
                Level->>Level: Nollaa kaikki tasoattribuutit
                Level->>Game: Aloita uusi taso
            end
            
        end  
    end

```
---

Vihollisen  luoti ja pelaaja:

```mermaid
sequenceDiagram
    participant Game
    participant EnemyBullet
    participant PlayerSprite
    participant EnemyBullet
    participant HitAnimation

    loop peli-iteraatio
        Game->>EnemyBullet: päivitä sijainti()
        Game->>EnemyBullet: tarkista törmäykset()

        alt törmäys pelaajaan
            EnemyBullet-->>PlayerSprite: osuma
            PlayerSprite->>PlayerSprite: lisää osuma pelaajalle
            Game-->>EnemyBullet: poista luoti
            Game->>HitAnimation: luo räjähdys
            alt pelaaja kuolee
                PlayerSprite-->>Game: siirry pelin lopetukseen, GAME OVER
            end
        end
    end

```


# Jatkokehitystä vaativat toiminnallisuudet ja rakenteelliset heikkoudet

Toiminnallisuus toteuttamatta