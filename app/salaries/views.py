from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Salary
from .serializers import SalarySerializer


class SalaryList(APIView):

    def post(self, request, format=None):
        serializer = SalarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)

    def get(self, request, format=None):
        salary = Salary.objects.all()
        serializer = SalarySerializer(salary, many=True)
        return Response(serializer.data)


class SalaryDetail(APIView):

    def get(self, request, pk, format=None):
        salary = self.get_object(pk)
        serializer = SalarySerializer(salary)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        salary = self.get_object(pk)
        salary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        salary = self.get_object(pk)
        serializer = SalarySerializer(salary, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Salary.objects.get(pk=pk)
        except Salary.DoesNotExist:
            raise Http404
