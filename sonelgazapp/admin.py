from django.contrib import admin
from .models import *
# Register your models here.






admin.register(Adresse, Cartebancaire, Commune, CommuneZone, Compteur, Employe,
               Facture, Index, Raccordement, Reclamation, Remise, Tarif,
              Tranceh, Wilaya, Zone)(admin.ModelAdmin)