import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.models import Aluno


def pytest_collection_modifyitems(items):
    # Garante ordem pedagógica da pirâmide: unit -> integration -> e2e (ui).
    marker_order = {"unit": 0, "integration": 1, "e2e": 2}

    def sort_key(item):
        for marker, position in marker_order.items():
            if item.get_closest_marker(marker):
                return (position, str(item.fspath), item.name)
        return (len(marker_order), str(item.fspath), item.name)

    items.sort(key=sort_key)


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def client(db_engine):
    from fastapi.testclient import TestClient
    from app.main import app

    Session = sessionmaker(bind=db_engine)

    def override_get_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


