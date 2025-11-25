from django.urls import path
from . import views


app_name = 'plants'

urlpatterns = [
    path('all/', views.all_view, name='all_view'),
    path('plants/new/', views.add_view, name="add_view"),
    path('<plant_id>/detail/', views.plant_detail_view, name='plant_detail_view'),
    path('<plant_id>/update/', views.update_view, name='update_view'),
    path('<plant_id>/delete/', views.delete_view, name='delete_view'),
    path('search/', views.search_view, name='search_view'),
    path('comment/add/<plant_id>/', views.add_comment_view, name="add_comment_view"),
    path('plants/by/country/<country_id>/', views.plants_by_country,name='plants_by_country'),
]