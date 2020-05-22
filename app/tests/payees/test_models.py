from datetime import date
import pytest

from payees.models import Payee


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
