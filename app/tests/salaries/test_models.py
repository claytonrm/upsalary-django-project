import pytest

from datetime import date
from salaries.models import Payee, Salary


@pytest.mark.django_db
def test_payee_model():
    # Given
    user = Payee(name="Billy Jean", entry="123456789", birthdate=date(2000, 1, 30))

    # When
    user.save()

    # Then
    assert user.name == "Billy Jean"
    assert user.entry == "123456789"
    assert user.birthdate == date(2000, 1, 30)
    assert str(user) == "123456789 - Billy Jean"


@pytest.mark.django_db
def test_salary_model():
    # Given
    josh = Payee(name="Josh Klinghoffer", entry="987654321", birthdate=date(1980, 8, 27))
    josh.save()

    salary = Salary(user=josh, amount=40454.95, taxes=1309.89)

    # When
    salary.save()

    # Then
    assert salary.amount == 40454.95
    assert salary.taxes == 1309.89
    assert salary.received_at is not None
    assert str(salary.user) == "987654321 - Josh Klinghoffer"
