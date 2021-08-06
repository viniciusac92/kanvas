from django.urls import path

from .views import AccountsView, Courses, CoursesRetrieveView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', AccountsView.as_view()),
    path('api/courses/', Courses.as_view()),
    path('api/courses/<int:course_id>/', CoursesRetrieveView.as_view()),
    path('api/courses/<int:course_id>/registrations/', Courses.as_view()),
]
