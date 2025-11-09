import pytest
import requests


url = "https://jsonplaceholder.typicode.com"
resp_code_ok = 200
resp_status_ok = "success"
count_post = 1


city = ""
pagination = 0


def test_list_all_posts():
    response = requests.get(f"{url}/posts")
    assert response.status_code == resp_code_ok
    assert isinstance(response.json(), list)
    assert 0 <= len(response.json())


@pytest.mark.parametrize(
    "post_num",
    [(4), (3)],
    ids=["first check", "second check"],
)
def test_post_id(post_num):
    response = requests.get(f"{url}/posts/{post_num}")
    assert response.status_code == resp_code_ok
    assert response.json().get("id", "") == post_num


@pytest.mark.parametrize(
    "post_id",
    [(4), (3), (2)],
    ids=["first check", "second check", "third check"],
)
def test_post_id_comm(post_id):
    response = requests.get(f"{url}/posts/{post_id}/comments")
    assert response.status_code == resp_code_ok

    data = response.json()
    assert isinstance(data, list)

    for item in data:
        assert item.get("postId", "") == post_id, (
            f"Неверный пост: {item.get('postId')} (ожидали {post_id})"
        )


@pytest.mark.parametrize(
    "post_id",
    [(4), (3), (2)],
    ids=["first check", "second check", "third check"],
)
def test_post_id_filter(post_id):
    params = {"postId": post_id}

    response = requests.get(f"{url}/comments", params=params)
    assert response.status_code == resp_code_ok

    data = response.json()
    assert isinstance(data, list)

    for item in data:
        assert item.get("postId", "") == post_id, (
            f"Неверный пост: {item.get('postId')} (ожидали {post_id})"
        )


@pytest.mark.parametrize(
    "post_num",
    [(1), (2)],
    ids=["first check", "second check"],
)
def test_post_delete(post_num):
    response = requests.delete(f"{url}/posts/{post_num}")
    assert response.status_code == resp_code_ok
