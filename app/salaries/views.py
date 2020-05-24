from django.db.models import Avg, Max, Min
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Salary
from .serializers import SalarySerializer, SalarySummarySerializer


class SalaryList(generics.ListAPIView):
    model = Salary
    serializer_class = SalarySerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(type=openapi.TYPE_OBJECT),
                "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                "taxes": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        )
    )
    def post(self, request, format=None):
        serializer = SalarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        headers = self.get_success_headers(request, serializer.data)
        return Response(None, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        queryset = Salary.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        return self.filter_by('user_id', user_id, queryset)

    def filter_by(self, param, value, queryset):
        if value is not None:
            queryset = queryset.filter(**{param: value})
        return queryset

    def get_success_headers(self, request, data):
        try:
            return {'Location': str(f"{request.build_absolute_uri()}{data['id']}/")}
        except (TypeError, KeyError):
            return {}


class SalaryDetail(APIView):

    def get(self, request, pk, format=None):
        if pk is not None:
            salary = self.get_object(pk)
            serializer = SalarySerializer(salary)
            return Response(serializer.data)

    def delete(self, request, pk, format=None):
        salary = self.get_object(pk)
        salary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "user": openapi.Schema(type=openapi.TYPE_OBJECT),
                "amount": openapi.Schema(type=openapi.TYPE_NUMBER),
                "taxes": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        )
    )
    def put(self, request, pk, format=None):
        salary = self.get_object(pk)
        serializer = SalarySerializer(salary, data=request.data, partial=False)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Salary.objects.get(pk=pk)
        except Salary.DoesNotExist:
            raise Http404


class SalarySummaryDetail(APIView):
    serializer_class = SalarySummarySerializer

    def get(self, request):
        agg_salary = Salary.objects.all().aggregate(Avg('amount'), Min('amount'), Max('amount'), Avg('taxes'))
        amount = {
            "average": agg_salary['amount__avg'],
            "lowest": agg_salary['amount__min'],
            "highest": agg_salary['amount__max']
        }
        taxes = {"average": agg_salary['taxes__avg']}
        return Response({"amount": amount, "taxes": taxes})
