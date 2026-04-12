import pytest
import pymysql


def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="127.0.0.1")
    parser.addoption("--port", action="store", default=3306, type=int)
    parser.addoption("--database", action="store", default="opencart")
    parser.addoption("--user", action="store", default="root")
    parser.addoption("--password", action="store", default="")


@pytest.fixture(scope="session")
def connection(request):
    conn = pymysql.connect(
        host=request.config.getoption("--host"),
        port=request.config.getoption("--port"),
        user=request.config.getoption("--user"),
        password=request.config.getoption("--password"),
        database=request.config.getoption("--database"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    yield conn
    conn.close()
