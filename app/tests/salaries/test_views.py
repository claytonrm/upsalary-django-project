import json
from datetime import date, datetime, timezone
import pytest

from salaries.models import Salary, Payee
from salaries.serializers import SalarySerializer


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


@pytest.mark.django_db
def test_get_single_salary(client, add_salary):
    # Given
    payee = Payee.objects.create(name="John Mayer", entry=2345643, birthdate=date(1975, 12, 27))
    salary = add_salary(user=payee, amount=60000, taxes=200)

    # When
    response = client.get(f"/api/salaries/{salary.id}/")

    # Then
    assert response.status_code == 200
    assert response.data['user']['name'] == "John Mayer"
    assert response.data['user']['entry'] == "2345643"
    assert response.data['user']['birthdate'] == "1975-12-27"
    assert float(response.data['amount']) == 60000
    assert float(response.data['taxes']) == 200


@pytest.mark.django_db
def test_get_all_salaries(client, add_salary):
    billy = Payee.objects.create(name="Billy", entry=345454, birthdate=date(1970, 11, 20))
    billy_salary = add_salary(user=billy, amount=54998.3, taxes=3004.68)
    
    joe = Payee.objects.create(name="Joe", entry=2345654334, birthdate=date(1980, 1, 1))
    joe_salary = add_salary(user=joe, amount=23434, taxes=566.68)

    response = client.get(f"/api/salaries/")

    assert response.status_code == 200
    assert float(response.data[0]['amount']) == 54998.3
    assert response.data[0]['user']['name'] == "Billy"
    assert float(response.data[1]['amount']) == 23434.0
    assert response.data[1]['user']['name'] == "Joe"