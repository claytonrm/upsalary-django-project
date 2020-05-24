from datetime import date, datetime
from salaries.serializers import SalarySerializer, SalaryAmountSummarySerializer, SalarySummarySerializer
from salaries.serializers import SalaryTaxesSummarySerializer


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
    assert serializer.errors == {"amount": ["This field is required."]}


def test_salary_amount_summary_serializer():
    valid_serializer_data = {
        "average": 1000.0,
        "highest": 900.0,
        "lowest": 950.0,
    }

    serializer = SalaryAmountSummarySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_salary_aggretation_serializer():
    invalid_serializer_data = {
        "highest": 900.0,
        "lowest": 950.0,
    }

    serializer = SalaryAmountSummarySerializer(data=invalid_serializer_data)
    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"average": ["This field is required."]}


def test_salary_taxes_summary_serializer():
    valid_serializer_data = {
        "average": 5000.0,
    }

    serializer = SalaryTaxesSummarySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.errors == {}


def test_salary_summary_serializer():
    valid_serializer_data = {
        "amount": {
            "average": 1000.0,
            "highest": 900.0,
            "lowest": 950.0,
        },
        "taxes": {
            "average": 393.0
        }
    }

    serializer = SalarySummarySerializer(data=valid_serializer_data)
    assert serializer.is_valid()
    assert serializer.validated_data == valid_serializer_data
    assert serializer.errors == {}


def test_invalid_salary_summary_serializer():
    invalid_serializer_data = {
        "amount": {
            "average": 1000.0,
            "lowest": 950.0,
        },
        "taxes": {
            "average": 393.0
        }
    }
    serializer = SalarySummarySerializer(data=invalid_serializer_data)

    assert not serializer.is_valid()
    assert serializer.validated_data == {}
    assert serializer.data == invalid_serializer_data
    assert serializer.errors == {"amount": {"highest": ["This field is required."]}}
