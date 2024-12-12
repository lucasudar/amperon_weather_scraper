import pytest
from sqlalchemy import create_engine

@pytest.fixture
def engine():
    db_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/tomorrow'
    return create_engine(db_url)


def test_connection(engine):
    try:
        conn = engine.connect()
        assert conn is not None
        conn.close()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")