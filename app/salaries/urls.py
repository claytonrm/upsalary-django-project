from django.urls import path

from .views import SalaryList, SalaryDetail


urlpatterns = [
    path("api/salaries/", SalaryList.as_view()),
    path("api/salaries/<int:pk>/", SalaryDetail.as_view()),
]
