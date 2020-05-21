import json
from datetime import date, datetime
import pytest

from salaries.models import Salary, Payee
from salaries.serializers import PayeeSerializer


@pytest.mark.django_db
def test_create_salary(client):
    # Given
    salaries = Salary.objects.all()
    assert len(salaries) == 0

    # When
    response = client.post(
        "/api/salaries/", 
        {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 23423.33,
            "taxes": 3995.48
        },
        content_type = "application/json"
    )

    # Then
    assert response.status_code == 201
    assert len(Salary.objects.all()) == 1
