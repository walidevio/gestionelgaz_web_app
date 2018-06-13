# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#for the user class
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
#from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import UserManager


#for the user manager class
from  django.contrib.auth.base_user import BaseUserManager


class Admin(models.Model):
    user_iduser = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='User_idUser', primary_key=True)  # Field name made lowercase.
    wilaya_idwilaya = models.ForeignKey('Wilaya', models.DO_NOTHING, db_column='Wilaya_idWilaya')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Admin'


class Adresse(models.Model):
    idadresse = models.IntegerField(db_column='idAdresse', primary_key=True)  # Field name made lowercase.
    rue = models.CharField(db_column='Rue', max_length=45)  # Field name made lowercase.
    num = models.CharField(db_column='Num', max_length=45)  # Field name made lowercase.
    idzone = models.ForeignKey('Zone', models.DO_NOTHING, db_column='idZone')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Adresse'


class Cartebancaire(models.Model):
    idcarte = models.IntegerField(db_column='idCarte', primary_key=True)  # Field name made lowercase.
    numerocarte = models.CharField(db_column='NumeroCarte', max_length=45)  # Field name made lowercase.
    pin = models.CharField(db_column='PIN', max_length=45)  # Field name made lowercase.
    montant = models.FloatField(db_column='Montant')  # Field name made lowercase.
    iduser = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CarteBancaire'


class Commune(models.Model):
    idcommune = models.IntegerField(db_column='idCommune', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=45)  # Field name made lowercase.
    codepostal = models.CharField(db_column='CodePostal', max_length=45)  # Field name made lowercase.
    wilaya_idwilaya = models.ForeignKey('Wilaya', models.DO_NOTHING, db_column='Wilaya_idWilaya')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Commune'


class CommuneZone(models.Model):
    idcommune = models.ForeignKey(Commune, models.DO_NOTHING, db_column='idCommune', primary_key=True)  # Field name made lowercase.
    zone_idzone = models.ForeignKey('Zone', models.DO_NOTHING, db_column='Zone_idZone')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Commune_Zone'
        unique_together = (('idcommune', 'zone_idzone'),)


class Compteur(models.Model):
    matricule = models.CharField(db_column='Matricule', primary_key=True, max_length=45)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Compteur'


class Employe(models.Model):
    user_iduser = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='User_idUser', primary_key=True)  # Field name made lowercase.
    zone_idzone = models.ForeignKey('Zone', models.DO_NOTHING, db_column='Zone_idZone')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Employe'


class Facture(models.Model):
    idfacture = models.IntegerField(db_column='idFacture', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    montant = models.FloatField(db_column='Montant')  # Field name made lowercase.
    paye = models.FloatField(db_column='Paye')  # Field name made lowercase.
    creditaa = models.FloatField(db_column='CreditAA')  # Field name made lowercase.
    idtarif = models.ForeignKey('Tarif', models.DO_NOTHING, db_column='idTarif')  # Field name made lowercase.
    matricule = models.ForeignKey('Compteur', models.DO_NOTHING, db_column='Matricule')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Facture'


class Index(models.Model):
    idindex = models.IntegerField(db_column='idIndex', primary_key=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.
    releve = models.IntegerField(db_column='Releve')  # Field name made lowercase.
    matricule = models.ForeignKey('Compteur', models.DO_NOTHING, db_column='Matricule')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Index'


class Raccordement(models.Model):
    iduser = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='idUser', primary_key=True)  # Field name made lowercase.
    idadresse = models.ForeignKey('Adresse', models.DO_NOTHING, db_column='idAdresse')  # Field name made lowercase.
    matricule = models.ForeignKey('Compteur', models.DO_NOTHING, db_column='Matricule')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Raccordement'
        unique_together = (('iduser', 'idadresse', 'matricule'),)


class Reclamation(models.Model):
    idreclamation = models.IntegerField(db_column='idReclamation', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45)  # Field name made lowercase.
    texte = models.TextField(db_column='Texte', blank=True, null=True)  # Field name made lowercase.
    prisecharge = models.CharField(db_column='PriseCharge', default='N', max_length=1)  # Field name made lowercase.
    user_iduser = models.ForeignKey('UserProfile', models.DO_NOTHING, db_column='User_idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Reclamation'


class Remise(models.Model):
    type = models.CharField(db_column='Type', max_length=2)  # Field name made lowercase.
    taux = models.FloatField(db_column='Taux')  # Field name made lowercase.
    date = models.DateField(db_column='Date')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Remise'


class Tarif(models.Model):
    idtarif = models.AutoField(db_column='idTarif', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='Code', max_length=45)  # Field name made lowercase.
    coef = models.FloatField(db_column='Coef')  # Field name made lowercase.
    droitfixe = models.FloatField(db_column='DroitFixe')  # Field name made lowercase.
    taxehabitation = models.FloatField(db_column='TaxeHabitation')  # Field name made lowercase.
    timbre = models.FloatField(db_column='Timbre')  # Field name made lowercase.
    primefixe = models.FloatField(db_column='PrimeFixe')  # Field name made lowercase.
    tva = models.FloatField(db_column='TVA')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tarif'


class Tranceh(models.Model):
    tranceh = models.IntegerField(db_column='Tranceh', primary_key=True)  # Field name made lowercase.
    prixunit = models.FloatField(db_column='PrixUnit')  # Field name made lowercase.
    quantite = models.FloatField(db_column='Quantite')  # Field name made lowercase.
    idtarif = models.ForeignKey(Tarif, models.DO_NOTHING, db_column='idTarif')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tranceh'
        unique_together = (('tranceh', 'idtarif'),)







class User(AbstractBaseUser, PermissionsMixin):
    iduser = models.AutoField(db_column='idUser', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=45)  # Field name made lowercase.
    prenom = models.CharField(db_column='Prenom', max_length=45)  # Field name made lowercase.
    datenaissance = models.DateField(db_column='DateNaissance')  # Field name made lowercase.
    email = models.CharField(db_column='E-mail', unique=True, max_length=45)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    username = models.CharField(db_column='Pseudo', unique=True, max_length=45, blank=True, null=True)  # Field name made lowercase.
    last_login = models.DateField(db_column='last_login', blank=True, null=True)
    password = models.CharField(db_column='MotPasse', max_length=45, blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=2)  # Field name made lowercase.

    objects = UserManager()



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        db_table = 'User'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.nom, self.prenom)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.nom

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Wilaya(models.Model):
    idwilaya = models.IntegerField(db_column='idWilaya', primary_key=True)  # Field name made lowercase.
    nom = models.CharField(db_column='Nom', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Wilaya'


class Zone(models.Model):
    idzone = models.IntegerField(db_column='idZone', primary_key=True)  # Field name made lowercase.
    nomagence = models.CharField(db_column='NomAgence', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Zone'
