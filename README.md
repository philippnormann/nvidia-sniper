# nvidia-sniper

This bot helps us buy Nvidia Founders Edition GPUs as soon as they become available.

## Features

- Continuously monitor the availability of target GPU on www.nvidia.com
- Automatically checkout item using PayPal or as guest (credit card)
- Support for multiple locales (as specified in `data/customer.json`)
- Support for multiple GPUs (as specified in `data/gpus.json`)

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
sudo apt install firefox firefox-geckodriver python3 pipenv
cd nvidia-sniper
pipenv install
```

### Mac
1. Install the latest version of [Firefox](https://www.firefox.com/)
2. Install [brew](https://brew.sh/index_de) package manager
3. Install Geckodriver using 
    - `brew install geckodriver`
4. Install Pipenv using 
    - `brew install pipenv`
5. Install project dependencies using 
    - `pipenv install`

### Windows
1. Install [Python](https://python-docs.readthedocs.io/en/latest/starting/install3/win.html) for Windows
2. Install the latest version of [Firefox](https://www.firefox.com/)
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
## Configuration
In the `customer.json` file, some fields require specific values.

### `locale`
The `locale` field can have the following values:
- `en-us`
- `en-gb`
- `de-de`
- `fr-fr`
- `it-it`
- `es-es`
- `nl-nl`
- `sv-se`
- `de-at`
- `fr-be`

### `speed`
The `speed` field can have the following values:
- `shippingOptionID2`: Standard Ground
- `shippingOptionID3`: Next Business day Afternoon
- `shippingOptionID4`: Second Business Day Afternoon

### `country`
The `country` field can have the following values:
- `AF`: Afghanistan
- `AL`: Albania
- `DZ`: Algeria
- `AS`: American Samoa
- `AD`: Andorra
- `AI`: Anguilla
- `AQ`: Antarctica
- `AG`: Antigua and Barbuda
- `AR`: Argentina
- `AM`: Armenia
- `AW`: Aruba
- `AU`: Australia
- `AT`: Austria
- `AZ`: Azerbaidjan
- `BS`: Bahamas
- `BH`: Bahrain
- `BD`: Bangladesh
- `BB`: Barbados
- `BY`: Belarus
- `BE`: Belgium
- `BZ`: Belize
- `BJ`: Benin
- `BM`: Bermuda
- `BT`: Bhutan
- `BO`: Bolivia
- `BQ`: Bonaire, Saint Eustatius and Saba
- `BA`: Bosnia-Herzegovina
- `BW`: Botswana
- `BV`: Bouvet Island
- `BR`: Brazil
- `IO`: British Indian Ocean Territory
- `BN`: Brunei Darussalam
- `BG`: Bulgaria
- `BF`: Burkina Faso
- `BI`: Burundi
- `KH`: Cambodia
- `CM`: Cameroon
- `CA`: Canada
- `IC`: Canary Islands
- `CV`: Cape Verde
- `KY`: Cayman Islands
- `CF`: Central African Republic
- `TD`: Chad
- `CL`: Chile
- `CN`: China
- `CX`: Christmas Island
- `CC`: Cocos (Keeling) Islands
- `CO`: Colombia
- `KM`: Comoros
- `CG`: Congo
- `CD`: Congo, The Democratic Republic Of The
- `CK`: Cook Islands
- `CR`: Costa Rica
- `HR`: Croatia
- `CW`: Curaçao
- `CY`: Cyprus
- `CZ`: Czech Republic
- `DK`: Denmark
- `DJ`: Djibouti
- `DM`: Dominica
- `DO`: Dominican Republic
- `TL`: EAST TIMOR
- `EC`: Ecuador
- `EG`: Egypt
- `SV`: El Salvador
- `GQ`: Equatorial Guinea
- `ER`: Eritrea
- `EE`: Estonia
- `ET`: Ethiopia
- `FK`: Falkland Islands
- `FO`: Faroe Islands
- `FJ`: Fiji
- `FI`: Finland
- `FR`: France
- `GF`: French Guiana
- `TF`: French Southern Territories
- `GA`: Gabon
- `GM`: Gambia
- `GE`: Georgia
- `DE`: Germany
- `GH`: Ghana
- `GI`: Gibraltar
- `GR`: Greece
- `GL`: Greenland
- `GD`: Grenada
- `GP`: Guadeloupe (French)
- `GU`: Guam (USA)
- `GT`: Guatemala
- `GG`: Guernsey
- `GN`: Guinea
- `GW`: Guinea Bissau
- `GY`: Guyana
- `HT`: Haiti
- `HM`: Heard and McDonald Islands
- `HN`: Honduras
- `HK`: Hong Kong
- `HU`: Hungary
- `IS`: Iceland
- `IN`: India
- `ID`: Indonesia
- `IQ`: Iraq
- `IE`: Ireland
- `IM`: Isle of Man
- `IL`: Israel
- `IT`: Italy
- `CI`: Ivory Coast (Cote D'Ivoire)
- `JM`: Jamaica
- `JP`: Japan
- `JE`: Jersey
- `JO`: Jordan
- `KZ`: Kazakhstan
- `KE`: Kenya
- `KI`: Kiribati
- `KW`: Kuwait
- `KG`: Kyrgyzstan
- `LA`: Laos
- `LV`: Latvia
- `LB`: Lebanon
- `LS`: Lesotho
- `LR`: Liberia
- `LY`: Libyan Arab Jamahiriya
- `LI`: Liechtenstein
- `LT`: Lithuania
- `LU`: Luxembourg
- `MO`: Macau
- `MK`: Macedonia
- `MG`: Madagascar
- `MW`: Malawi
- `MY`: Malaysia
- `MV`: Maldives
- `ML`: Mali
- `MT`: Malta
- `MH`: Marshall Islands
- `MQ`: Martinique
- `MR`: Mauritania
- `MU`: Mauritius
- `YT`: Mayotte
- `MX`: Mexico
- `FM`: Micronesia, Federated States of
- `MD`: Moldavia, Republic of
- `MC`: Monaco
- `MN`: Mongolia
- `ME`: Montenegro
- `MS`: Montserrat
- `MA`: Morocco
- `MZ`: Mozambique
- `MM`: Myanmar
- `NA`: Namibia
- `NR`: Nauru
- `NP`: Nepal
- `NL`: Netherlands
- `NC`: New Caledonia (French)
- `NZ`: New Zealand
- `NI`: Nicaragua
- `NE`: Niger
- `NG`: Nigeria
- `NU`: Niue
- `NF`: Norfolk Island
- `MP`: Northern Mariana Islands
- `NO`: Norway
- `OM`: Oman
- `PK`: Pakistan
- `PW`: Palau
- `PS`: Palestinaian Territory
- `PA`: Panama
- `PG`: Papua New Guinea
- `PY`: Paraguay
- `PE`: Peru
- `PH`: Philippines
- `PN`: Pitcairn Island
- `PL`: Poland
- `PF`: Polynesia (French)
- `PT`: Portugal
- `PR`: Puerto Rico
- `QA`: Qatar
- `RE`: Reunion (French)
- `RO`: Romania
- `RU`: Russian Federation
- `GS`: S. Georgia and S. Sandwich Isls.
- `BL`: Saint Barthélemy
- `SH`: Saint Helena
- `KN`: Saint Kitts and Nevis Anguilla
- `LC`: Saint Lucia
- `MF`: Saint Martin (French part)
- `PM`: Saint Pierre and Miquelon
- `ST`: Saint Tome and Principe
- `VC`: Saint Vincent and Grenadines
- `WS`: Samoa
- `SM`: San Marino
- `SA`: Saudi Arabia
- `SN`: Senegal
- `RS`: Serbia
- `SC`: Seychelles
- `SL`: Sierra Leone
- `SG`: Singapore
- `SX`: Sint Maarten (Dutch part)
- `SK`: Slovak Republic
- `SI`: Slovenia
- `SB`: Solomon Islands
- `ZA`: South Africa
- `KR`: South Korea
- `ES`: Spain
- `LK`: Sri Lanka
- `SR`: Suriname
- `SJ`: Svalbard and Jan Mayen Islands
- `SZ`: Swaziland
- `SE`: Sweden
- `CH`: Switzerland
- `TW`: Taiwan
- `TJ`: Tajikistan
- `TZ`: Tanzania
- `TH`: Thailand
- `TG`: Togo
- `TK`: Tokelau
- `TO`: Tonga
- `TT`: Trinidad and Tobago
- `TN`: Tunisia
- `TR`: Turkey
- `TM`: Turkmenistan
- `TC`: Turks and Caicos Islands
- `TV`: Tuvalu
- `UG`: Uganda
- `UA`: Ukraine
- `AE`: United Arab Emirates
- `GB`: United Kingdom
- `US`: United States
- `UM`: United States Minor Outlying Islands
- `UY`: Uruguay
- `UZ`: Uzbekistan
- `VU`: Vanuatu
- `VA`: Vatican City State
- `VE`: Venezuela
- `VN`: Vietnam
- `VG`: Virgin Islands (British)
- `VI`: Virgin Islands (USA)
- `WF`: Wallis and Futuna Islands
- `EH`: Western Sahara
- `YE`: Yemen
- `ZM`: Zambia
- `AX`: Åland Islands

### `state`
For `en-us` locale the `state` field can have the following values:
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

### `notification`
Multiple apprise notifications can be send on successful checkout. See https://github.com/caronc/apprise#supported-notifications for more information. Add another entry to the notification dict for multiple providers, any name can be used.