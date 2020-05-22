import pytest

from datetime import date
from salaries.models import Salary
from payees.models import Payee


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
