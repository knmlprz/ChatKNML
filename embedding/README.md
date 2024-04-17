# embedding-api

## How run services

### GPU option

1. Instal git lfs
2. NVIDIA Docker Toolkit
3. Add shh key to huggingface account
4. run this in ChatKNML/ :

```sh
cd embedding/models
git clone git@hf.co:intfloat/e5-large-v2
```

### Aleternativ for 1,2,3

Copy every file form here:

#### IMPORTANT

Keep file tree like this !!!

```sh
models
├── e5-large-v2
│   ├── 1_Pooling
│   │   └── config.json
│   ├── config.json
│   ├── handler.py
│   ├── model.safetensors
│   ├── modules.json
│   ├── pytorch_model.bin
│   ├── README.md
│   ├── sentence_bert_config.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── vocab.txt
└── README.md
```

### NO GPU option

from `docker-compose.yml` remove:

```sh
deploy:
     resources:
       reservations:
         devices:
         - driver: nvidia
           count: 1
           capabilities: [ gpu ]

```

#### MOST IMPORTANT DON'T PUSH THIS CHANGE

#### Rest like in GPU option GLHF
