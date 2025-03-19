from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('CN/', views.pegar_dados_CN, name='dados_CN'),
]
