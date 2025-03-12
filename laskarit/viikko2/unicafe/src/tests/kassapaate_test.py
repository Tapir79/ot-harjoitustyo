import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(10000)

# Luodun kassapäätteen rahamäärä ja myytyjen lounaiden määrä on oikea (rahaa 1000 euroa, lounaita myyty 0)

    def test_kassapaatteen_saldo_luotu_oikein(self):
        saldo = self.kassapaate.kassassa_rahaa_euroina()
        self.assertEqual(saldo, 1000.0)
        
    def test_kassapaatteen_lounaat_luotu_oikein(self):
        lounaat = self.kassapaate.edulliset + self.kassapaate.maukkaat
        self.assertEqual(lounaat, 0)

# Käteisosto toimii sekä edullisten että maukkaiden lounaiden osalta
    def test_edullisten_lounaiden_kateisosto_toimii_oikein(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_maukkaiden_lounaiden_kateisosto_toimii_oikein(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004)

# Jos maksu riittävä: kassassa oleva rahamäärä kasvaa lounaan hinnalla ja vaihtorahan suuruus on oikea

    def test_edullisten_lounaiden_kateisoston_vaihtoraha_on_oikein(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(300)
        self.assertEqual(vaihtoraha, 60)

    def test_maukkaiden_lounaiden_kateisoston_vaihtoraha_on_oikein(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(450)
        self.assertEqual(vaihtoraha, 50)


 # Jos maksu on riittävä: myytyjen lounaiden määrä kasvaa   
    def test_edullisten_lounaiden_kateisostolla_myytyjen_lounaiden_maara_kasvaa(self):
        self.kassapaate.syo_edullisesti_kateisella(240)
        self.assertEqual(self.kassapaate.edulliset, 1)
 
    def test_maukkaiden_lounaiden_kateisostolla_myytyjen_lounaiden_maara_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

# Jos maksu ei ole riittävä: kassassa oleva rahamäärä ei muutu, kaikki rahat palautetaan vaihtorahana ja myytyjen lounaiden määrässä ei muutosta
    def test_edullisten_kateismaksun_ollessa_riittamaton_rahat_palautetaan(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(palautus, 200)

    def test_edullisten_maksun_ollessa_riittamaton_kassan_saldo_ei_muutu(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
    
    def test_maukkaiden_kateismaksun_ollessa_riittamaton_rahat_palautetaan(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(palautus, 200)

    def test_maukkaiden_kateismaksun_ollessa_riittamaton_kassan_saldo_ei_muutu(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)


# seuraavissa testeissä tarvitaan myös Maksukorttia jonka oletetaan toimivan oikein
# Korttiosto toimii sekä edullisten että maukkaiden lounaiden osalta
    def test_korttiosto_toimii_edullisten_lounaiden_osalta(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 97.6)

    def test_korttiosto_toimii_maukkaiden_lounaiden_osalta(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.maksukortti.saldo_euroina(), 96.0)

    def test_syo_edullisesti_kortilla_ei_muuta_kassan_saldoa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000)

    def test_syo_maukkaasti_kortilla_ei_muuta_kassan_saldoa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(),1000)


# Jos kortilla on tarpeeksi rahaa, veloitetaan summa kortilta ja palautetaan True
    def test_syo_edullisesti_kortilla_onnistuu_jos_saldo_riittaa(self):
        palautus = self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(palautus, True)

    def test_syo_maukkaasti_kortilla_onnistuu_jos_saldo_riittaa(self):
        palautus = self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(palautus, True)


# Jos kortilla on tarpeeksi rahaa, myytyjen lounaiden määrä kasvaa
    def test_syo_edullisesti_kortilla_kasvattaa_lounaiden_maara_jos_saldo_riittaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_syo_maukkaasti_kortilla_kasvattaa_lounaiden_maara_jos_saldo_riittaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)
        self.assertEqual(self.kassapaate.maukkaat, 1)

# Jos kortilla ei ole tarpeeksi rahaa, kortin rahamäärä ei muutu, myytyjen lounaiden määrä muuttumaton ja palautetaan False
    def test_syo_edullisesti_kortilla_epaonnistuu_jos_saldo_ei_riita(self):
        kortti = Maksukortti(10)
        palautus = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(palautus, False)

    def test_syo_maukkaasti_kortilla_epaonnistuu_jos_saldo_ei_riita(self):
        kortti = Maksukortti(10)
        palautus = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(palautus, False)

# Kassassa oleva rahamäärä ei muutu kortilla ostettaessa
    def test_syo_edullisesti_kortilla_ei_kasvata_lounaiden_maara_jos_saldo_ei_riita(self):
        kortti = Maksukortti(10)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kortilla_ei_kasvata_lounaiden_maara_jos_saldo_ei_riita(self):
        kortti = Maksukortti(10)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.maukkaat, 0)

# Kortille rahaa ladattaessa kortin saldo muuttuu ja kassassa oleva rahamäärä kasvaa ladatulla summalla  
    def test_kortin_saldo_kasvaa_ladatulla_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 101)
    
    def test_kassan_saldo_kasvaa_kortille_ladatulla_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1001)

# Kortille rahaa ladattaessa kortin saldo ei muutu ja kassan saldo ei muutu, jos ladataan negatiivinen summa
    def test_kortin_saldo_ei_kasva_ladatulla_negatiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 100)
    
    def test_kassan_saldo_ei_kasva_kortille_ladatulla_negatiivisella_summalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
