from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view, logout_get

app_name = 'account'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('my_account/', views.my_account, name='my_account'),
    path('ticket-details/<int:ticket_id>/', views.ticket_details, name='ticket_details'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('logout-get/', logout_get, name='logout_get'),  # Optional GET logout URL
]
