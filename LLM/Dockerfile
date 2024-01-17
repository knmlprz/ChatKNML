FROM python:3.11-buster as builder

RUN pip install poetry==1.6.1
RUN apt-get update && apt-get install -y git
RUN git clone --recurse-submodules https://github.com/abetlen/llama-cpp-python.git
# RUN mkdir models && cd models && wget https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q2_K.gguf



ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root


FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . ./

ENV CMAKE_ARGS="-DLLAMA_CUBLAS=ON"
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python[server]
RUN python3 -m llama_cpp.server --model models/llama-2-7b.Q2_K.gguf --n_gpu_layers 9999999

ENTRYPOINT ["python", "-m", "test_conetion.py"]
