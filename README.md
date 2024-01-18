---
Appplication name: "Demo Momy backend"
Author: "Tan Huynh Nhat"
Created date: "08/01/2024"
Version: "0.0.1 (Alpha)"
---

# Source code demo Momy AI generate baby face

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1nJF1ZEi2VVKQHCjowKQekZiHXKos2Ukd#scrollTo=9pctmf7KmGvS)

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
|[midjourney_api_client](https://pypi.org/project/midjourney-api-client/1.0.1)|1.0.1|Useapi.net provides a simple, reliable and affordable way to use Midjourney via standard REST API|

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

If you need API documentation, you can go to this url [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs). And... boooom💥! All API are here

### Client

Just easy, open file `src/index.html`. Done!!!

## How to AI generate work

To generate baby image, you need an image of parents, similar rate and sex of your AI baby. You can do that in client.

In client page, you can see 5 option `mom_percent` and `dad_percent` generate:
1. Dad **0%** - **100%** Mom
2. Dad **25%** - **75%** Mom
3. Dad **50%** - **50%** Mom
4. Dad **75%** - **25%** Mom
5. Dad **100%** - **0%** Mom

And, you can also see 2 option of `sex`:
* **Male**: is baby boy
* **Female**: is baby girl

When you upload image of parents, I save these images to server and upload to [Discord](https://discord.com). After upload to Discord, I will receive `mom_url` and `dad_url`.

Then, from your option selected, I generate a prompt for [Midjourney AI](https://www.midjourney.com/explore). Prompt structure is below
```
{mom_url} {dad_url} simple sticker cartoon neonate {sex} face, neonate {sex} face is smiling, image 1 similar rate is {mom_percent}% and image 2 similar rate is {dad_percent}% in white background, simple graphic design, symmetrical, 300 dpi, –-no glasses, –-no mockup --v 4 --s 750
```

After that, I use API of [useapi.net](https://useapi.net) to generate AI baby image.

## Pricing

> No such thing as a free lunch
>
> -- Pierre Dos Utt

In this project, I use Midjourney basic plan and useapi.net subscribe. Total price is **$20**/month

Base on Midjourney time generate to calculate cost of per user. Corporeality:
* Averange time of generate is 45 seconds = **$0.038**
* Fixed costs of useapi.net is **$0.038**
* Total cost of 1 user is **$0.076** ~ **1,866.75 VND**

### Discord

I can't find any plan of Discord pricing. But, I has been find discription of Discord[^2]

>All bots can make up to 50 requests per second to our API. If no authorization header is provided, then the limit is applied to the IP address. This is independent of any individual rate limit on a route. If your bot gets big enough, based on its functionality, it may be impossible to stay below 50 requests per second during normal operations.
>
>Global rate limit issues generally show up as repeatedly getting banned from the Discord API when your bot starts (see below). If your bot gets temporarily Cloudflare banned from the Discord API every once in a while, it is most likely not a global rate limit issue. You probably had a spike of errors that was not properly handled and hit our error threshold.

### Midjourney

Midjourney has 4 price plans[^3]

|Plan|Pricing|Corresponding quantity (1 user = 45s)|
|:-|-:|-:|
|Basic|$10/3.3 hr(s)/month|264 users/month|
|Standard|$15/15 hr(s)/month|1200 users/month|
|Pro|$60/30 hr(s)/month|2400 users|
|Mega|$120/60 hr(s)/month|4800 users|

### Useapi.net

**$10/monthly** subscription.[^4]


[^1]: [Momy document research](https://colab.research.google.com/drive/1nJF1ZEi2VVKQHCjowKQekZiHXKos2Ukd#scrollTo=9pctmf7KmGvS)
[^2]: [Discord Rate Limits](https://discord.com/developers/docs/topics/rate-limits)
[^3]: [Midjourney pricing plan](https://docs.midjourney.com/docs/plans)
[^4]: [Useapi.net pricing plan](https://useapi.net/docs/subscription)