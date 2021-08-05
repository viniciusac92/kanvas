from django.urls import path

from .views import CoursesView

urlpatterns = [
    path('courses/', CoursesView.as_view()),
    path('courses/<int:course_id>/registrations/', CoursesView.as_view()),
]
