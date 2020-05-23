from django.http import Http404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Salary
from .serializers import SalarySerializer


class SalaryList(generics.ListAPIView):
    model = Salary
    serializer_class = SalarySerializer

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
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
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
