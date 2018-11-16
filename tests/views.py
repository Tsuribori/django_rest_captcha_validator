from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
