from enum import Enum


class OperationType(str, Enum):
    """
    Valid operation types as a string enum.
    Inheriting from str means Pydantic serialises these as plain strings
    in JSON — the API returns "Add", not "OperationType.ADD".
    """
    ADD      = "Add"
    SUB      = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE   = "Divide"


class CalculationFactory:
    """
    Maps an OperationType to its computation function.

    Open/Closed Principle: adding a new operation = one new dictionary entry.
    No existing code changes. No if/elif chains to maintain.
    """

    _operations: dict = {
        OperationType.ADD:      lambda a, b: a + b,
        OperationType.SUB:      lambda a, b: a - b,
        OperationType.MULTIPLY: lambda a, b: a * b,
        OperationType.DIVIDE:   lambda a, b: a / b,
    }

    @classmethod
    def compute(cls, op_type: OperationType, a: float, b: float) -> float:
        """
        Look up the operation and execute it.

        Raises:
            ValueError: if op_type is not a known OperationType.
            ZeroDivisionError: if Divide is called with b == 0.
        """
        operation = cls._operations.get(op_type)
        if operation is None:
            raise ValueError(f"Unknown operation: '{op_type}'")
        return operation(a, b)