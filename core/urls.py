from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('update-damage/', views.update_damage, name='update_damage'),
    path('toggle-hidden-axie/<int:axie_id>/', views.toggle_hidden_axie, name='toggle_hidden_axie')
]
