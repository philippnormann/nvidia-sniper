# nvidia-sniper

This bot helps us buy Nvidia Founders Edition GPUs as soon as they become available.

## Features

- Continuously monitor the availability of target GPU on www.nvidia.com
- Automatically checkout item using PayPal or as guest (credit card)
- Support for multiple locales (as specified in `data/customer.json`)
- Support for multiple GPUs (as specified in `data/gpus.json`)

<img src="screencast.gif" alt="screencast" width="500"/>

## Installation

To run the bot, we need the following things:

- Python 3.8
- Pipenv
- Firefox
- Geckodriver

### Linux (Ubuntu)
```bash
sudo apt install firefox firefox-geckodriver python3 pipenv
cd nvidia-sniper
pipenv install
```

### Mac
1. Install the latest version of [Firefox](https://www.mozilla.org/de/firefox/new/)
2. Install [brew](https://brew.sh/index_de) package manager
3. Install Geckodriver using `brew install geckodriver`
4. Install Pipenv using `brew install pipenv`
5. Install project dependencies using `pipenv install`

### Windows
1. Install [Python](https://www.python.org/downloads/release/python-380/) for Windows
2. Install the latest version of [Firefox](https://www.mozilla.org/de/firefox/new/)
3. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) and add it to PATH or folder source
4. Install Pipenv using `pip install pipenv`
5. Install project dependencies using `pipenv install`
6. Install curses for Windows using `pipenv install windows-curses`

## Usage

To use the bot, fill out `data/customer.json` and run the script.

```bash
pipenv run python -m sniper
```