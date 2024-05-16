import json
from datetime import datetime, timedelta

from tests.fixtures.test_session import client
from tests.fixtures.url_mapping_fixtures import test_url_mapping


def test_create_short_key(client):
    test_expire_date = (datetime.now().date() + timedelta(days=3)).isoformat()
    response = client.post(
        "v1/shorten",
        json={"origin_url": "https://example.com", "expire_date": test_expire_date},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["origin_url"] == "https://example.com"
    assert "shorten_key" in data


def test_get_origin_url(client, test_url_mapping):
    shorten_key = test_url_mapping.shorten_key
    response = client.get(f"/v1/{shorten_key}", follow_redirects=False)

    assert response.status_code == 301
    assert response.headers["location"] == "https://example.com"


def test_get_view_count(client, test_url_mapping):
    shorten_key = test_url_mapping.shorten_key

    response = client.get(f"/v1/stats/{shorten_key}")

    assert response.status_code == 200
    data = response.json()

    assert data["view_count"] == test_url_mapping.view_count


def test_update_mapping(client, test_url_mapping):
    shorten_key = test_url_mapping.shorten_key
    update_expire_date = (test_url_mapping.expire_date + timedelta(days=2)).isoformat()

    response = client.patch(
        f"/v1/shorten/{shorten_key}",
        json={"expire_date": update_expire_date},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["expire_date"] == update_expire_date
