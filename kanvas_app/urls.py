from django.urls import path

from .views import AccountsView, CoursesView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', AccountsView.as_view()),
    path('api/courses/', CoursesView.as_view()),
    path('api/courses/<int:course_id>/registrations/', CoursesView.as_view()),
]
