import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

# Tehtävä 6: Takaisin testeihin
# Kortin saldo alussa oikein
    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

# Rahan lataaminen kasvattaa saldoa oikein
    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 20.0)

# Rahan ottaminen toimii:
## - Saldo vähenee oikein, jos rahaa on tarpeeksi
    def test_saldo_vahenee_oikein_jos_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)
## - Saldo ei muutu, jos rahaa ei ole tarpeeksi
    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)
## - Metodi palauttaa True, jos rahat riittivät ja muuten False
    def test_jos_raha_riittaa_palautuu_true(self):
        palautus = self.maksukortti.ota_rahaa(900)
        self.assertEqual(palautus, True)
    def test_jos_raha_ei_riita_palautuu_false(self):
        palautus = self.maksukortti.ota_rahaa(1500)
        self.assertEqual(palautus, False)