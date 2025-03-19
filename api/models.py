from django.db import models
from django.db import models


class News(models.Model):
    name = models.CharField(max_length=200)  # Título da notícia
    content = models.TextField()  # Conteúdo completo da notícia
    date = models.DateTimeField()  # Data da postagem (pode ser preenchida via scraping)
    author = models.CharField(max_length=200, blank=True, null=True)  # Nome do autor (pode ser desconhecido)
    font = models.CharField(max_length=200)  # Fonte da notícia

    def __str__(self):
        return self.name
