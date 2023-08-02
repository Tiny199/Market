from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *



urlpatterns = [
    path('', index, name="index"),
    path('contact/', contact, name="contact"),
    path('item/<int:pk>/',detail, name='detail'),
    path('sign-up/',signupview,name='sign-up'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login'),
    path('item/new-item', newItemview, name='new-item'),
    path('dashboard',dashboardView,name='dashboard'),
    path('dashboard/<int:pk>/delete', deleteView,name='delete'),
    path('item/<int:pk>/edit', editItemview,name='edit'),
    path('search', searchView,name='search'),
]