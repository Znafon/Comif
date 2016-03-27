from .models import Client, Categorie, Item, Transaction
from .serializers import ClientSerializer, CategorieSerializer
from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from django.shortcuts import get_object_or_404
from decimal import Decimal

# Create your views here.

class ClientsList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_view_name(self):
        return 'Liste des utilisateurs'

class ClientDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   generics.GenericAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        client = self.get_object()
        amount = Decimal(request.data.get('amount', '0'))
        client.solde += amount
        client.save()
        client.refresh_from_db()
        serializer = ClientSerializer(client)
        return Response(serializer.data)


@api_view(['GET'])
def login(request):
    return Response({'detail': 'Logged successfully'})

@api_view(['GET'])
def commande(request, pk):
    client = get_object_or_404(Client, pk=pk)

    items = {get_object_or_404(Item, pk=key): int(nombre[0]) for key, nombre in dict(request.GET).iteritems()}

    cout = sum([item.prix*nombre for item, nombre in items.iteritems()])

    for item, nombre in items.iteritems():
        item.nombre -= nombre
        item.save()
        item.refresh_from_db()

    client.solde -= cout
    client.save()
    client.refresh_from_db()
    serializer = ClientSerializer(client)

    transaction = Transaction(type_de_la_transaction = "Achat", prix = cout, client=client)
    transaction.save()
    
    return Response(serializer.data)


class InventaireList(generics.ListAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
