import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_konstruktori_asettaa_saldon_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 12.0)

    def test_saldo_vähenee_oikein_jos_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(200)

        self.assertEqual(self.maksukortti.saldo_euroina(), 8.0)

    def test_saldo_ei_muutu_jos_rahaa_ei_tarpeeksi(self):
        maksukortti = Maksukortti(100)
        maksukortti.ota_rahaa(150)

        self.assertEqual(maksukortti.saldo_euroina(), 1.0)

    def test_metodi_palauttaa_true_jos_rahat_riittävät(self):
        self.assertTrue(self.maksukortti.ota_rahaa(200))

    def test_metodi_palauttaa_false_jos_rahat_eivät_riitä(self):
        self.assertFalse(self.maksukortti.ota_rahaa(2000))