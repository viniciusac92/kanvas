from django.urls import path

from .views import (
    AccountsView,
    ActivitiesView,
    CoursesRetrieveView,
    CoursesView,
    LoginView,
    SubmissionEditView,
    SubmissionRetrieveView,
    SubmissionView,
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('accounts/', AccountsView.as_view()),
    path('courses/', CoursesView.as_view()),
    path('courses/<int:course_id>/', CoursesRetrieveView.as_view()),
    path('courses/<int:course_id>/registrations/', CoursesView.as_view()),
    path('activities/', ActivitiesView.as_view()),
    path('activities/<int:activity_id>/submissions/', SubmissionView.as_view()),
    path('submissions/<int:submission_id>/', SubmissionEditView.as_view()),
    path('submissions/', SubmissionRetrieveView.as_view()),
]
