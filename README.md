# nvidia-sniper [![discord](https://img.shields.io/discord/756303724095471617.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/S2SUzX)

This bot helps us buy Nvidia Founders Edition GPUs as soon as they become available.

## Features

- Continuously monitor the availability of target GPU on www.nvidia.com
- Automatically checkout item using PayPal or as guest (credit card)
- Automatically submit the order for credit card payment 
- Support for multiple locales (as defined in `data/customer.json`)
- Support for multiple GPUs (as defined in `data/gpus.json`)

<img src="screencast.gif" alt="screencast" width="640"/>

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
sudo apt install firefox python3 pipenv
cd nvidia-sniper
pipenv install
```

### Mac
1. Install the latest version of [Firefox](https://www.firefox.com/)
2. Install [brew](https://brew.sh/index_de) package manager
3. Install Pipenv using 
    - `brew install pipenv`
4. Navigate to project directory using 
    - `cd nvidia-sniper` 
5. Install project dependencies using 
    - `pipenv install`

### Windows
1. Install [Python](https://python-docs.readthedocs.io/en/latest/starting/install3/win.html) for Windows
2. Install the latest version of [Firefox](https://www.firefox.com/)
3. Open PowerShell and install Pipenv using 
    - `pip install pipenv`
4. Navigate to project directory using 
    - `cd nvidia-sniper` 
5. Install project dependencies using 
    - `pipenv install`
6. Install curses for Windows using 
    - `pipenv install windows-curses`

## Updating
To update `nvidia-sniper` use, `git pull` or download a fresh `.zip` archive from GitHub.

Make sure to back up the `customer.json` in advance as it might get replaced in the process.
## Usage

To use the bot, fill out `data/customer.json` and run the script.

```bash
cd nvidia-sniper
pipenv run python -m sniper
```
## Configuration
In the `customer.json` file, some fields require specific values.

### `notification`
The bot can send multiple apprise notifications, including a screenshot attachment upon successful checkout. See https://github.com/caronc/apprise#supported-notifications for more information. Add additional entries to the `notification` dictionary in the `customer.json` file for multiple providers. For each notification channel, a custom `message` and a `title` can be set. Additionally, the `screenshot` attachment can be toggled per channel.

A couple of example URLs for different notification services: 
- `pover://user@token`: Pushover
- `tgram://bottoken/ChatID`: Telegram
- `discord://webhook_id/webhook_token`: Discord

### `locale`
The `locale` field can have the following values:
- `de-at`: Austria
- `fr-fr`: Belgium
- `en-us`: Canada
- `cs-cz`: Czech Republic
- `da-dk`: Denmark
- `fi-fi`: Finland
- `fr-fr`: France
- `de-de`: Germany
- `it-it`: Italy
- `fr-fr`: Luxembourg
- `pl-pl`: Poland
- `ru-ru`: Russian Federation
- `es-es`: Spain
- `sv-se`: Sweden
- `en-gb`: United Kingdom
- `en-us`: United States

### `speed`
The `speed` field can have the following values:
- `shippingOptionID2`: Standard Ground
- `shippingOptionID3`: Next Business day Afternoon
- `shippingOptionID4`: Second Business Day Afternoon

### `country`
The `country` field can have the following values:
- `AT`: Austria
- `BE`: Belgium
- `CA`: Canada
- `CZ`: Czech Republic
- `DK`: Denmark
- `FI`: Finland
- `FR`: France
- `DE`: Germany
- `IT`: Italy
- `LU`: Luxembourg
- `PL`: Poland
- `RU`: Russian Federation
- `ES`: Spain
- `SE`: Sweden
- `GB`: United Kingdom
- `US`: United States

### `state`
For `en-us` locale, the `state` field can have the following values:
- `AL`: Alabama
- `AK`: Alaska
- `AB`: Alberta
- `AS`: American Samoa
- `AZ`: Arizona
- `AR`: Arkansas
- `AA`: Armed Forces America
- `AE`: Armed Forces Europe
- `AP`: Armed Forces Pacific
- `BC`: British Columbia
- `CA`: California
- `CO`: Colorado
- `CT`: Connecticut
- `DE`: Delaware
- `DC`: District Of Columbia
- `FM`: Federated States of Micronesia
- `FL`: Florida
- `GA`: Georgia
- `GU`: Guam
- `HI`: Hawaii
- `ID`: Idaho
- `IL`: Illinois
- `IN`: Indiana
- `IA`: Iowa
- `KS`: Kansas
- `KY`: Kentucky
- `LA`: Louisiana
- `ME`: Maine
- `MB`: Manitoba
- `MH`: Marshall Islands
- `MD`: Maryland
- `MA`: Massachusetts
- `MI`: Michigan
- `MN`: Minnesota
- `MS`: Mississippi
- `MO`: Missouri
- `MT`: Montana
- `NE`: Nebraska
- `NV`: Nevada
- `NB`: New Brunswick
- `NH`: New Hampshire
- `NJ`: New Jersey
- `NM`: New Mexico
- `NY`: New York
- `NL`: Newfoundland and Labrador
- `NC`: North Carolina
- `ND`: North Dakota
- `MP`: Northern Mariana Islands
- `NT`: Northwest Territories
- `NS`: Nova Scotia
- `NU`: Nunavut
- `OH`: Ohio
- `OK`: Oklahoma
- `ON`: Ontario
- `OR`: Oregon
- `PW`: Palau
- `PA`: Pennsylvania
- `PE`: Prince Edward Island
- `PR`: Puerto Rico
- `QC`: Quebec
- `RI`: Rhode Island
- `SK`: Saskatchewan
- `SC`: South Carolina
- `SD`: South Dakota
- `TN`: Tennessee
- `TX`: Texas
- `UT`: Utah
- `VT`: Vermont
- `VI`: Virgin Islands
- `VA`: Virginia
- `WA`: Washington
- `WV`: West Virginia
- `WI`: Wisconsin
- `WY`: Wyoming
- `YT`: Yukon
