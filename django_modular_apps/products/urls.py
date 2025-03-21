from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('<str:name>', views.home, name='home'),
    path('<str:name>/detail/<str:barcode>', views.detail, name='detail'),
    path('<str:name>/update/<str:barcode>', views.update, name='update'),
    path('<str:name>/delete/<str:barcode>', views.delete, name='delete')
]
