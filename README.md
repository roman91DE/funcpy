# FuncPy

Simple Functional Programming Tools for Python

## Installation

```bash
# Install with pip
pip install funcpy

# Or with uv
uv pip install funcpy
```

## Features

FuncPy provides essential functional programming utilities for Python:

- `compose`: Compose two functions into a new function
- `pipe`: Pipe a value through a series of transformations
- `curry`: Curry a function for partial application

## Examples

```python
from funcpy.core import compose, pipe, curry

# Function composition
add_one = lambda x: x + 1
multiply_by_two = lambda x: x * 2
add_one_and_multiply = compose(multiply_by_two, add_one)
result = add_one_and_multiply(3)  # (3 + 1) * 2 = 8

# Piping values
result = pipe(
    3, 
    lambda x: x + 1,
    lambda x: x * 2,
    lambda x: f"Result: {x}"
)  # "Result: 8"

# Currying
add = curry(lambda x, y: x + y)
add_five = add(5)
result = add_five(10)  # 15
```

## Development

This project uses `uv` for dependency management and development workflow.

### Setup Development Environment

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Run type checking
mypy src
```

## License

MIT License