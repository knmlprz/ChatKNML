# ChatKNML

[![KNML](https://i.imgur.com/GLpXodx.png)](https://knml.edu.pl/)

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0%2B-blue)](https://www.docker.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.6%2B-blue)](https://python-poetry.org/)
[![Django](https://img.shields.io/badge/Django-3.2%2B-green)](https://www.djangoproject.com/)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3.2%2B-blue)](https://discordpy.readthedocs.io/en/stable/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16%2B-blue)](https://www.postgresql.org/)
[![Git](https://img.shields.io/badge/Git-2.40%2B-red)](https://git-scm.com/)
[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Getting started

### First setup

1. Clone the repository:

    ```sh
    git clone git@github.com:knmlprz/ChatKNML.git
    ```

2. Navigate to the project directory:

    ```sh
    cd ChatKNML
    ```

3. Create a new branch for your development work:

    ```sh
    git checkout -b {your_branch_name}
    ```

4. Make sure you are working on the correct branch:

   ```sh
    git status
    ```

### Starting app development

1. Copy the `.env.example` file:

    ```sh
    cp .env.example .env
    ```

   Modify the environment variables to suit your requirements.

2. Launching services using the "dev" profile:

    ```sh
    docker compose --profile dev up
    ```

### Starting app production

#### Starting app

```sh
docker compose --profile prod up
```

### Starting llm and embedding

1. Download model (must have for service llm-embedding to work!!!)

    Download model (size of file 3.6GB ):

    ```sh
    curl -o ./llm/models/llama-2-7b.Q3_K_L.gguf -L https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q3_K_L.gguf
    ```

    or

    ```sh
    wget -P ./llm/models/llama-2-7b.Q3_K_L.gguf https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q3_K_L.gguf
    ```

2. Launching llm and embedding

    2.1. Running on cpu

    ```sh
    docker compose --profile cpu up
    ```

    2.2. Running on gpu

    ```sh
    docker compose --profile gpu up
    ```

#### LLM and embedding api swagger

Swegger with EP for completions(llm + embedding) and only embedding is [here](http://0.0.0.0:9000/docs)
