from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.registrar_usuario, name='register_user'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='home'), name='login_user'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout_user'),
]