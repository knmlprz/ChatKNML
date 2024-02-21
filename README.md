# ChatKNML

## Getting started

### Starting app development

Launching services using the "dev" profile:

```sh
docker compose --profile dev up
```

### Starting app production

#### Embedding api

Download models (need git-lfs):

```sh
cd models
git clone git@hf.co:intfloat/e5-large-v2
```

After starting the app, OpenAI-compatible embedding API will be available at: <http://172.16.3.101:5001/v1>

 Check the docs here: <http://172.16.3.101:5001/docs>

#### Download llm model (must have for servis llm to work !!!)

Download model (this can take ~6min):

```sh
wget -P ./llm/models https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q3_K_L.gguf
```

#### Starting app

```sh
docker compose --profile prod up
```
