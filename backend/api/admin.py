# coding=utf-8

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Client, Item, Categorie, Promotion, Transaction
from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Sum
from django.db import connection

from actions import export_as_csv_action

class PromotionFilter(admin.SimpleListFilter):
    title = 'promotion'
    parameter_name = 'promotion'

    def lookups(self, request, model_admin):
        promotions = Promotion.objects.all().order_by('nom')
        return map(lambda p: [p.id, p.nom], promotions)

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(promotion_id = self.value())

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
    list_display = ('nom', 'solde', 'promotion')
    search_fields = ['nom', 'solde', 'promotion']
    list_filter = (SoldeFilter,PromotionFilter,)
    actions = [export_as_csv_action("Exporter la sélection en CSV",
                                fields=['nom', 'solde', 'promotion'])]

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

class TransactionChangeList(ChangeList):

    def get_results(self, *args, **kwargs):
        super(TransactionChangeList, self).get_results(*args, **kwargs)
        q = self.result_list.aggregate(prix_total=Sum('prix'))
        self.total = q['prix_total']
        self.chart = self.seven_days_stats()

    def seven_days_stats(self):
        data = ['Ventes (en euros)']
        label_data = ['x']

        # TODO Ajouter un timedelta pour afficher les 7 derniers jours
        truncate_date = connection.ops.date_trunc_sql('day', 'date')
        qs = Transaction.objects.extra({'day':truncate_date})
        dictionnaire = qs.filter(type_de_la_transaction='Achat').values('day').annotate(Sum('prix')).order_by('day')

        for couple in dictionnaire:
            data.append(str(couple['prix__sum']))
            label_data.append(couple['day'].strftime('%d-%m-%Y'))
        return {'data':data,'labels':label_data}



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    change_list_template = 'admin/transaction_change_list.html'
    list_display = ('date', 'client', 'prix', 'type_de_la_transaction')
    date_hierarchy = 'date';
    search_fields = ['type_de_la_transaction',]

    def get_changelist(self, request):
        return TransactionChangeList

    class Meta:
        model=Transaction

admin.site.register(Categorie)
admin.site.register(Promotion)
