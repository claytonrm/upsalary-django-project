import pytest

from salaries.models import Salary


@pytest.fixture(scope='function')
def add_salary():
    def _add_salary(user, amount, taxes=0.0):
        return Salary.objects.create(user=user, amount=amount, taxes=taxes)
    return _add_salary
