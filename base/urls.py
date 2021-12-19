from django.urls import path
from . import views

urlpatterns = [
    path ('login/', views.loginPage, name='login'),
    path ('logout/', views.logoutUser, name='logout'),
    path ('register/', views.registerPage, name='register'),

    path('', views.home, name='home'),
    path('offer/<str:pk>/', views.offer, name='offer'),

    path('create-offer/', views.createOffer, name="create-offer"),
    path('update-offer/<str:pk>/', views.updateOffer, name="update-offer"),
    path('delete-offer/<str:pk>/', views.deleteOffer, name="delete-offer"),
]


