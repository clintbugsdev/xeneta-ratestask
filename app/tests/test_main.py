from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_get_rates():
    q = "date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main"
    response = client.get(f"/rates?{q}")
    assert response.status_code == 200
    assert {
        "day":"2016-01-01","average_price":1112
        } in response.json() # Assumption from given example
    assert {
        "day":"2016-01-02","average_price":1112
        } in response.json() # Assumption from given example


def test_get_rates_require_orign_and_destination():
    q = "date_from=2016-01-01&date_to=2016-01-10"
    response = client.get(f"/rates?{q}")
    assert response.status_code == 422
    assert "detail" in response.json()
    assert {
        "loc":["query","origin"],
        "msg":"field required","type":"value_error.missing"
        } in response.json()['detail']
    assert {
        "loc":["query","destination"],
        "msg":"field required","type":"value_error.missing"
        }in response.json()['detail']
