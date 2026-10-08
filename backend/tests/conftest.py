import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.api.deps import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

# Single shared engine — all test sessions use the same in-memory DB
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

# Keep a single connection open so the in-memory DB isn't destroyed between uses
connection = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables once per test on the shared connection, rollback after."""
    Base.metadata.create_all(bind=connection)
    transaction = connection.begin_nested()
    yield
    transaction.rollback()
    Base.metadata.drop_all(bind=connection)


@pytest.fixture
def db(setup_db):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
