from django.urls import path
from django.contrib.auth import views as auth_views
from user_app import views


app_name = 'user_app'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.CustomRegistrationView.as_view(), name='signup'),
    path("signup_done/", views.CustomRegistrationDoneView.as_view(), name="signup_done"),
    path("signup_confirm/<uidb64>/<token>/",  views.CustomRegistrationConfirmView.as_view(), name="signup_confirm",),
]



