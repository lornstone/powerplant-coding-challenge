import json

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def load_json(file_name: str):
    with open("tests/data/" + file_name, 'r') as f:
        return json.load(f)


def test_payload_1():
    payload = load_json("payload1.json")
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200


def test_payload_2():
    # Note that the current algorithm does not handle this case well, so we expect a 400 error for now
    payload = load_json("payload2.json")
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 400


def test_payload_3():
    payload = load_json("payload3.json")
    expected_results = load_json("response3.json")

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    assert response.json() == expected_results


def test_wrong_payload():
    payload = load_json("wrongpayload.json")
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 422
