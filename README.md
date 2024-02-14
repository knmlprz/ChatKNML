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

1. **Clone the repository**:

    ```sh
    git clone git@github.com:knmlprz/ChatKNML.git
    ```

2. **Navigate to the project directory**:

    ```sh
    cd ChatKNML
    ```

3. **Create a new branch for your development work**:

    ```sh
    git checkout -b {your_branch_name}
    ```

4. **Make sure you are working on the correct branch**:

   ```sh
    git status
    ```

### Starting app development

1. **Copy the `.env.example` file**:

    ```sh
    cp .env.example .env
    ```

   Modify the environment variables to suit your requirements.

2. Launching services using the "dev" profile:

    ```sh
    docker compose --profile dev up
    ```

### Starting app production

1. **Embedding api**:

    Download models (need git-lfs):

    ```sh
    cd models
    git clone git@hf.co:intfloat/e5-large-v2
    ```

    After starting the app, OpenAI-compatible embedding API will be available at: 
    <http://172.16.3.101:5001/v1>

    Check the docs here: <http://172.16.3.101:5001/docs>

2. **llamacpp**:

    Download models (this can take >1h):

    ```sh
    wget https://huggingface.co/TheBloke/sheep-duck-llama-2-70B-v1.1-GGUF/resolve/main/sheep-duck-llama-2-70b-v1.1.Q4_K_S.gguf
    ```

3. **Starting app**:

    ```sh
    docker compose --profile prod up
    ```
