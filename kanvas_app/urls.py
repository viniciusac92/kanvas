from django.urls import path

urlpatterns = [
    path('login/', example_view.as_view()),
    path('protected/', example_view.as_view()),
]
