# nvidia-sniper

This bot helps us buy Nvidia Founders Edition GPUs as soon as they become available.

## Features

- Continuously monitor the availability of target GPU on www.nvidia.com
- Automatically checkout item using PayPal or as guest (credit card)
- Support for multiple locales (as specified in `data/customer.json`)
- Support for multiple GPUs (as specified in `data/gpus.json`)

## Usage

To use the bot, fill out `data/customer.json` and run the script.

```bash
pipenv run python -m sniper
```
![Alt text](screencast.gif)