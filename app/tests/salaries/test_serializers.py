from datetime import date, datetime, timezone
from salaries.serializers import PayeeSerializer, SalarySerializer
from salaries.models import Payee

# def test_valid_payee_serializer():
#     # Given
#     valid_serializer_data = {
#         "name": "Billy Jean",
#         "entry": "123456789",
#         "birthdate": date(2000, 1, 20)
#     }

#     # When
#     serializer = PayeeSerializer(data=valid_serializer_data)

#     # Then
#     assert serializer.is_valid()
#     assert serializer.errors == {}


def test_valid_salary_serializer():
    # Given
    valid_serializer_data = {
        "user": {"name": "Billy Jean", "entry": "123456789", "birthdate": date(2000, 1, 20)},
        "amount": 1000.00,
        "taxes": 200.00,
        "received_at": datetime(2020, 5, 20, 10, 10, 54, 343, None)
    }

    # When
    serializer = SalarySerializer(data=valid_serializer_data)

    # Then
    assert serializer.is_valid()
    # assert serializer.validated_data == expected_validated_data
    # assert serializer.data == expected_validated_data
    assert serializer.errors == {}


def test_invalid_salary_serializer():
    invalid_serializer_data = {
        "user": {"name": "Billy Jean", "entry": "123456789", "birthdate": date(2000, 1, 20)},
        "taxes": 200.00,
        "received_at": datetime(2020, 1, 30, 10, 10, 54, 343, None)
    }

    serializer = SalarySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    # assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"amount": ["This field is required."]}