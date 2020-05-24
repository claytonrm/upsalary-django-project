from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payee
from .serializers import PayeeSerializer


class PayeeList(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "entry": openapi.Schema(type=openapi.TYPE_STRING),
                "birthdate": openapi.Schema(type=openapi.FORMAT_DATE),
            },
        )
    )
    def post(self, request, format=None):
        serializer = PayeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save()
        headers = self.get_success_headers(request, serializer.data)
        return Response(None, status.HTTP_201_CREATED, headers=headers)

    def get(self, request, format=None):
        payees = Payee.objects.all()
        serializer = PayeeSerializer(payees, many=True)
        return Response(serializer.data)

    def get_success_headers(self, request, data):
        try:
            return {'Location': str(f"{request.build_absolute_uri()}{data['id']}/")}
        except (TypeError, KeyError):
            return {}


class PayeeDetail(APIView):

    def get(self, request, pk, format=None):
        payee = self.get_object(pk)
        serializer = PayeeSerializer(payee)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        payee = self.get_object(pk)
        payee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "entry": openapi.Schema(type=openapi.TYPE_STRING),
                    "birthdate": openapi.Schema(type=openapi.FORMAT_DATE),
            },
        )
    )
    def put(self, request, pk, format=None):
        payee = self.get_object(pk)
        serializer = PayeeSerializer(payee, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(None, status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Payee.objects.get(pk=pk)
        except Payee.DoesNotExist:
            raise Http404
