from django.urls import path
from api.views import add_source, list_sources, get_news_by_source

urlpatterns = [
    path('sources/', add_source, name="add_source"),  # Adicionar fonte
    path('sources/list/', list_sources, name="list_sources"),  # Listar fontes
    path('news/<int:source_id>/', get_news_by_source, name="get_news_by_source"),  # Notícias de uma fonte específica
]
