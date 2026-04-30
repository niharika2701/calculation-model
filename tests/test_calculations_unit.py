import pytest
from pydantic import ValidationError
from app.calculations import CalculationFactory, OperationType
from app.schemas import CalculationCreate


# ── Factory tests ─────────────────────────────────────────────────────────────

class TestCalculationFactory:
    """Tests for CalculationFactory.compute() — no database needed."""

    def test_add(self):
        assert CalculationFactory.compute(OperationType.ADD, 3, 2) == 5

    def test_subtract(self):
        assert CalculationFactory.compute(OperationType.SUB, 10, 4) == 6

    def test_multiply(self):
        assert CalculationFactory.compute(OperationType.MULTIPLY, 3, 4) == 12

    def test_divide(self):
        assert CalculationFactory.compute(OperationType.DIVIDE, 10, 2) == 5

    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            CalculationFactory.compute(OperationType.DIVIDE, 10, 0)

    def test_add_floats(self):
        result = CalculationFactory.compute(OperationType.ADD, 1.5, 2.5)
        assert result == 4.0

    def test_subtract_negative_result(self):
        result = CalculationFactory.compute(OperationType.SUB, 2, 10)
        assert result == -8

    def test_multiply_by_zero(self):
        assert CalculationFactory.compute(OperationType.MULTIPLY, 99, 0) == 0


# ── CalculationCreate schema tests ────────────────────────────────────────────

class TestCalculationCreateSchema:
    """Tests for Pydantic validation — no database needed."""

    def test_valid_add(self):
        calc = CalculationCreate(a=1, b=2, type="Add")
        assert calc.type == OperationType.ADD

    def test_valid_subtract(self):
        calc = CalculationCreate(a=10, b=3, type="Sub")
        assert calc.type == OperationType.SUB

    def test_valid_multiply(self):
        calc = CalculationCreate(a=4, b=5, type="Multiply")
        assert calc.type == OperationType.MULTIPLY

    def test_valid_divide(self):
        calc = CalculationCreate(a=10, b=2, type="Divide")
        assert calc.type == OperationType.DIVIDE

    def test_invalid_type_rejected(self):
        """Anything not in OperationType must raise a ValidationError."""
        with pytest.raises(ValidationError):
            CalculationCreate(a=1, b=2, type="Power")

    def test_divide_by_zero_rejected(self):
        """b=0 with Divide must raise a ValidationError."""
        with pytest.raises(ValidationError):
            CalculationCreate(a=10, b=0, type="Divide")

    def test_divide_by_zero_allowed_for_other_ops(self):
        """b=0 is fine for Add, Sub, Multiply."""
        calc = CalculationCreate(a=5, b=0, type="Add")
        assert calc.b == 0

    def test_optional_user_id_defaults_to_none(self):
        calc = CalculationCreate(a=1, b=1, type="Add")
        assert calc.user_id is None

    def test_user_id_accepted(self):
        calc = CalculationCreate(a=1, b=1, type="Add", user_id=42)
        assert calc.user_id == 42

    def test_float_inputs(self):
        calc = CalculationCreate(a=3.14, b=2.71, type="Multiply")
        assert calc.a == 3.14