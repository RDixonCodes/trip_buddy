from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('user/create', views.create_user),
    path('user/login', views.login),
    path('user/logout', views.logout),
    path('user/hello', views.dashboard),
    path('user/trip', views.trip),
    path('new/trip', views.create_trip),
    path('trip/<int:trip_id>/edit', views.edit_trip),
    path('edit/<int:trip_id>/trip', views.updated_trip),
    path('trip/<int:trip_id>/view', views.view_trip),
    path('remove/<int:trip_id>', views.delete_trip)
]