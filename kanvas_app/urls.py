from django.urls import path

from .views import AccountsView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', AccountsView.as_view()),
]
