# nvidia-sniper

This bot helps us buy Nvidia Founders Edition GPUs as soon as they become available.

## Features

- Continuously monitor the availability of target GPU on www.nvidia.com
- Automatically checkout item using PayPal or as guest (credit card)
- Support for multiple locales (as specified in `data/customer.json`)
- Support for multiple GPUs (as specified in `data/gpus.json`)

<img src="screencast.gif" alt="screencast" width="500"/>

## Supported GPUs

- GeForce RTX 3090
- GeForce RTX 3080
- GeForce RTX 3070
- NVIDIA TITAN RTX
- GeForce RTX 2080 Super
- GeForce RTX 2070 Super
- GeForce RTX 2060 Super

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
3. Install Geckodriver using 
    - `brew install geckodriver`
4. Install Pipenv using 
    - `brew install pipenv`
5. Install project dependencies using 
    - `pipenv install`

### Windows
1. Install [Python](https://python-docs.readthedocs.io/en/latest/starting/install3/win.html) for Windows
2. Install the latest version of [Firefox](https://www.mozilla.org/de/firefox/new/)
3. Download [Geckodriver](https://github.com/mozilla/geckodriver/releases) and add executable to PATH or to `nvidia-sniper` directory
4. Open PowerShell and install Pipenv using 
    - `pip install pipenv`
5. Navigate to project directory using 
    - `cd nvidia-sniper` 
5. Install project dependencies using 
    - `pipenv install`
6. Install curses for Windows using 
    - `pipenv install windows-curses`

## Usage

To use the bot, fill out `data/customer.json` and run the script.

```bash
cd nvidia-sniper
pipenv run python -m sniper
```