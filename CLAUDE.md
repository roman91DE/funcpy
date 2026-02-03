# CLAUDE.md

## Project Overview

FuncPy is a Python library providing simple functional programming tools — composable operations for lists, dictionaries, and strings via static method interfaces. It has zero runtime dependencies and targets Python >= 3.10.

## Repository Structure

```
src/funcpy/
  __init__.py       # Package init, exports List, Dict, Functions, Str, compose, curry, pipe
  core.py           # All core functionality (~230 lines)
tests/
  __init__.py
  test_core.py      # pytest test suite (~280 lines, 30 tests)
pyproject.toml      # Build config (hatchling), deps, tool settings
```

## Core Classes (all methods are `@staticmethod`)

- **`List`** — `map`, `filter`, `foldl`, `foldr`, `reverse` on Python lists
- **`Dict`** — `vmap`, `kmap`, `vfilter`, `kfilter` on dicts
- **`Str`** — `map`, `filter`, `foldl`, `foldr`, `reverse` on strings
- **`Functions`** — `swap`, `compose`, `pipe`, `curry` (function composition and utilities)

### Module-level aliases

`compose`, `pipe`, and `curry` are also exported at module level for convenience:

```python
from funcpy.core import compose, pipe, curry
```

## Build & Tooling

| Tool | Purpose | Config location |
|------|---------|----------------|
| **hatchling** | Build backend | `pyproject.toml [build-system]` |
| **uv** | Package manager (preferred) | — |
| **pytest** | Testing | `pyproject.toml [tool.pytest]` |
| **pytest-cov** | Coverage | dev dependency |
| **ruff** | Linter + formatter | `pyproject.toml [tool.ruff]` |
| **mypy** | Type checking (strict) | `pyproject.toml [tool.mypy]` |

## Common Commands

```bash
uv pip install -e ".[dev]"   # Install with dev dependencies
pytest                        # Run tests
ruff check .                  # Lint
ruff format .                 # Format
mypy src                      # Type check (strict mode)
```

## Code Conventions

- **Python >= 3.10** — uses pattern matching (`match/case`), modern type hints (`list[A]` not `List[A]`)
- **Type hints on all public functions** — generic types use single-letter TypeVars (`A`, `B`, `C`)
- **Google-style docstrings** with `Example:` sections
- **Line length:** 88 characters
- **Naming:** PascalCase classes, snake_case methods/params
- **Functional style:** pure functions, no mutation, static methods, recursive where natural
- **mypy strict:** `disallow_untyped_defs`, `strict_optional`, `warn_return_any` all enabled
- **Ruff rules:** E, F, I, B, C4, UP, D, N, DTZ enabled; tests exempt from D and S rules

## Testing Conventions

- Test file pattern: `test_*.py` in `tests/`
- Plain functions (no classes): `def test_<class>_<method>_<case>():`
- Edge cases tested: empty collections, single elements, no-match filters
- Non-commutative operations tested to verify fold direction
- Variables named `got`/`expected` for clarity

## Known Gaps

- `pyproject.toml` defines CLI entry point `funcpy = "funcpy.cli:main"` — **`cli.py` does not exist**
