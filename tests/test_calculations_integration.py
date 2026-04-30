import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User, Calculation
from app.schemas import CalculationCreate
from app.calculations import CalculationFactory, OperationType


# ── Test database setup ───────────────────────────────────────────────────────

TEST_DATABASE_URL = "sqlite:///./test_calculations.db"


@pytest.fixture(scope="module")
def db_session():
    """
    Creates a fresh SQLite database for the entire test module.
    Drops all tables after tests complete — no leftover state.
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


# ── Integration tests ─────────────────────────────────────────────────────────

class TestCalculationIntegration:
    """
    Tests that hit a real database.
    Verifies the full flow: validate → compute → store → retrieve.
    """

    def test_insert_add_calculation(self, db_session):
        """Add operation is stored correctly in the database."""
        schema = CalculationCreate(a=10, b=5, type="Add")
        result = CalculationFactory.compute(schema.type, schema.a, schema.b)

        record = Calculation(
            a=schema.a,
            b=schema.b,
            type=schema.type.value,
            result=result,
            user_id=None
        )
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.id is not None
        assert record.result == 15.0
        assert record.type == "Add"

    def test_insert_subtract_calculation(self, db_session):
        schema = CalculationCreate(a=20, b=8, type="Sub")
        result = CalculationFactory.compute(schema.type, schema.a, schema.b)

        record = Calculation(
            a=schema.a, b=schema.b,
            type=schema.type.value, result=result
        )
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.result == 12.0

    def test_insert_multiply_calculation(self, db_session):
        schema = CalculationCreate(a=6, b=7, type="Multiply")
        result = CalculationFactory.compute(schema.type, schema.a, schema.b)

        record = Calculation(
            a=schema.a, b=schema.b,
            type=schema.type.value, result=result
        )
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.result == 42.0

    def test_insert_divide_calculation(self, db_session):
        schema = CalculationCreate(a=100, b=4, type="Divide")
        result = CalculationFactory.compute(schema.type, schema.a, schema.b)

        record = Calculation(
            a=schema.a, b=schema.b,
            type=schema.type.value, result=result
        )
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.result == 25.0

    def test_retrieve_calculation_from_db(self, db_session):
        """Records inserted earlier must be retrievable and correct."""
        records = db_session.query(Calculation).all()
        assert len(records) >= 4

    def test_calculation_with_user_id(self, db_session):
        """user_id FK stores correctly when provided."""
        # First create a user to reference
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        schema = CalculationCreate(a=9, b=3, type="Divide", user_id=user.id)
        result = CalculationFactory.compute(schema.type, schema.a, schema.b)

        record = Calculation(
            a=schema.a, b=schema.b,
            type=schema.type.value, result=result,
            user_id=user.id
        )
        db_session.add(record)
        db_session.commit()
        db_session.refresh(record)

        assert record.user_id == user.id
        assert record.result == 3.0

    def test_invalid_type_rejected_before_db(self, db_session):
        """Invalid type never reaches the database — Pydantic catches it."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            CalculationCreate(a=1, b=2, type="InvalidOp")

    def test_divide_by_zero_rejected_before_db(self, db_session):
        """Division by zero never reaches the database — Pydantic catches it."""
        from pydantic import ValidationError
        with pytest.raises(ValidationError):
            CalculationCreate(a=10, b=0, type="Divide")