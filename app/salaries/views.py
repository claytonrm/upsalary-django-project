from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Salary, Payee
from .serializers import SalarySerializer


class SalaryView(APIView):

    def post(self, request, format=None):
        serializer = SalarySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(None, status=status.HTTP_201_CREATED)
