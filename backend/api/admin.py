# coding=utf-8

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Client, Item, Categorie

from actions import export_as_csv_action

class SoldeFilter(admin.SimpleListFilter):
    title = 'solde'
    parameter_name = 'solde'

    def lookups(self, request, model_admin):
        return (
                ('+', 'Positif'),
                ('-', u'Négatif')
               )

    def queryset(self, request, queryset):
        if self.value() == '+':
            return queryset.filter(solde__gt = 0)
        if self.value() == '-':
            return queryset.filter(solde__lte = 0)

class CategorieFilter(admin.SimpleListFilter):
    title = "catégorie"
    parameter_name = 'categorie'

    def lookups(self, request, model_admin):
        categories = Categorie.objects.all().order_by('nom')
        return map(lambda c: [c.id, c.nom], categories)

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(categorie_id = self.value())

class NombreFilter(admin.SimpleListFilter):
    title = 'disponibilité'
    parameter_name = 'quantite'

    def lookups(self, request, model_admin):
        return (
                 ('disponible', 'En stock'),
                 ('indisponible', 'En rupture de stock')
        )

    def queryset(self, request, queryset):
        if self.value() == 'disponible':
            return queryset.filter(nombre__gt = 0)
        if self.value() == 'indisponible':
            return queryset.filter(nombre__lte = 0)

class AvailableFilter(admin.SimpleListFilter):
    title = 'en vente'
    parameter_name = 'available'

    def lookups(self, request, model_admin):
        return (
            ('available', 'En vente'),
            ('not_available', 'Pas en vente')
        )

    def queryset(self, request, queryset):
        if self.value() == 'available':
            return queryset.filter(disponible_a_la_vente = True)
        if self.value() == 'not_available':
            return queryset.filter(disponible_a_la_vente = False)

@admin.register(Client)
class ClientAdmin(SimpleHistoryAdmin):
    list_display = ('nom', 'solde')
    search_fields = ['nom', 'solde']
    list_filter = (SoldeFilter,)
    actions = [export_as_csv_action("Exporter la sélection en CSV",
                                fields=['nom', 'solde'])]

@admin.register(Item)
class ItemAdmin(SimpleHistoryAdmin):
    search_fields = ('nom', 'prix')
    list_filter = (CategorieFilter, NombreFilter, AvailableFilter)

    fields = (
        ('nom', 'disponible_a_la_vente'),
        ('prix'),
        ('nombre'),
        ('categorie'),
        ('couleur')
    )

    actions = [export_as_csv_action("Exporter la sélection en CSV",
                                    fields=['nom', 'nombre', 'prix', 'disponible_a_la_vente', 'categorie'])]

    def get_list_display(self, request):
        if request.GET.get('categorie', False):
            list_display = ('nom', 'nombre', 'prix')
        else:
            list_display = ('nom', 'nombre', 'prix', 'categorie')
        return list_display

admin.site.register(Categorie)
