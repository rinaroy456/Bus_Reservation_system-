from django.urls import path
from . import views

app_name = 'bookTicket'
urlpatterns = [
    path('book-ticket/<str:bus_id>/', views.book_ticket, name='bookTicket'),
]
