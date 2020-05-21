from django.urls import path

from .views import SalaryView


urlpatterns = [
    path("api/salaries/", SalaryView.as_view()),
]
