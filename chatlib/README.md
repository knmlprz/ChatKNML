## Chatlib

Library for creating chatbots.

Modules:
- wikijs - module for querying wikijs

## Installation

```bash
poetry install
```

## Development

```bash
poetry install --with dev
```

## Testing

To run integration tests you need to have:

- `WIKIJS_API_TOKEN` env variable set to valid token (ask admins)

Run every test (including integration tests):

```bash
poetry run python -m pytest
```

Run unit tests only:

```bash
poetry run python -m pytest -m "not integration"
```

## Formatting and linting

Formatting:

```bash
poetry run ruff format .
```

Linting

```bash
poetry run ruff check .
```
