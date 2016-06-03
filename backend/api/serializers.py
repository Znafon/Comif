from .models import Client, Categorie, Item

from rest_framework import serializers

class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('nom', 'solde', 'cotisant', 'id')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('nom', 'id', 'nombre', 'prix', 'couleur')

class CategorieSerializer(serializers.HyperlinkedModelSerializer):
    items = serializers.SerializerMethodField()

    def get_items(self, obj):
        items = obj.item_set.filter(disponible_a_la_vente = True)
        serializer = ItemSerializer(items, many = True)
        return serializer.data

    class Meta:
        model = Categorie
        fields = ('nom', 'id', 'items')
