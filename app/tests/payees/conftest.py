import pytest

from payees.models import Payee


@pytest.fixture(scope='function')
def add_payee():
    def _add_payee(name, entry, birthdate):
        return Payee.objects.create(name=name, entry=entry, birthdate=birthdate)
    return _add_payee
