from django.test import TestCase
from datetime import datetime
from .models import Stad


class StadTestCase(TestCase):

    def setUp(self):
        Stad.objects.create(naam="Wijchen",
                            stad=False,
                            verleendatum=datetime(1599, 12, 31))
        Stad.objects.create(naam="Haarlem",
                            stad=True,
                            verleendatum=datetime(1245, 11, 23))
        Stad.objects.create(naam="Assen",
                            stad=True,
                            verleendatum=datetime(1809, 3, 13))

    def test_klassieke_stadsrechten(self):
        """Controleer of de stad klassieke stadsrechten heeft"""
        wijchen = Stad.objects.get(naam="Wijchen")
        haarlem = Stad.objects.get(naam="Haarlem")
        assen = Stad.objects.get(naam="Assen")
        self.assertFalse(wijchen.heeft_klassieke_stadsrechten())
        self.assertTrue(haarlem.heeft_klassieke_stadsrechten())
        self.assertFalse(assen.heeft_klassieke_stadsrechten())
