from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime


class Titel(models.Model):
    """De titel van de verlener van de stadsrechten, zoals Graaf of Bisschop"""

    naam = models.CharField(
        max_length=100,
        unique=True,
        help_text=_('De naam van de titel, zoals Hertog of Graaf.'),
    )
    kroon = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('De naam van de afbeelding van de '
                    'kroon die bij de titel hoort.'),
    )
    copyright = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('De copyright houder van de afbeelding hoort.')
    )

    def __str__(self):
        return self.naam

    @property
    def object_naam(self):
        return 'titel'


class Verlener(models.Model):
    """
    De naam van de verlener van de stadsrechten.
    Dit is over het algemeen de regerende edelman of geestelijke van het land.
    Uiteindelijk komt de autoriteit via de keizer (in het geval van de adel,
    of de paus (in het geval van de geestelijkheid).
    """

    naam = models.CharField(
        max_length=250,
        blank=True,
        help_text=_('De volledige naam van de Verlener, zonder titel(s).'),
    )
    portret = models.URLField(
        blank=True,
        null=True,
        help_text=_('Een URL naar de afbeelding van de verlener.'),
    )
    mainimg = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('De naam van het image die als stadsgezicht gebruikt '
                    'wordt.'),
    )
    synopsis = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Zeer korte beschrijving van de verlener voor de '
                    'indexpagina.'),
    )
    titel = models.ForeignKey(
        Titel,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text=_('De stad waarvoor de de stadsrechten zijn verleend.'),
    )
    wapen = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Naam van de image met het wapen van de verlener.'),
    )
    beschrijving = models.TextField(
        blank=True,
        help_text=_('Een korte biografie van de verlener uit een '
                    'geaccepteerde bron.'),
    )
    copyright = models.CharField(
        max_length=50,
        help_text=_('Copyright tekst bij de afbeelding van de verlener.'),
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='full_name',
                fields=[
                    'naam',
                    'titel'
                ],
            ),
        ]

    def __str__(self):
        return self.naam

    @property
    def object_naam(self):
        return 'verlener'


class Land(models.Model):
    """
    Het land waar de stad bij verlening van de stadsrechten in lag. De meeste
    landen bestaan niet meer, omdat ze zijn opgegaan in provincies of andere
    grotere verbanden en daardoor niet meer als aparte juridische eenheid
    worden gezien.
    """

    naam = models.CharField(
        max_length=250,
        unique=True,
        help_text=_('Naam van de heerlijkheid waar de stad onderdeel '
                    'van was.'),
    )
    landsheer = models.ManyToManyField(
        Verlener,
        help_text=_('De naam van de heer van de heerlijkheid.'),
    )

    class Meta:
        verbose_name = "Land"
        verbose_name_plural = "Landen"

    def __str__(self):
        return self.naam

    @property
    def object_naam(self):
        return 'land'


class Provincie(models.Model):
    """De naam  van de (Nederlandse) provincie."""

    naam = models.CharField(
        max_length=50,
        unique=True,
        help_text=_('Naam van de (huidige) provincie.'),
    )

    def __str__(self):
        return self.naam

    @property
    def object_naam(self):
        return 'provincie'


class Stad(models.Model):
    """
    De stad die de stadsrechten heeft verleend. De definitie van een stad
    is in het kort een nederzetting die via de autoriteit van de keizer of
    de paus bepaalde rechten heeft gekregen, die tegenwoordig als stadsrechten
    worden gezien.
    Dit zijn onder meer het recht tot de hoge rechtspraak, het houden van een
    (jaar/week)markt, het heffen van belasting en het bouwen van een stadsmuur.
    """

    naam = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        help_text=_('Naam van de stad.'),
    )
    verleendatum = models.DateField(
        'verleendatum',
        null=True,
        default=datetime.date.today,
        help_text=_('De eerst bekende en officieel vastgelegde datum van de '
                    'stadsrechten verlening.'),
    )
    verlener = models.ForeignKey(
        Verlener,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('De verlener van de stadsrechten.'),
    )
    provincie = models.ForeignKey(
        Provincie,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('De provincie waarin de stad tegenwoordig ligt.'),
    )
    mainimg = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('De naam van het image voor het stadsgezicht.'),
    )
    synopsis = models.CharField(
        max_length=50,
        blank=True,
        help_text=_('Zeer korte beschrijving van de stad voor de '
                    'indexpagina.'),
    )
    stad = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text=_('De stad is een stad volgens de definitie.'),
    )
    banned = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text=_('De stad wordt wel genoemd in het repertoire, maar '
                    'voldoet niet aan de definitie.'),
    )
    wapen = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('De naam van het image met het stadswapen.'),
    )
    beschrijving = models.TextField(
        blank=True,
        help_text=_('De beschrijving van de stadsverlening volgens het '
                    'repertoire of andere geaccepteerde bron.'),
    )
    latin = models.CharField(
        blank=True,
        max_length=100,
        help_text=_('De latijnse versie van de naam van de stad.'),
    )

    class Meta:
        verbose_name = "Stad"
        verbose_name_plural = "Steden"

    def heeft_klassieke_stadsrechten(self):
        """
        Een stad heeft klassieke stadsrechten wanneer de stad
        daadwerkelijk stadsrechten heeft en de stadsrechten gebaseerd zijn
        op het Brabantse model. Hiervoor is grofweg het jaar 1100 genomen
        """
        if not self.stad or self.banned:
            return False

        if self.verleendatum > datetime.date(1099, 12, 31) and \
           self.verleendatum < datetime.date(1600, 1, 1):
            return True
        return False

    @property
    def object_naam(self):
        return 'stad'

    def __str__(self):
        return self.naam


class Bezoek(models.Model):
    """Het bezoek aan de stad."""

    datum = models.DateField(
        'bezoekdatum',
        blank=True,
        null=True,
        default=datetime.date.today,
        help_text=_('Datum van het eerste bezoek aan de stad.'),
    )
    rating = models.FloatField(
        blank=True,
        null=True,
        default=6.0,
        help_text=_('Beoordeling van het bezoek en de stad.'),
    )
    stad = models.ForeignKey(
        Stad,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=_('De stad die bezocht is.'),
    )
    mainimg = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('Naam van de afbeelding bij het bezoek.'),
    )

    class Meta:
        verbose_name = "Bezoek"
        verbose_name_plural = "Bezoeken"

    def _str__(self):
        return self.stad.naam

    @property
    def object_naam(self):
        return 'bezoek'


class Spoor(models.Model):
    """
    Restanten van de stad uit de tijd van de stadsverlening, of de
    tijd waarin de stadsverlening relevant was. Die periode loopt
    grofweg van 800 tot 1800.
    De meest relevante restanten zijn de restanten die ook al in de
    stad aanwezig waren (als dan niet als restant) ten tijde van de
    stadsrechtenverlening.
    """

    naam = models.CharField(
        max_length=100,
        blank=True,
        help_text=('Naam van het spoor van de stad.'),
    )
    stad = models.ForeignKey(
        Stad,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text=('De stad waar het spoor te vinden is.'),
    )
    image = models.CharField(
        max_length=100,
        blank=True,
        help_text=_('De naam van het image dat bij het spoor hoort.'),
    )
    beschrijving = models.TextField(
        blank=True,
        help_text=_('Beschrijvende tekst bij het spoor en waarom het '
                    'een spoor is.'),
    )
    mlat = models.FloatField(
        null=True,
        blank=True,
        help_text=_('Breedtegraad van het spoor.'),
    )
    mlon = models.FloatField(
        null=True,
        help_text=_('Lengtegraad van het spoor.'),
    )

    class Meta:
        verbose_name = "Spoor"
        verbose_name_plural = "Sporen"

    def __str__(self):
        return self.naam

    @property
    def object_naam(self):
        return 'spoor'
