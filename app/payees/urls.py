from django.urls import path

from .views import PayeeDetail, PayeeList

urlpatterns = [
    path('', PayeeList.as_view()),
    path("<int:pk>/", PayeeDetail.as_view())
]
