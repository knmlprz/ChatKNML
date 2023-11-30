# Pre-commit

## Installing Code Formatting Tools

Install pre-commit using the following command:

   ```bash
   pip install pre-commit

Install hooks for your project

    ```bash
    pre-commit install

Pre-commit will automatically run configured hooks to check and format the code

1. Add files to the commit

    ```bash
    git add .

2. Commit the changes

    ```bash
    git commit -m "Your commit message"
    pre-commit run --all-files

To update hooks to the latest versions, use the following command


```bash
pre-commit autoupdate
