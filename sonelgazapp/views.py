from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from  django.http import HttpResponse,Http404
from .models import *
from .forms import *
from django.urls import reverse
import datetime



# Create your views here.
def loginView(request):
    return render(request, 'registration/login.html', context=None)

def home(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    return render(request, 'home.html', context={'is_employee' : is_employee})


@login_required
def reclamation(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    if request.method == 'GET':
        reclamation_form = ReclamationForm(request.user)
        context = ({"reclamation" : reclamation_form,
                    'is_employee': is_employee})
        return render(request, 'reclamation.html', context)
    elif request.method == 'POST':
        reclamation_form = ReclamationForm(request.user, request.POST)
        if reclamation_form.is_valid():
            rec = reclamation_form.save(commit=False)
            rec.user_iduser = request.user
            rec.user_iduser_id = request.user.pk
            rec.save()
            return redirect(reverse('home'))

def work_reclam(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    if request.method == 'GET':
        zone_emp = Employe.objects.get(user_iduser=request.user)
        zone_emp = zone_emp.zone_idzone
        adr = Adresse.objects.filter(idZone=zone_emp)
        reclams = Reclamation.objects.filter(address__in=adr, prisecharge='N')
        context = {'rec' : reclams,
                   'is_employee': is_employee}
        return render(request, 'work_reclam.html', context=context)
    if request.method == 'POST':
        id_rec = request.POST['id_reclamation']
        rec = Reclamation.objects.get(pk=id_rec)
        rec.prisecharge = 'O'
        rec.save()
        return redirect(reverse('work_rec'))

def factures(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    list_fac = Facture.objects.filter(iduser=request.user).order_by('-date')
    context = ({'list_fac' : list_fac,
                'is_employee' : is_employee})
    return render(request, 'factures.html', context=context)

def det_facture(request, id_facture):
    if request.method == 'GET':
        if Employe.objects.filter(user_iduser=request.user).exists():
            is_employee = True
        else:
            is_employee = False
        facture = get_object_or_404(Facture, pk=id_facture)

        context =({'is_employee' : is_employee,
                  'facture' : facture,
                  })

        return render(request, 'detailed_facture.html', context=context)

    if request.method == 'POST':
        n_carte = request.POST['numerocarte']
        carte = Cartebancaire.objects.get(numerocarte=n_carte)
        facture = request.POST['facture']
        carte.montant = carte.montant - Facture.objects.filter(pk=facture).first().montant
        carte.save()
        f = Facture.objects.get(pk=facture)
        f.paye = 'O'
        f.save()
        return redirect(reverse('facture_paye'))

def facture_paye(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    return render(request, 'fac', context={'is_employee': is_employee})

def idx(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False

    if request.method == 'GET':
        releve_form = ReleveForm()

        return render(request, 'releve.html', context={'is_employee' : is_employee,
                                                   'releve' : releve_form})

    if request.method == 'POST':
        releve_form = ReleveForm(request.POST)
        mat = request.POST['matricule']
        compt = Compteur.objects.filter(matricule=mat)[0]
        index = Index(releve=request.POST['releve'], matricule=compt)
        index.save()
        return redirect(reverse('idx'))

def work_racc(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False

    if request.method == 'GET':
        zone_emp = Employe.objects.get(user_iduser=request.user)
        zone_emp = zone_emp.zone_idzone
        adr = Adresse.objects.filter(idZone=zone_emp)
        rac = Raccordement.objects.filter(idadresse__in=adr, matricule='')
        context = {'rac' : rac,
                   'is_employee': is_employee}
        return render(request, 'work_racc.html', context=context)

    if request.method == 'POST':
        id_rac = request.POST['id_rac']
        id_compt = request.POST['id_compt']
        add = Adresse.objects.get(pk=request.POST['id_add'])

        user = User.objects.get(username=request.POST['id_user'])
        type = request.POST['type']
        id_tar = Tarif.objects.get(code=request.POST['id_tar'])
        compteur = Compteur(matricule=id_compt, idaddress=add, iduser=user, type=type, tarif=id_tar)
        compteur.save()
        rac = Raccordement.objects.get(pk=id_rac)
        rac.matricule = id_compt
        rac.save()
        index = Index(matricule=compteur, releve=0, date=datetime.date.today())
        index.save()
        return redirect(reverse('work_racc'))

def raccordement(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False

    if request.method == 'GET':
        context = {'is_employee' : is_employee}
        return render(request, 'raccordement.html', context=context)
    if request.method == 'POST':
        #num rue codep type
        num = request.POST['num']
        rue = request.POST['rue']
        codep = request.POST['codep']
        t = request.POST['type']

        zone = Zone.objects.get(communezone__idcommune__codepostal__exact=codep)
        a, c = Adresse.objects.get_or_create(num=num, rue=rue, idZone=zone)
        r = Raccordement(type=t, iduser=request.user, idadresse=a)
        r.save()
        return redirect(reverse('demande_done'))

def demande_done(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    return render(request, 'demande_done.html', context={'is_employee' : is_employee})

def carte_bancaire(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False

    if request.method == 'GET':
        return render(request, 'carte_bancaire.html', context={'is_employee' : is_employee})

    if request.method == 'POST':
        num = request.POST['numc']
        pin = request.POST['pin']
        montant = request.POST['montant']

        c, d = Cartebancaire.objects.get_or_create(numerocarte=num, pin=pin, montant=montant, iduser=request.user)

        return redirect(reverse('good_job'))

def good_job(request):
    if Employe.objects.filter(user_iduser=request.user).exists():
        is_employee = True
    else:
        is_employee = False
    return render(request, 'good_job.html', context={'is_employee': is_employee})

