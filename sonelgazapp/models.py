
from django.db import models

from django.contrib.auth.models import User

import datetime







class Adresse(models.Model):

    rue = models.CharField(db_column='Rue', max_length=45)  # Field name made lowercase.
    num = models.CharField(db_column='Num', max_length=45)  # Field name made lowercase.
    idZone = models.ForeignKey('Zone', on_delete=models.DO_NOTHING)  # Field name made lowercase.

    def __str__(self):
         return self.num+', '+self.rue


class Cartebancaire(models.Model):
    numerocarte = models.CharField(db_column='NumeroCarte', max_length=45)
    pin = models.CharField(db_column='PIN', max_length=45)
    montant = models.FloatField(db_column='Montant')
    iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)




class Commune(models.Model):
    nom = models.CharField(db_column='Nom', max_length=45)  # Field name made lowercase.
    codepostal = models.CharField(db_column='CodePostal', max_length=45)  # Field name made lowercase.
    wilaya_idwilaya = models.ForeignKey('Wilaya', on_delete=models.DO_NOTHING)  # Field name made lowercase.




class CommuneZone(models.Model):
    idcommune = models.ForeignKey('Commune', on_delete=models.DO_NOTHING)  # Field name made lowercase.
    zone_idzone = models.ForeignKey('Zone', on_delete=models.DO_NOTHING)  # Field name made lowercase.



class Compteur(models.Model):
    matricule = models.CharField(max_length=45, default='')
    idaddress = models.ForeignKey('Adresse', on_delete=models.DO_NOTHING)
    iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.
    tarif = models.ForeignKey('Tarif', on_delete=models.DO_NOTHING)

    def get_nouv_idx(self):
        return Index.objects.filter(matricule=self).order_by('-pk').first()

    def get_ans_idx(self):
        return Index.objects.filter(matricule=self).order_by('-pk').exclude(pk=self.get_nouv_idx().pk).first()

    def get_difference(self):
        return self.get_nouv_idx().releve - self.get_ans_idx().releve

    def get_cons(self):
        return self.get_difference() * self.tarif.coef

    def get_cons_par_tranche(self):
        cons = self.get_cons()
        cons_list = list()
        for t in self.tarif.get_tranches():
            if cons > t.quantite:
                x = [t.quantite,t.prixunit]
                cons_list.append(x)
                cons = cons - t.quantite
            elif cons < t.quantite:
                x = [cons, t.prixunit]
                cons_list.append(x)
                cons = 0
        return cons_list

    def get_rest(self):
        fact = Facture.objects.get(iduser=self.iduser, idaddress=self.idaddress)
        rest = fact.get_biggest_tranche().__len__() - self.get_cons_par_tranche().__len__()
        return range(rest)

    def get_montant_ht(self):
        montant_ht = self.tarif.primefixe
        for x,y in self.get_cons_par_tranche():
            montant_ht = montant_ht + x * y
        return montant_ht

    def get_tva(self):
        result = (self.get_montant_ht() * self.tarif.tva)/100
        return round(result, 2)

    def get_montant_tt_taxe(self):
        result = self.get_montant_ht() + self.get_tva()
        return round(result,2)

class Employe(models.Model):
    user_iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    zone_idzone = models.ForeignKey('Zone', on_delete=models.DO_NOTHING)



class Facture(models.Model):
    iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    idaddress = models.ForeignKey('Adresse', on_delete=models.DO_NOTHING)
    date = models.DateField(db_column='Date')
    montant = models.FloatField(db_column='Montant')
    paye = models.CharField(db_column='Paye', max_length=1)

    def get_compteurs(self):
        compteurs = Compteur.objects.filter(idaddress=self.idaddress)
        return compteurs

    def get_biggest_tranche(self):
        i=0
        for c in self.get_compteurs():
            if c.tarif.get_tranches().count() > i:
                i = c.tarif.get_tranches().count()
        return range(i)

    def get_montant(self):
        x = 0
        for c in self.get_compteurs():
            x = x + c.get_montant_tt_taxe()
        x = x + 50 + 75
        return x

    def get_montant_espece(self):
        return self.get_montant() + 16



class Index(models.Model):
    date = models.DateField(db_column='Date', default=datetime.date.today)
    releve = models.IntegerField(db_column='Releve')
    matricule = models.ForeignKey('Compteur', on_delete=models.DO_NOTHING)



class Raccordement(models.Model):
    TYPE_CHOICES =[('G', 'Gaz'),
                   ('E', 'Electricite'),]
    type = models.CharField(db_column='Type',choices=TYPE_CHOICES, max_length=1)
    iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    idadresse = models.ForeignKey('Adresse', on_delete=models.DO_NOTHING)
    matricule = models.CharField(db_column='Matricule',max_length=45, default='')



class Reclamation(models.Model):
    RECLAMATION_CHOICES = [
        ('coupure', 'Coupure'),
        ('erreur_fac', 'Erreur dans la facture'),
        ('autre', 'Autres'),
    ]
    type = models.CharField(db_column='Type',choices=RECLAMATION_CHOICES, max_length=45)
    texte = models.TextField(db_column='Texte', blank=True, null=True)
    prisecharge = models.CharField(db_column='PriseCharge', max_length=1, default='N')
    user_iduser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.ForeignKey('Adresse', on_delete=models.DO_NOTHING)


class Remise(models.Model):
    type = models.CharField(db_column='Type', max_length=2)  # Field name made lowercase.
    taux = models.FloatField(db_column='Taux')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.



class Tarif(models.Model):
    code = models.CharField(db_column='Code', max_length=45)  # Field name made lowercase.
    coef = models.FloatField(db_column='Coef')  # Field name made lowercase.
    droitfixe = models.FloatField(db_column='DroitFixe')  # Field name made lowercase.
    taxehabitation = models.FloatField(db_column='TaxeHabitation')  # Field name made lowercase.
    timbre = models.FloatField(db_column='Timbre')  # Field name made lowercase.
    primefixe = models.FloatField(db_column='PrimeFixe')  # Field name made lowercase.
    tva = models.FloatField(db_column='TVA')  # Field name made lowercase.

    def get_tranches(self):
        return Tranceh.objects.filter(idtarif=self)


class Tranceh(models.Model):
    prixunit = models.FloatField(db_column='PrixUnit')  # Field name made lowercase.
    quantite = models.FloatField(db_column='Quantite')  # Field name made lowercase.
    idtarif = models.ForeignKey('Tarif', on_delete=models.DO_NOTHING)  # Field name made lowercase.

class Wilaya(models.Model):
    nom = models.CharField(db_column='Nom', max_length=45)  # Field name made lowercase.

class Zone(models.Model):
    nomagence = models.CharField(db_column='NomAgence', max_length=45)  # Field name made lowercase.
    def __str__(self):
        return self.nomagence
