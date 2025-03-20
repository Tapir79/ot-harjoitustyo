class Kassapaate:

    EDULLINEN_LOUNAS = "edulliset"
    MAUKAS_LOUNAS = "maukkaat"

    def __init__(self):
        self.kassassa_rahaa = 100000
        self.edulliset = 0
        self.maukkaat = 0

    def lisaa_lounas(self, lounas):
        if lounas == self.EDULLINEN_LOUNAS:
                self.edulliset += 1
        else:
            self.maukkaat += 1

    def maksa_kateisella(self, kateinen, maksu, lounas):
        if maksu >= kateinen:
            self.kassassa_rahaa = self.kassassa_rahaa + kateinen
            self.lisaa_lounas(lounas)
            return maksu - kateinen
        else:
            return maksu

    def maksa_kortilla(self, kortti, lounas, maksu):
        if kortti.saldo >= maksu:
            kortti.ota_rahaa(maksu)
            self.lisaa_lounas(lounas)
            return True
        else:
            return False

    def syo_edullisesti_kateisella(self, maksu):
        return self.maksa_kateisella(240, maksu, self.EDULLINEN_LOUNAS)

    def syo_maukkaasti_kateisella(self, maksu):
        return self.maksa_kateisella(400, maksu, self.MAUKAS_LOUNAS)

    def syo_edullisesti_kortilla(self, kortti):
        return self.maksa_kortilla(kortti, self.EDULLINEN_LOUNAS, 240)

    def syo_maukkaasti_kortilla(self, kortti):
        return self.maksa_kortilla(kortti, self.MAUKAS_LOUNAS, 400)

    def lataa_rahaa_kortille(self, kortti, summa):
        if summa >= 0:
            kortti.lataa_rahaa(summa)
            self.kassassa_rahaa += summa
        else:
            return

    def kassassa_rahaa_euroina(self):
        return self.kassassa_rahaa / 100
