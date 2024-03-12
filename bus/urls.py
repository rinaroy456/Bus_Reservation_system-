from django.urls import path,include
from . import views
app_name = 'bus'
urlpatterns  = [
    path('', views.index, name='index'),
    path('search-bus/', views.search_bus, name='searchBus'),
    path('autocomplete_pick/', views.autocomplete_pick, name='pickareas'),
    path('autocomplete_drop/', views.autocomplete_drop, name='dropareas'),
]