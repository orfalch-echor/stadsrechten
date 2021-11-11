from django.urls import path

from . import views

app_name = "stadsrechten"

urlpatterns = [
    path('', views.index, name='index'),
    path('find/', views.find, name='find'),
    path('stad/<int:stad_id>/', views.stad, name='stad'),
    path('verlener/<int:verlener_id>/', views.verlener, name='verlener'),
    path('steden/', views.steden, name='steden'),
]
