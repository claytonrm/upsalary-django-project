import json
from datetime import date, datetime
import pytest

from salaries.models import Salary, Payee
from salaries.serializers import PayeeSerializer


@pytest.mark.django_db
def test_create_salary(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", 
        {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 23423.33,
            "taxes": 3434.35
        },
        content_type = "application/json"
    )

    # Then
    assert response.status_code == 201
    assert len(Salary.objects.all()) == 1


@pytest.mark.django_db
def test_created_salary_no_taxes(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", 
        {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 23423.33
        },
        content_type="application/json"
    )
    
    # Then
    assert response.status_code == 201
    assert len(Salary.objects.all()) == 1


@pytest.mark.django_db
def test_created_salary_empty_json(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post("/api/salaries/", {}, content_type="application/json")
    
    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0


@pytest.mark.django_db
def test_created_salary_no_user(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", 
        {
            "amount": 23423.33,
            "taxes": 3434.35
        },
        content_type="application/json"
    )
    
    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0


@pytest.mark.django_db
def test_created_salary_no_amount(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", 
        {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "taxes": 23423.33
        }, 
        content_type="application/json")
    
    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0
