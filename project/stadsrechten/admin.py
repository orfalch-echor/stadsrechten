from django.contrib import admin
from .models import Stad
from .models import Verlener
from .models import Titel
from .models import Land
from .models import Provincie
from .models import Bezoek
from .models import Spoor


@admin.register(Stad)
class StadAdmin(admin.ModelAdmin):
    pass


@admin.register(Verlener)
class VerlenerAdmin(admin.ModelAdmin):
    pass


@admin.register(Titel)
class TitelAdmin(admin.ModelAdmin):
    pass


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    pass


@admin.register(Provincie)
class ProvincieAdmin(admin.ModelAdmin):
    pass


@admin.register(Bezoek)
class BezoekAdmin(admin.ModelAdmin):
    pass


@admin.register(Spoor)
class SpoorAdmin(admin.ModelAdmin):
    pass
