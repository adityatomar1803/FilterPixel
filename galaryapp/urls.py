from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.RedirectToLoginOrHomeView.as_view(), name='redirect-login-or-home'),
    path('home/', views.Home.as_view(), name='home'),
    path("login/", views.UserLogin.as_view(), name="login"),
    path('get_data/<int:id>/<int:index>', views.get_data, name='get_data'),
    path('logout/', LogoutView.as_view(), name='logout'),
]