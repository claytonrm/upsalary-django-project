from datetime import date
import pytest

from payees.models import Payee


@pytest.mark.django_db
def test_create_payee(client):
    # Given
    payees = Payee.objects.all()
    assert len(payees) == 0

    # When
    response = client.post("/api/users/", {
            "name": "John Mayer",
            "entry": "1234567893",
            "birthdate": date(1991, 1, 30)
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 201
    assert len(Payee.objects.all()) == 1


@pytest.mark.django_db
def test_get_single_payee(client, add_payee):
    # Given
    payee = add_payee(name="Tom DeLonge", entry="34376378", birthdate=date(1989, 2, 4))

    # When
    response = client.get(f"/api/users/{payee.id}/")

    # Then
    assert response.status_code == 200
    assert response.data['name'] == "Tom DeLonge"


@pytest.mark.django_db
def test_get_single_payee_incorrect_id(client):
    # Given
    # When
    response = client.get("/api/users/99/")

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_all_payees(client, add_payee):
    # Given
    chad = add_payee(name="Chad Smith", entry="39745238", birthdate=date(1972, 10, 7))
    flea = add_payee(name="Flea", entry="43234795", birthdate=date(1977, 3, 2))

    # When
    response = client.get("/api/users/")

    # Then
    assert response.status_code == 200
    assert response.data[0]["name"] == chad.name
    assert response.data[1]["name"] == flea.name


@pytest.mark.django_db
def test_remove_payee(client, add_payee):
    # Given
    josh = add_payee(name="Josh Klinghoffer", entry="432342432", birthdate=date(1991, 11, 25))
    response_before = client.get(f"/api/users/{josh.id}/")
    assert response_before.status_code == 200
    assert response_before.data['name'] == "Josh Klinghoffer"

    # When
    response = client.delete(f"/api/users/{josh.id}/")

    # Then
    assert response.status_code == 204

    response_after = client.get("/api/users/")
    assert response_after.status_code == 200
    assert len(response_after.data) == 0


@pytest.mark.django_db
def test_remove_payee_incorrect_id(client):
    # Given
    # When
    response = client.delete("/api/users/99/")

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_payee(client, add_payee):
    # Given
    payee = add_payee(name="Josh Klinghoffer", entry="432342432", birthdate=date(1991, 11, 25))

    # When
    response = client.put(
        f"/api/users/{payee.id}/",
        {"name": "John Frusciante", "entry": "343343222303", "birthdate": "1985-06-10"},
        content_type="application/json"
    )

    # Then
    assert response.status_code == 204

    response_after = client.get(f"/api/users/{payee.id}/")
    assert response_after.status_code == 200
    assert response_after.data['name'] == "John Frusciante"
    assert response_after.data['entry'] == "343343222303"


@pytest.mark.django_db
def test_update_payee_incorrect_id(client):
    # Given
    # When
    response = client.put("/api/users/999/")

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("add_payee, payload, status_code", [
    ["add_payee", {}, 400],
    ["add_payee", {"name": "Paul", "entry": "34933343"}, 400]
], indirect=["add_payee"])
def test_update_payee_invalid_json(client, add_payee, payload, status_code):
    # Given
    payee = add_payee(name="Josh Klinghoffer", entry="432342432", birthdate=date(1991, 11, 25))

    # When
    response = client.put(f"/api/users/{payee.id}/", payload, content_type="application/json")

    # Then
    assert response.status_code == status_code
