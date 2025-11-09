import pytest
import requests


url = "https://dog.ceo/api/"
resp_code_ok = 200
resp_status_ok = "success"


def test_list_all():
    response = requests.get(f"{url}breeds/list/all")
    assert response.status_code == resp_code_ok
    assert response.json().get("status") == resp_status_ok


def test_img_random():
    response = requests.get(f"{url}breeds/image/random")
    assert response.json().get("message").endswith(".jpg"), (
        f"There is no foto .jpg in response"
    )
    assert response.status_code == resp_code_ok
    assert response.json().get("status") == resp_status_ok


@pytest.mark.parametrize(
    ("hound"),
    [("basenji"), ("eskimo")],
    ids=["first check", "second check"],
)
def test_breeds_list(hound):
    response = requests.get(f"{url}breed/{hound}/images/random")
    assert hound.lower() in response.json().get("message"), (
        f"Порода '{hound}' не встречается в URL"
    )
    assert response.json().get("message").endswith(".jpg"), (
        f"There is no foto .jpg in response"
    )
    assert response.status_code == resp_code_ok
    assert response.json().get("status") == resp_status_ok


HOUNDS = ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"]


@pytest.mark.parametrize("hound", HOUNDS, ids=HOUNDS)
def test_hound_subbreeds(hound):
    response = requests.get(f"{url}breed/hound/list")
    assert hound in response.json().get("message", []), (
        f"'{hound}' нет в списке подпород"
    )
    assert response.status_code == resp_code_ok
    assert response.json().get("status") == resp_status_ok
