from datetime import date
import pytest

from salaries.models import Salary, Payee


@pytest.mark.django_db
def test_create_salary(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 23423.33,
            "taxes": 3434.35
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 201
    assert len(Salary.objects.all()) == 1


@pytest.mark.django_db
def test_create_salary_existing_user(client, add_salary):
    # Given
    add_salary(
        user=Payee.objects.create(name="John Mayer", entry="2345643", birthdate=date(1975, 12, 27)),
        amount=60000, taxes=200
    )
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 1

    # When
    response = client.post(
        "/api/salaries/", {
            "user": {"name": "Corey", "entry": "2345643", "birthdate": date(1975, 12, 27)},
            "amount": 23423.33,
            "taxes": 3434.35
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 201

    response_after = client.get("/api/salaries/")
    assert len(response_after.data) == 2
    assert response_after.data[0]['user']['name'] == "Corey"
    assert response_after.data[1]['user']['name'] == "Corey"
    assert float(response_after.data[0]['amount']) == 60000
    assert float(response_after.data[1]['amount']) == 23423.33


@pytest.mark.django_db
def test_create_salary_no_taxes(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 23423.33
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 201
    assert len(Salary.objects.all()) == 1


@pytest.mark.django_db
def test_create_salary_empty_json(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post("/api/salaries/", {}, content_type="application/json")

    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0


@pytest.mark.django_db
def test_create_salary_no_user(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", {
            "amount": 23423.33,
            "taxes": 3434.35
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0


@pytest.mark.django_db
def test_create_salary_no_amount(client):
    # Given
    salaries_before_post = Salary.objects.all()
    assert len(salaries_before_post) == 0

    # When
    response = client.post(
        "/api/salaries/", {
            "user": {"name": "Joe", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "taxes": 23423.33
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 400
    assert len(Salary.objects.all()) == 0


@pytest.mark.django_db
def test_get_single_salary(client, add_salary):
    # Given
    payee = Payee.objects.create(name="John Mayer", entry=2345643, birthdate=date(1975, 12, 27))
    salary = add_salary(user=payee, amount=60000, taxes=200)

    # When
    response = client.get(f"/api/salaries/{salary.id}/")

    # Then
    assert response.status_code == 200
    assert response.data['user']['name'] == "John Mayer"
    assert response.data['user']['entry'] == "2345643"
    assert response.data['user']['birthdate'] == "1975-12-27"
    assert float(response.data['amount']) == 60000
    assert float(response.data['taxes']) == 200


@pytest.mark.django_db
def test_get_all_salaries(client, add_salary):
    # Given
    billy = Payee.objects.create(name="Billy", entry=345454, birthdate=date(1970, 11, 20))
    add_salary(user=billy, amount=54998.3, taxes=3004.68)

    joe = Payee.objects.create(name="Joe", entry=2345654334, birthdate=date(1980, 1, 1))
    add_salary(user=joe, amount=23434, taxes=566.68)

    # When
    response = client.get("/api/salaries/")

    # Then
    assert response.status_code == 200
    assert float(response.data[0]['amount']) == 54998.3
    assert response.data[0]['user']['name'] == "Billy"
    assert float(response.data[1]['amount']) == 23434.0
    assert response.data[1]['user']['name'] == "Joe"


@pytest.mark.django_db
def test_remove_salary(client, add_salary):
    # Given
    mark = Payee.objects.create(name="Mark", entry=5434343366, birthdate=date(1996, 12, 3))
    salary = add_salary(user=mark, amount=20400.8, taxes=8000.03)
    response_before = client.get(f"/api/salaries/{salary.id}/")
    assert response_before.status_code == 200
    assert float(response_before.data['amount']) == 20400.8

    # When
    response = client.delete(f"/api/salaries/{salary.id}/")
    assert response.status_code == 204

    # Then
    response_after = client.get("/api/salaries/")
    assert response_after.status_code == 200
    assert len(response_after.data) == 0


@pytest.mark.django_db
def test_remove_salary_incorrect_id(client):
    # Given
    # When
    response = client.delete("/api/salaries/9999/")

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_salary(client, add_salary):
    # Given
    tom = Payee.objects.create(name="Tom", entry="1234323453", birthdate=date(1991, 12, 12))
    salary = add_salary(user=tom, amount=99000)

    # When
    response = client.put(
        f"/api/salaries/{salary.id}/", {
            "user": {"name": "Tom DeLonge", "entry": "3443422", "birthdate": date(1991, 6, 17)},
            "amount": 100000,
            "taxes": 20000
        },
        content_type="application/json"
    )

    # Then
    assert response.status_code == 204

    response_after = client.get(f"/api/salaries/{salary.id}/")
    assert response_after.status_code == 200
    assert response_after.data['user']['name'] == "Tom DeLonge"
    assert float(response_after.data['amount']) == 100000
    assert float(response_after.data['taxes']) == 20000
    # Not allowed to update
    assert response_after.data['user']['entry'] == "1234323453"


@pytest.mark.django_db
def test_update_incorrect_id(client):
    # Given
    # When
    response = client.put("/api/salaries/99/")
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.parametrize("add_salary, payload, status_code", [
    ["add_salary", {}, 400],
    ["add_salary", {"taxes": 1000}, 400],
], indirect=["add_salary"])
def test_update_salary_invalid_json(client, add_salary, payload, status_code):
    # Given
    travis = Payee.objects.create(name="Travis", entry=4545444443, birthdate=date(1993, 12, 12))
    salary = add_salary(user=travis, amount=19330, taxes=349)

    # When
    response = client.put(f"/api/salaries/{salary.id}/", payload, content_type="application/json")

    # Then
    assert response.status_code == status_code


@pytest.mark.django_db
def test_get_salary_by_query_param(client, add_salary):
    # Given
    travis = Payee.objects.create(name="Travis", entry=4545444443, birthdate=date(1993, 12, 12))
    add_salary(
        user=travis,
        amount=19330,
        taxes=349
    )

    add_salary(
        user=Payee.objects.create(name="Mark", entry=5434343366, birthdate=date(1996, 12, 3)),
        amount=20400.8,
        taxes=8000.03
    )

    add_salary(
        user=Payee.objects.create(name="Tom", entry="1234323453", birthdate=date(1991, 12, 12)),
        amount=99000
    )

    # When
    response = client.get('/api/salaries/', {'user_id': travis.id})

    # Then
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['user']['name'] == travis.name
    assert float(response.data[0]['amount']) == 19330
