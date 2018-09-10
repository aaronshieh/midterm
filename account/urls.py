from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.new_account, name="new"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('deposit/<int:id>', views.deposit, name="deposit"),
]