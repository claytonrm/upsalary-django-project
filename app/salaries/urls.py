from django.urls import path

from .views import SalaryDetail, SalaryList

urlpatterns = [
    path('', SalaryList.as_view()),
    path('<int:pk>/', SalaryDetail.as_view()),
]
