# Embeding-api

## How run servis 

### GPU option

1. Instal git lfs
2. NVIDIA Docker Toolkit [link](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) 
3. Add shh key to hugingface  account [link](https://huggingface.co/docs/hub/security-git-ssh) or [link](https://huggingface.co/blog/password-git-deprecation)

4. run this in ChatKNML/ :
```sh
cd embeding_models
git clone git@hf.co:intfloat/e5-large-v2
```
### Aleternativ for 1,2,3

copy evry flie form here: [link](https://huggingface.co/intfloat/multilingual-e5-large/tree/main)

#### IMPORTANT

keep file tree like this !!!

```sh
embeding_models
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
48 deploy:
49      resources:
50        reservations:
51          devices:
52          - driver: nvidia
53            count: 1
54            capabilities: [ gpu ]

```

#### <span style="color: red;">MOST IMPORTANT DONT PUSH THIS CHANGE !!!</span>

ps. Patryk don't kill me :'(  I want help to beginers. 

#### Rest like in GPU option GLHF :)
