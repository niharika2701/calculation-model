def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    # Arrange: a and b come in as floats
    # Act: add them
    # Return the result
    return a + b


def subtract(a: float, b: float) -> float:
    """Return a minus b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return a multiplied by b."""
    return a * b


def divide(a: float, b: float) -> float:
    """
    Return a divided by b.

    Raises:
        ValueError: if b is zero.
        WHY ValueError? It's a standard Python error for bad input values.
        Our API layer will catch this and return HTTP 400.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(a: float, b: float) -> float:
    """Return a raised to the power of b."""
    return a ** b


def modulo(a: float, b: float) -> float:
    """
    Return the remainder when a is divided by b.

    Raises:
        ValueError: if b is zero.
    """
    if b == 0:
        raise ValueError("Cannot perform modulo by zero")
    return a % b