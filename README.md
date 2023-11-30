## ChatKNML

### Getting started

#### Embedding api

Download models (need git-lfs):

```sh
cd models
git clone git@hf.co:intfloat/e5-large-v2
```

After starting the app, OpenAI-compatible embedding API will be available at: http://172.16.3.101:5001/v1 Check the docs here: http://172.16.3.101:5001/docs 

#### llamacpp

Download models (this can take >1h):

```sh
wget https://huggingface.co/TheBloke/sheep-duck-llama-2-70B-v1.1-GGUF/resolve/main/sheep-duck-llama-2-70b-v1.1.Q4_K_S.gguf
```

#### Starting app

```sh
docker compose up -d
```
