import pytest


@pytest.fixture(
    params=[
        (3, 4, 5, 12, 6.0),
        (5, 12, 13, 30, 30.0),
        (1.5, 2.0, 2.5, 6, 1.5),
    ]
)
def triangle_case(request):
    return request.param
