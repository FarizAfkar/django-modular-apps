from django.urls import path
from modules import views

app_name = 'modules'

urlpatterns = [
    path('', views.home, name='home'),
    path('upgrade/<str:name>', views.upgrade, name='upgrade'),
    path('unistall/<str:name>', views.uninstall, name='uninstall'),
]
