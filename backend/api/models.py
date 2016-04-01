 # coding=utf-8

from django.db import models
from simple_history.models import HistoricalRecords
from colorfield.fields import ColorField

class Promotion(models.Model):
    nom = models.CharField(max_length = 30)

    def __unicode__(self):
        return unicode(self.nom)

class Client(models.Model):
    nom = models.CharField(max_length = 300)
    solde = models.DecimalField(max_digits = 5, decimal_places = 2)
    history = HistoricalRecords()

    promotion = models.ForeignKey(Promotion, models.PROTECT, default = 1)

    class Meta:
        ordering = ['nom']

    def __unicode__(self):
        return unicode(self.nom)

class Categorie(models.Model):
    nom = models.CharField(max_length = 100)

    def __unicode__(self):
        return unicode(self.nom)

class Item(models.Model):
    nom = models.CharField(max_length = 100)
    disponible_a_la_vente = models.BooleanField(default = True)
    nombre = models.IntegerField()
    prix = models.DecimalField(max_digits = 5, decimal_places = 2)
    couleur = ColorField(default='#00C0EF')
    history = HistoricalRecords()

    categorie = models.ForeignKey(Categorie, models.CASCADE)


    class Meta:
        verbose_name = "item"
        verbose_name_plural = u"inventaire"

        ordering = ['categorie', 'nom']

    def __unicode__(self):
        return u'{nom} - {nombre}'.format(nom = self.nom, nombre = self.nombre)
