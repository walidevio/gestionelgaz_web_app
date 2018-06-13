from django.urls import path, include

from sonelgazapp.views import *
from . import views
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('home/', home, name='home'),
    path('reclamation/', reclamation, name='reclamation'),
    path('factures/', factures, name='factures'),
    path('reclam/', work_reclam, name='work_rec'),
    path('racc/', work_racc, name='work_racc'),
    path('demande_rac/', raccordement, name='demande_rac'),
    path('demande_done/', demande_done, name='demande_done'),
    path('carte/', carte_bancaire, name = 'carte'),
    path('good_job/', good_job, name='good_job'),
    path('facture_paye/', facture_paye, name='facture_paye'),
    path('idx/', idx, name='idx'),
    path('factures/<int:id_facture>/', det_facture, name='det_facture')

]