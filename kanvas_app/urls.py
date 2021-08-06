from django.urls import path

from .views import (
    AccountsView,
    ActivitiesView,
    CoursesRetrieveView,
    CoursesView,
    LoginView,
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', AccountsView.as_view()),
    path('api/courses/', CoursesView.as_view()),
    path('api/courses/<int:course_id>/', CoursesRetrieveView.as_view()),
    path('api/courses/<int:course_id>/registrations/', CoursesView.as_view()),
    path('api/activities/', ActivitiesView.as_view()),
]
