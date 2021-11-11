from django.shortcuts import render
from .models import Bezoek
from .models import Stad
from .models import Verlener
import random


def index(request):
    """
    De hoofdpagina.
    Hier wordt een standaard boodschap getoond, met 3 random gekozen
    items van Stad of Verlener model, die in de header wordt getoond.
    """

    steden = list(
        Stad.objects.order_by('verleendatum')
    )
    verlener = list(
        Verlener.objects.all()
    )

    iois = []
    if (len(verlener) + len(steden)) >= 3:
        iois = random.sample(verlener + steden, 3)

    context = {
        'steden': steden,
        'iois': iois,
    }
    return render(request, 'stadsrechten/index.html', context)


def stad(request, stad_id):
    """
    Detail view van een stad.
    """

    stad = Stad.objects.get(pk=stad_id)
    bezoek = Bezoek.objects.filter(
        stad__pk=stad_id,
    ).first()
    sporen = stad.spoor_set.all()
    land = dict()

    if stad.verlener:
        land = stad.verlener.land_set.all()

    context = {
        'stad': stad,
        'bezoek': bezoek,
        'land': land,
        'sporen': sporen,
    }
    return render(request, 'stadsrechten/stad.html', context)


def steden(request):
    """
    List view van de steden.
    In de listing is te zien wanneer een stad stadsrechten heeft (flag)
    of niet (circle).
    """

    steden = list(
        Stad.objects.filter(
            banned=0
        ).order_by('naam')
    )
    context = {
        'steden': steden,
    }
    return render(request, 'stadsrechten/steden.html', context)


def find(request):
    """
    Zoekt de stad (met ignorecase startswith) die de gebruiker
    in het zoekveld in geeft.
    Het resultaat wordt naar de listing template gestuurd en geeft
    dus een gefilterde output van de steden listing.
    """

    query = request.GET.get("q")
    steden = list(
        Stad.objects.filter(
            naam__istartswith=query,
        )
    )
    context = {
       'steden': steden,
    }
    return render(request, 'stadsrechten/steden.html', context)


def verlener(request, verlener_id):
    """
    Detail view van de Verlener
    """

    verlener = Verlener.objects.get(
        pk=verlener_id
    )
    steden = list(Stad.objects.filter(
        verlener__id=verlener_id
    ))

    context = {
        'verlener': verlener,
        'steden': steden,
    }
    return render(request, 'stadsrechten/verlener.html', context)
