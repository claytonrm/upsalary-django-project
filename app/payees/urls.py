from django.urls import path

from .views import PayeeDetail, PayeeList

urlpatterns = [
    path("api/users/", PayeeList.as_view()),
    path("api/users/<int:pk>/", PayeeDetail.as_view())
]
