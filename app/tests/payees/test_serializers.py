from datetime import date
from payees.serializers import PayeeSerializer


def test_valid_payee_serializer():
    # Given
    valid_serializer_data = {
        "name": "Billy Jean",
        "entry": "123456789",
        "birthdate": date(2000, 1, 20)
    }

    # When
    serializer = PayeeSerializer(data=valid_serializer_data)

    # Then
    assert serializer.is_valid()
    # assert serializer.validated_data == valid_serializer_data
    # assert serializer.data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_payee_serializer():
    invalid_serializer_data = {
        "name": "Josh",
        "birthdate": date(1992, 8, 14)
    }

    serializer = PayeeSerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    # assert serializer.validated_data == {}
    # assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"entry": ["This field is required."]}
