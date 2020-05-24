from django.urls import path

from .views import SalaryDetail, SalaryList, SalarySummaryDetail

urlpatterns = [
    path('', SalaryList.as_view()),
    path('<int:pk>/', SalaryDetail.as_view()),
    path('describe/', SalarySummaryDetail.as_view())
]
