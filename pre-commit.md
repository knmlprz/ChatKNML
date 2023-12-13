# Pre-commit

## Instalowanie narzędzi do formatowania kodu

## Zainstaluj przed zatwierdzeniem, używając następującego polecenia

```bash
pip install pre-commit
```

## Zainstaluj hooki dla swojego projektu

```bash
pre-commit install
```

## Pre-commit automatycznie uruchomi hooki w celu sprawdzenia i sformatowania kodu

## Dodaj pliki do zatwierdzenia

```bash
git add .
```

## Zatwierdz zmiany

```bash
git commit -m "Your commit message"
pre-commit run --all-files
```

## Aby zaktualizować hooki do najnowszych wersji, użyj poniższego polecenia

```bash
pre-commit autoupdate
```
