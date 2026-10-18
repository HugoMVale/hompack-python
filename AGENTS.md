# Repository instructions

## Project structure

- `src/hompack/` contains the Python package and its public API.
- `tests/` contains the Python test suite.
- `meson.build` builds and packages the native HOMPACK shared library.
- `subprojects/hompack/` is pulled from another repository and must not be edited here. The upstream repository is the source of truth for the Fortran implementation; make native-source changes there.
- `docs/` contains the MkDocs documentation.

## Development setup and checks

Use Python 3.12 or newer, `uv`, and a Fortran compiler supported by Meson. From the repository root:

```sh
uv sync
uv pip install -ve . --no-build-isolation
uv run --frozen pytest
uv run pre-commit install --hook-type pre-push
```

The pre-push hook runs Ruff linting, Ruff format checks, and Pyrefly type
checking before pushing to a remote.

The editable install compiles the native library, so it must be rerun after changes that affect the native build or packaged library. To build the documentation, install the docs group and run `uv run mkdocs build`.

## Code conventions

- Keep Python source under `src/hompack/`; use the existing Ruff configuration in `pyproject.toml`.
- All public methods require full docstrings in NumPy style.
- Test functions require a docstring; a simple one-line docstring is sufficient.
- Add or update focused tests in `tests/` for behavior changes.
- Keep packaging and native build changes consistent with the root `meson.build` and `pyproject.toml`.
- Do not edit generated build artifacts or downloaded/vendor-managed subproject files. In particular, never modify `subprojects/hompack/` in this repository.
