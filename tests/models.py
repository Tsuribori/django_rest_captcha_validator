from django.db import models

class Item(models.Model):
    item_text = models.CharField(max_length=64)
