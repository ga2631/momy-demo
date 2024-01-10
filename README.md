---
Appplication name: "Demo Momy backend"
Author: "Tan Huynh Nhat"
Created date: "08/01/2024"
---

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nJF1ZEi2VVKQHCjowKQekZiHXKos2Ukd#scrollTo=9pctmf7KmGvS)


# Source code demo Momy AI generate baby face

A simple code to generate baby face use some AI tool. This repo only use to demo, so the source code is not clear and not safety

My research document in [here](https://colab.research.google.com/drive/1nJF1ZEi2VVKQHCjowKQekZiHXKos2Ukd#scrollTo=9pctmf7KmGvS)[^1]

## Requirement
|Language/Package|Version|Description|
|:-|-:|:-|
|[python](https://www.python.org/downloads/release/python-3116/)|3.11.6|Programing language|
|[fastapi](https://pypi.org/project/fastapi/0.108.0/)|0.108.0|a modern, fast (high-performance), web framework for building APIs|
|[uvicorn](https://pypi.org/project/uvicorn/0.25.0/)|0.25.0|Uvicorn is an ASGI web server implementation for Python|
|[requests](https://pypi.org/project/requests/2.31.0/)|2.31.0|HTTP library|
|[pydantic](https://pypi.org/project/pydantic/2.5.3/)|2.5.3|Data validation library|
|[pydash](https://pypi.org/project/pydash/7.0.6/)|7.0.6|Lo-Dash for python|

## How to use

### Prepare enviroment

First, you need create virtualenv project's codebases. To do this, you must install [virtualenv](https://pypi.org/project/virtualenv/). Execute below command

```sh
pip install virtualenv
```

After install virtualenv, you need go to `app` dir and create virtualenv.

```sh
cd app
```

```sh
virtualenv enviroments
```

Now, you can install requirement package above. Or easier, you just execute below command

```sh
pip install -r requirements.txt
```

### Start server

At `app` dir, execute below command to start server

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

with:
`--host` Bind socket to this host. Default: 127.0.0.1
`--port` Bind socket to this port. If 0, an available port will be picked. Default: 8000

After start server, you can access the APIs of project. 

If you need API documentation, you can go to this url [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs). And boooom💥! All API are here

### Client

Just easy, open file `src/index.html`. Done!!!

## How to AI generate work

To generate baby image, you need an image of dad and an image of mom. You can upload in client page.

In client page, you can see 5 option generate:
1. Dad 0% - 100% Mom
2. Dad 25% - 75% Mom
3. Dad 50% - 50% Mom
4. Dad 75% - 25% Mom
5. Dad 100% - 0% Mom

By default, baby use face of Mom is base (face, jaw). If Dad similar percent > 50%, use face of Dad is base.

When you have 2 image of parents, we use Face++[^2] to merge 2 face in 1 face with merge rate is selected option above.

Then, depends on you want baby is male or female (select at "Sex" option in client too), we create an prompt to generate merged image to baby with cartoon style. The AI we use is Pixlr[^3].

## Pricing

> No such thing as a free lunch
>
> -- Pierre Dos Utt

The APIs we use are paid. 1 request generate is 0.12$. For detail, please keep an eye on reading

Face++ merge API[^4] is <strong>0.1\$</strong>\/request

Pixlr plus with 1.99\$\/80 Credits\/month[^5] equivalent to <strong>0.02\$</strong>\/4 credits\/4 image

**Total**: you must be charge <strong>0.12\$</strong>\/4 baby image

[^1]: [Momy document research](https://colab.research.google.com/drive/1nJF1ZEi2VVKQHCjowKQekZiHXKos2Ukd#scrollTo=9pctmf7KmGvS)
[^2]: [Face++](https://www.faceplusplus.com/) AI Open Platform is a platform offering computer vision technologies
[^3]: [Pixlr](https://pixlr.com/image-generator/) Generate an image using Generative AI by describing what you want to see
[^4]: [Face++ Image Beautify API price plan](https://www.faceplusplus.com/v2/pricing-details/#api_3) 
[^5]: [Pixlr price plan](https://pixlr.com/pricing) 