import pytest
from datetime import datetime, timedelta

from .test_session import session
from models.mapping_models import URLMapping


@pytest.fixture(scope="function")
def test_url_mapping(session):
    test_expire_date = datetime.now().date() + timedelta(days=3)
    test_url_mapping = URLMapping(
        origin_url="https://example.com",
        shorten_key="test_shorten_key",
        view_count=0,
        expire_date=test_expire_date,
    )

    session.add(test_url_mapping)
    session.commit()

    return test_url_mapping
