import pytest
import requests


url = "https://api.openbrewerydb.org/v1/"
resp_code_ok = 200
resp_status_ok = "success"
city = ""
pagination = 0
count_rand_brewery = 1


def test_list_all_breweries():
    response = requests.get(f"{url}breweries")
    assert response.status_code == resp_code_ok
    assert isinstance(response.json(), list)
    assert 0 <= len(response.json())


@pytest.mark.parametrize(
    "city, pagination",
    [("san diego", 4), ("austin", 3)],
    ids=["first check", "second check"],
)
def test_city_filter(city, pagination):
    params = {
        "by_city": city,
        "per_page": pagination,
    }
    response = requests.get(f"{url}breweries", params=params)
    assert response.status_code == resp_code_ok

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= pagination, f"Ожидаем ≤ {pagination}, а получили {len(data)}"

    for item in data:
        assert item.get("city", "").lower() == city, (
            f"Неверный город: {item.get('city')} (ожидали {city})"
        )


def test_brewery_random():
    response = requests.get(f"{url}breweries/random")
    assert response.status_code == resp_code_ok

    assert isinstance(response.json(), list)
    assert len(response.json()) == count_rand_brewery, (
        f"Ожидаем ≤ {count_rand_brewery}, а получили {len(response.json())}"
    )


@pytest.mark.parametrize(
    "country, pagination",
    [("South Korea", 4), ("USA", 3), ("Russia", 2)],
    ids=["first check", "second check", "third check"],
)
def test_country_ilter(country, pagination):
    params = {
        "by_country": country,
        "per_page": pagination,
    }
    response = requests.get(f"{url}breweries", params=params)
    assert response.status_code == resp_code_ok

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= pagination, f"Ожидаем ≤ {pagination}, а получили {len(data)}"

    for item in data:
        assert item.get("country", "") == country, (
            f"Неверный город: {item.get('country')} (ожидали {country})"
        )


@pytest.mark.parametrize(
    "type, pagination",
    [("micro", 4), ("nano", 3), ("regional", 2)],
    ids=["first check", "second check", "third check"],
)
def test_type_filter(type, pagination):
    params = {
        "by_type": type,
        "per_page": pagination,
    }
    response = requests.get(f"{url}breweries", params=params)
    assert response.status_code == resp_code_ok

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= pagination, f"Ожидаем ≤ {pagination}, а получили {len(data)}"

    for item in data:
        assert item.get("brewery_type", "") == type, (
            f"Неверный город: {item.get('brewery_type')} (ожидали {type})"
        )
