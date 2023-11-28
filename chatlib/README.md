## Chatlib

Library for creating chatbots.

Modules:
- wikijs - module for querying wikijs

## Installation

```sh
poetry install
```

## Development

```sh
poetry install --with dev
```

## Testing

To run integration tests you need to have:

- `WIKIJS_API_TOKEN` env variable set to valid token (ask admins)

Run every test (including integration tests):

```sh
poetry run python -m pytest
```

Run unit tests only:

```sh
poetry run python -m pytest -m "not integration"
```

## Formatting and linting

Formatting:

```sh
poetry run ruff format .
```

Linting

```sh
poetry run ruff check .
```
