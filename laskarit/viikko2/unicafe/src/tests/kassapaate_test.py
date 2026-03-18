import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapääte(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_konstruktori_asettaa_saldon_oikein_luodulle_kassapäätteelle(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_konstruktori_asettaa_lounaiden_määrän_oikein(self):
        lounaat = self.kassapaate.edulliset + self.kassapaate.maukkaat

        self.assertEqual(lounaat, 0)

    def test_käteis_lounaan_osto_nostaa_edullisten_lounaiden_määrää(self):
        self.kassapaate.syo_edullisesti_kateisella(240)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_käteis_lounaan_osto_nostaa_maukkaiden_lounaiden_määrää(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_riittävä_käteis_edulliseen_lounaaseen_kasvattaa_kassaa_lounaan_hinnalla(self):
        self.kassapaate.syo_edullisesti_kateisella(240)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)

    def test_riittävä_käteis_maukkaaseen_lounaaseen_kasvattaa_kassaa_lounaan_hinnalla(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)

    def test_riittävä_käteis_edulliseen_lounaaseen_saa_oikean_vaihtorahan(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(300)

        self.assertEqual(vaihtoraha, 60)

    def test_riittävä_käteis_maukkaaseen_lounaaseen_saa_oikean_vaihtorahan(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(450)

        self.assertEqual(vaihtoraha, 50)

    def test_korttiosto_toimii_edullisen_lounaan_ostossa(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.kortti))

    def test_korttiosto_toimii_maukkaan_lounaan_ostossa(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.kortti))

    def test_kassan_rahamäärä_ei_muutu_edullisen_korttiostolla(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_rahamäärä_ei_muutu_maukkaan_korttiostolla(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_myytyjen_edullisten_määrä_nousee_kun_korttiosto_onnistuu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_myytyjen_maukkaiden_määrä_nousee_kun_korttiosto_onnistuu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_myytyjen_edullisten_määrä_ei_nouse_jos_ei_tarpeeksi_rahaa_kortilla(self):
        self.kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_myytyjen_maukkaiden_määrä_ei_nouse_jos_ei_tarpeeksi_rahaa_kortilla(self):
        self.kortti = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_jos_kortilla_ei_tarpeeksi_rahaa_maukaaseen_palautetaan_false(self):
        self.kortti = Maksukortti(100)

        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(self.kortti))

    def test_jos_kortilla_ei_tarpeeksi_rahaa_edulliseen_palautetaan_false(self):
        self.kortti = Maksukortti(100)

        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(self.kortti))

    def test_jos_kortilla_ei_tarpeeksi_rahaa_edulliseen_kortin_rahamäärä_ei_muutu(self):
        self.kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 100)

    def test_jos_kortilla_ei_tarpeeksi_rahaa_maukkaaseen_kortin_rahamäärä_ei_muutu(self):
        self.kortti = Maksukortti(100)
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 100)

    def test_jos_kortilla_tarpeeksi_rahaa_edulliseen_kortin_rahamäärä_muuttuu(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 760)

    def test_jos_kortilla_tarpeeksi_rahaa_maukkaaseen_kortin_rahamäärä_muuttuu(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo, 600)

    def test_kortin_saldo_muuttuu_rahaa_ladattaessa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 100)

        self.assertEqual(self.kortti.saldo, 1100)

    def test_kassapäätteen_saldo_muuttuu_rahaa_ladattaessa_kortille(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 100)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100100)

    def test_jos_käteinen_ei_riitä_edulliseen_ei_kassan_rahamäärä_muutu(self):
        self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_jos_käteinen_ei_riitä_maukkaaseen_ei_kassan_rahamäärä_muutu(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kortille_ei_voi_ladata_negatiivista_summaa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -100)

        self.assertEqual(self.kortti.saldo, 1000)

    def test_kassa_palauttaa_rahaa_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)